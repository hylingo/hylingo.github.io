import { ref } from 'vue'
import firebase from 'firebase/compat/app'
import 'firebase/compat/database'
import 'firebase/compat/auth'
import { t } from '@/i18n'
import { mergeListenCountMaps } from '@/utils/listenCount'
import { cloudSync } from '@/config/thresholds'
import { milestoneStateTick } from '@/learning/milestoneTick'
import {
  readLangBundle,
  writeLangBundleFull,
  SYNCED_CLOUD_KEYS,
  type LangBundle,
} from '@/learning/learnStorage'
import type { StudyLang, StatsMap, DayStats } from '@/types'
import { safeSet, safeRemove, safeGetNumber } from '@/storage/safeLS'
import { LS } from '@/storage/keys'
import { readPracticeSlot, writePracticeSlot } from '@/storage/practiceSlot'

const firebaseConfig = {
  apiKey: "AIzaSyBCZa2CyskF8bM_CU0l2UaT7Wwq25cz30Q",
  authDomain: "jp-learn-e01bd.firebaseapp.com",
  databaseURL: "https://jp-learn-e01bd-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "jp-learn-e01bd",
  storageBucket: "jp-learn-e01bd.firebasestorage.app",
  messagingSenderId: "1055060519096",
  appId: "1:1055060519096:web:ed0421d0a6938186c6ec4d",
}

// userId 现在仅用作显示名（来自 Firebase Auth 的 displayName，等同注册时的用户名）。
// 真正用于 RTDB 路径的是 Firebase Auth 的 UID（见 currentUid()）。
const userId = ref('')
let db: firebase.database.Database | null = null
let auth: firebase.auth.Auth | null = null
let syncTimer: ReturnType<typeof setTimeout> | null = null

/** 用户名 → 伪邮箱：交给 Firebase Auth 认证 */
const PSEUDO_EMAIL_DOMAIN = '@hylingo.local'
function usernameToEmail(name: string): string {
  return name.toLowerCase() + PSEUDO_EMAIL_DOMAIN
}

function currentUid(): string | null {
  return auth?.currentUser?.uid ?? null
}

/** 所有 RTDB .set 串行 + await，避免多次上传乱序完成用旧快照覆盖新数据（测验队列等） */
let serializedCloudChain: Promise<void> = Promise.resolve()

function runSerialized<T>(task: () => Promise<T>): Promise<T> {
  const p = serializedCloudChain.then(() => task())
  serializedCloudChain = p.then(
    () => undefined,
    () => undefined,
  )
  return p
}

function emptyBundle(): LangBundle {
  const b = {} as LangBundle
  for (const ck of SYNCED_CLOUD_KEYS) {
    b[ck] = {}
  }
  return b
}

function asFullBundle(partial: Partial<LangBundle> | undefined | null): LangBundle {
  const e = emptyBundle()
  if (!partial) return e
  for (const ck of SYNCED_CLOUD_KEYS) {
    const v = partial[ck]
    if (v != null && typeof v === 'object' && !Array.isArray(v)) {
      e[ck] = v
    }
  }
  return e
}

/** 只认 schemaVersion:2 + langs；其余形状视为空桶 */
function parseCloudLangs(cloud: unknown): Record<StudyLang, LangBundle> {
  const blank = (): Record<StudyLang, LangBundle> => ({ ja: emptyBundle(), en: emptyBundle() })
  if (!cloud || typeof cloud !== 'object' || Array.isArray(cloud)) {
    return blank()
  }
  const c = cloud as Record<string, unknown>
  if (c.schemaVersion !== 2 || !c.langs || typeof c.langs !== 'object' || Array.isArray(c.langs)) {
    return blank()
  }
  const L = c.langs as Record<string, unknown>
  return {
    ja: asFullBundle(L.ja as Partial<LangBundle>),
    en: asFullBundle(L.en as Partial<LangBundle>),
  }
}

function rawResetAtMs(cloud: unknown): number {
  if (!cloud || typeof cloud !== 'object' || Array.isArray(cloud)) return 0
  const v = (cloud as Record<string, unknown>).resetAt
  const n = typeof v === 'number' ? v : Number(v)
  return Number.isFinite(n) && n > 0 ? n : 0
}

function mergeMaxNumbers(a: Record<string, number>, b: Record<string, number>): Record<string, number> {
  const merged = { ...a }
  for (const key in b) {
    merged[key] = Math.max(merged[key] || 0, b[key] || 0)
  }
  return merged
}

function mergeLaterReviewDates(a: Record<string, string>, b: Record<string, string>): Record<string, string> {
  const merged = { ...a }
  for (const key in b) {
    const vb = b[key]
    if (!merged[key] || vb > merged[key]) merged[key] = vb
  }
  return merged
}

function mergeDismissed(a: Record<string, true>, b: Record<string, true>): Record<string, true> {
  return { ...a, ...b }
}

function mergeStats(a: StatsMap, b: StatsMap): StatsMap {
  const merged: StatsMap = {}
  const allDays = new Set([...Object.keys(a), ...Object.keys(b)])
  for (const day of allDays) {
    const da: Partial<DayStats> = a[day] || {}
    const db: Partial<DayStats> = b[day] || {}
    merged[day] = {
      studied: Math.max(da.studied || 0, db.studied || 0),
      quizzed: Math.max(da.quizzed || 0, db.quizzed || 0),
      correct: Math.max(da.correct || 0, db.correct || 0),
      listened: Math.max(da.listened || 0, db.listened || 0),
      recorded: Math.max(da.recorded || 0, db.recorded || 0),
      followCompleted: Math.max(da.followCompleted || 0, db.followCompleted || 0),
      followSentences: Math.max(da.followSentences || 0, db.followSentences || 0),
      wrong: mergeMaxNumbers(da.wrong || {}, db.wrong || {}),
    }
  }
  return merged
}

// LangBundle 字段类型为 unknown（来自 LS / 云端 JSON），合并前在边界处断言。
type NumMap = Record<string, number>
type DismissedMap = Record<string, true>
type DateMap = Record<string, string>

function mergeLangBundle(local: LangBundle, cloud: LangBundle): LangBundle {
  return {
    stats: mergeStats((local.stats || {}) as StatsMap, (cloud.stats || {}) as StatsMap),
    counts: mergeMaxNumbers((local.counts || {}) as NumMap, (cloud.counts || {}) as NumMap),
    delays: mergeLaterReviewDates((local.delays || {}) as DateMap, (cloud.delays || {}) as DateMap),
    listened: mergeListenCountMaps((local.listened || {}) as NumMap, (cloud.listened || {}) as NumMap),
    practiceRecognized: mergeDismissed(
      (local.practiceRecognized || {}) as DismissedMap,
      (cloud.practiceRecognized || {}) as DismissedMap,
    ),
    masteryQuizPassed: mergeDismissed(
      (local.masteryQuizPassed || {}) as DismissedMap,
      (cloud.masteryQuizPassed || {}) as DismissedMap,
    ),
    quizQueue: mergeMaxNumbers((local.quizQueue || {}) as NumMap, (cloud.quizQueue || {}) as NumMap),
    starred: mergeDismissed((local.starred || {}) as DismissedMap, (cloud.starred || {}) as DismissedMap),
    practiceStreak: mergeMaxNumbers(
      (local.practiceStreak || {}) as NumMap,
      (cloud.practiceStreak || {}) as NumMap,
    ),
    articlePerfect: mergeArticlePerfect(
      (local.articlePerfect || {}) as Record<string, Record<string, true>>,
      (cloud.articlePerfect || {}) as Record<string, Record<string, true>>,
    ),
  }
}

function mergeArticlePerfect(
  a: Record<string, Record<string, true>>,
  b: Record<string, Record<string, true>>,
): Record<string, Record<string, true>> {
  const out: Record<string, Record<string, true>> = {}
  const keys = new Set([...Object.keys(a), ...Object.keys(b)])
  for (const k of keys) {
    out[k] = { ...(a[k] || {}), ...(b[k] || {}) }
  }
  return out
}

function langBundleHasAny(b: LangBundle): boolean {
  for (const ck of SYNCED_CLOUD_KEYS) {
    const v = b[ck]
    if (v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).length > 0) return true
  }
  return false
}

function readBothBundlesFromLS(): Record<StudyLang, LangBundle> {
  return {
    ja: readLangBundle('ja'),
    en: readLangBundle('en'),
  }
}

function writeBothBundlesToLS(ja: LangBundle, en: LangBundle) {
  writeLangBundleFull('ja', ja)
  writeLangBundleFull('en', en)
  milestoneStateTick.value++
}

type PracticeSlotCloud = { id: string; title: string; index: number }
type PracticeSlotsCloud = { essay?: PracticeSlotCloud | null; dialogue?: PracticeSlotCloud | null }

function readPracticeSlots(): PracticeSlotsCloud {
  const result: PracticeSlotsCloud = {}
  for (const fmt of ['essay', 'dialogue'] as const) {
    const slot = readPracticeSlot(fmt)
    if (slot) result[fmt] = slot
  }
  return result
}

function writePracticeSlots(slots: PracticeSlotsCloud) {
  for (const fmt of ['essay', 'dialogue'] as const) {
    writePracticeSlot(fmt, slots[fmt] ?? null)
  }
}

function buildV2Payload(ja: LangBundle, en: LangBundle, resetAt?: number) {
  const payload: Record<string, unknown> = {
    schemaVersion: 2,
    langs: { ja, en },
    practiceSlots: readPracticeSlots(),
  }
  if (resetAt != null && resetAt > 0) payload.resetAt = resetAt
  return payload
}

let _initResolved = false
function initFirebase(): Promise<void> {
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig)
  }
  db = firebase.database()
  auth = firebase.auth()
  return new Promise<void>((resolve) => {
    auth!.onAuthStateChanged((user) => {
      userId.value = user?.displayName || ''
      if (!_initResolved) {
        _initResolved = true
        resolve()
      }
    })
  })
}

async function performCloudUpload(): Promise<void> {
  const uid = currentUid()
  if (!uid || !db) return
  const { ja, en } = readBothBundlesFromLS()
  if (!langBundleHasAny(ja) && !langBundleHasAny(en)) return
  const resetAt = safeGetNumber(LS.FB_RESET_AT, 0)
  await db.ref('users/' + uid + '/data').set(
    buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined),
  )
}

function syncToCloud() {
  if (!currentUid() || !db) return
  runSerialized(() => performCloudUpload()).catch(() => {})
}

async function flushDataToCloud(): Promise<void> {
  const uid = currentUid()
  if (!uid || !db) return
  const resetAt = Date.now()
  safeSet(LS.FB_RESET_AT, String(resetAt))
  await runSerialized(async () => {
    const { ja, en } = readBothBundlesFromLS()
    await db!.ref('users/' + uid + '/data').set(buildV2Payload(ja, en, resetAt))
  })
}

function debouncedSync() {
  if (syncTimer) clearTimeout(syncTimer)
  syncTimer = setTimeout(() => {
    syncTimer = null
    syncToCloud()
  }, cloudSync.debounceMs)
}

function parseOneSlot(raw: unknown): PracticeSlotCloud | null {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null
  const { id, title, index } = raw as Record<string, unknown>
  if (typeof id !== 'string' || !id) return null
  return { id, title: typeof title === 'string' ? title : '', index: typeof index === 'number' ? index : 0 }
}

function parseCloudPracticeSlots(cloud: unknown): PracticeSlotsCloud {
  if (!cloud || typeof cloud !== 'object' || Array.isArray(cloud)) return {}
  const c = cloud as Record<string, unknown>
  // 兼容旧格式 practiceArticle（单槽位）
  if (c.practiceArticle && !c.practiceSlots) {
    const s = parseOneSlot(c.practiceArticle)
    return s ? { essay: s } : {}
  }
  const ps = c.practiceSlots
  if (!ps || typeof ps !== 'object' || Array.isArray(ps)) return {}
  const slots = ps as Record<string, unknown>
  return {
    essay: parseOneSlot(slots.essay) || undefined,
    dialogue: parseOneSlot(slots.dialogue) || undefined,
  }
}

/** 将云端 v2 数据合并进本地并写回 LS；上传 payload 须由调用方在合并后再次 readBothBundlesFromLS 构建，以免 await 间隙内的新写入丢失 */
function mergeCloudIntoLocal(cloudRaw: unknown): void {
  const localResetAt = safeGetNumber(LS.FB_RESET_AT, 0)
  const cloudResetAt = rawResetAtMs(cloudRaw)
  const cloudLangs = parseCloudLangs(cloudRaw)

  // 合并云端练习槽位：每个槽位独立合并，同篇取更大进度
  const cloudSlots = parseCloudPracticeSlots(cloudRaw)
  const localSlots = readPracticeSlots()
  const mergedSlots: PracticeSlotsCloud = { ...localSlots }
  for (const fmt of ['essay', 'dialogue'] as const) {
    const cs = cloudSlots[fmt]
    const ls = localSlots[fmt]
    if (cs && !ls) {
      mergedSlots[fmt] = cs
    } else if (cs && ls && cs.id === ls.id && cs.index > ls.index) {
      mergedSlots[fmt] = cs
    }
  }
  writePracticeSlots(mergedSlots)

  // 仅当本机已有 reset 游标且云端更新时整桶以云端为准。
  if (cloudResetAt > localResetAt && localResetAt > 0) {
    writeBothBundlesToLS(cloudLangs.ja, cloudLangs.en)
    safeSet(LS.FB_RESET_AT, String(cloudResetAt))
    writePracticeSlots(cloudSlots)
    return
  }

  const localJa = readLangBundle('ja')
  const localEn = readLangBundle('en')
  const mergedJa = mergeLangBundle(localJa, cloudLangs.ja)
  const mergedEn = mergeLangBundle(localEn, cloudLangs.en)
  writeBothBundlesToLS(mergedJa, mergedEn)

  const nextResetMarker = Math.max(localResetAt, cloudResetAt)
  if (nextResetMarker > 0) {
    safeSet(LS.FB_RESET_AT, String(nextResetMarker))
  }
}

async function pullAndMerge(): Promise<boolean> {
  const uid = currentUid()
  if (!uid || !db) return false
  try {
    return await runSerialized(async () => {
      const snap = await db!.ref('users/' + uid + '/data').once('value')
      if (!snap.exists()) return false
      mergeCloudIntoLocal(snap.val())
      const { ja, en } = readBothBundlesFromLS()
      const resetAt = safeGetNumber(LS.FB_RESET_AT, 0)
      await db!.ref('users/' + uid + '/data').set(
        buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined),
      )
      return true
    })
  } catch {
    return false
  }
}

type FirebaseAuthError = { code?: string }

async function register(username: string, password: string): Promise<{ success: boolean; message: string }> {
  const name = username.trim().toLowerCase()
  if (!name || name.length < 2) {
    return { success: false, message: t('loginMinLen') }
  }
  if (!/^[a-z0-9_-]+$/.test(name)) {
    return { success: false, message: t('loginFormat') }
  }
  if (password.length < 6) {
    return { success: false, message: t('passwordMinLen') }
  }
  if (!auth || !db) {
    return { success: false, message: t('loginFail') }
  }

  try {
    const cred = await auth.createUserWithEmailAndPassword(usernameToEmail(name), password)
    const user = cred.user
    if (!user) return { success: false, message: t('loginFail') }
    await user.updateProfile({ displayName: name })
    userId.value = name

    // 注册后把本地已有数据上传一份做初始化
    const { ja, en } = readBothBundlesFromLS()
    if (langBundleHasAny(ja) || langBundleHasAny(en)) {
      const resetAt = safeGetNumber(LS.FB_RESET_AT, 0)
      await runSerialized(async () => {
        await db!
          .ref('users/' + user.uid + '/data')
          .set(buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined))
      })
    }

    return { success: true, message: t('registerSuccess') }
  } catch (e) {
    const code = (e as FirebaseAuthError)?.code
    if (code === 'auth/email-already-in-use') {
      return { success: false, message: t('usernameTaken') }
    }
    if (code === 'auth/weak-password') {
      return { success: false, message: t('passwordMinLen') }
    }
    return { success: false, message: t('loginFail') }
  }
}

async function login(username: string, password: string): Promise<{ success: boolean; message: string }> {
  const name = username.trim().toLowerCase()
  if (!name || name.length < 2) {
    return { success: false, message: t('loginMinLen') }
  }
  if (!password) {
    return { success: false, message: t('passwordMinLen') }
  }
  if (!auth || !db) {
    return { success: false, message: t('loginFail') }
  }

  try {
    const cred = await auth.signInWithEmailAndPassword(usernameToEmail(name), password)
    const user = cred.user
    if (!user) return { success: false, message: t('loginFail') }
    userId.value = user.displayName || name

    const cloudSnap = await db.ref('users/' + user.uid + '/data').once('value')
    if (cloudSnap.exists()) {
      const cloud = cloudSnap.val()
      await runSerialized(async () => {
        mergeCloudIntoLocal(cloud)
        const { ja, en } = readBothBundlesFromLS()
        const resetAt = safeGetNumber(LS.FB_RESET_AT, 0)
        await db!.ref('users/' + user.uid + '/data').set(
          buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined),
        )
      })
    }

    return { success: true, message: t('loginFound') }
  } catch (e) {
    const code = (e as FirebaseAuthError)?.code
    if (code === 'auth/user-not-found') {
      return { success: false, message: t('userNotFound') }
    }
    if (code === 'auth/wrong-password' || code === 'auth/invalid-credential' || code === 'auth/invalid-login-credentials') {
      return { success: false, message: t('wrongPassword') }
    }
    return { success: false, message: t('loginFail') }
  }
}

function logout() {
  auth?.signOut().catch(() => {})
  userId.value = ''
  safeRemove(LS.FB_USER_ID)
}

export function useFirebase() {
  return {
    userId,
    syncToCloud,
    flushDataToCloud,
    debouncedSync,
    register,
    login,
    logout,
    pullAndMerge,
    initFirebase,
  }
}
