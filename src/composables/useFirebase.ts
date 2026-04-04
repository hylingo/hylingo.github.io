import { ref } from 'vue'
import firebase from 'firebase/compat/app'
import 'firebase/compat/database'
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
import type { StudyLang } from '@/types'

const firebaseConfig = {
  apiKey: "AIzaSyBCZa2CyskF8bM_CU0l2UaT7Wwq25cz30Q",
  authDomain: "jp-learn-e01bd.firebaseapp.com",
  databaseURL: "https://jp-learn-e01bd-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "jp-learn-e01bd",
  storageBucket: "jp-learn-e01bd.firebasestorage.app",
  messagingSenderId: "1055060519096",
  appId: "1:1055060519096:web:ed0421d0a6938186c6ec4d",
}

const userId = ref(localStorage.getItem('jp_user_id') || '')
let db: firebase.database.Database | null = null
let syncTimer: ReturnType<typeof setTimeout> | null = null

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

function mergeStats(a: Record<string, any>, b: Record<string, any>): Record<string, any> {
  const merged: Record<string, any> = {}
  const allDays = new Set([...Object.keys(a), ...Object.keys(b)])
  for (const day of allDays) {
    const da = a[day] || {}
    const db = b[day] || {}
    merged[day] = {
      studied: Math.max(da.studied || 0, db.studied || 0),
      quizzed: Math.max(da.quizzed || 0, db.quizzed || 0),
      correct: Math.max(da.correct || 0, db.correct || 0),
      listened: Math.max(da.listened || 0, db.listened || 0),
      wrong: mergeMaxNumbers(da.wrong || {}, db.wrong || {}),
    }
  }
  return merged
}

function mergeLangBundle(local: LangBundle, cloud: LangBundle): LangBundle {
  return {
    stats: mergeStats((local.stats || {}) as any, (cloud.stats || {}) as any),
    counts: mergeMaxNumbers((local.counts || {}) as any, (cloud.counts || {}) as any),
    delays: mergeLaterReviewDates((local.delays || {}) as any, (cloud.delays || {}) as any),
    listened: mergeListenCountMaps((local.listened || {}) as any, (cloud.listened || {}) as any),
    listenDismissed: mergeDismissed((local.listenDismissed || {}) as any, (cloud.listenDismissed || {}) as any),
    practiceRecognized: mergeDismissed((local.practiceRecognized || {}) as any, (cloud.practiceRecognized || {}) as any),
    masteryQuizPassed: mergeDismissed((local.masteryQuizPassed || {}) as any, (cloud.masteryQuizPassed || {}) as any),
    quizQueue: mergeMaxNumbers((local.quizQueue || {}) as any, (cloud.quizQueue || {}) as any),
    quizFails: mergeMaxNumbers((local.quizFails || {}) as any, (cloud.quizFails || {}) as any),
    quizPhase1: mergeDismissed((local.quizPhase1 || {}) as any, (cloud.quizPhase1 || {}) as any),
  }
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

function buildV2Payload(ja: LangBundle, en: LangBundle, resetAt?: number) {
  const payload: Record<string, unknown> = {
    schemaVersion: 2,
    langs: { ja, en },
  }
  if (resetAt != null && resetAt > 0) payload.resetAt = resetAt
  return payload
}

async function hashPassword(password: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(password + 'jp-learn-salt')
  const hash = await crypto.subtle.digest('SHA-256', data)
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('')
}

function initFirebase() {
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig)
  }
  db = firebase.database()
}

function syncToCloud() {
  if (!userId.value || !db) return
  const { ja, en } = readBothBundlesFromLS()
  if (!langBundleHasAny(ja) && !langBundleHasAny(en)) return
  const resetAt = Number(localStorage.getItem('jp_reset_at') || '0')
  const payload = buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined)
  db.ref('users/' + userId.value + '/data').set(payload)
}

function flushDataToCloud() {
  if (!userId.value || !db) return
  const { ja, en } = readBothBundlesFromLS()
  const resetAt = Date.now()
  const payload = buildV2Payload(ja, en, resetAt)
  db.ref('users/' + userId.value + '/data').set(payload)
  localStorage.setItem('jp_reset_at', String(resetAt))
}

function debouncedSync() {
  if (syncTimer) clearTimeout(syncTimer)
  syncTimer = setTimeout(syncToCloud, cloudSync.debounceMs)
}

/** 将云端 v2 数据合并进本地并写回同结构；非 v2 的学习字段忽略，resetAt 仍从原始节点读取 */
function mergeCloudIntoLocal(cloudRaw: unknown): { uploaded: Record<string, unknown> } {
  const localResetAt = Number(localStorage.getItem('jp_reset_at') || '0')
  const cloudResetAt = rawResetAtMs(cloudRaw)
  const cloudLangs = parseCloudLangs(cloudRaw)

  if (cloudResetAt > localResetAt) {
    writeBothBundlesToLS(cloudLangs.ja, cloudLangs.en)
    localStorage.setItem('jp_reset_at', String(cloudResetAt))
    return { uploaded: buildV2Payload(cloudLangs.ja, cloudLangs.en, cloudResetAt) }
  }

  const localJa = readLangBundle('ja')
  const localEn = readLangBundle('en')
  const mergedJa = mergeLangBundle(localJa, cloudLangs.ja)
  const mergedEn = mergeLangBundle(localEn, cloudLangs.en)
  writeBothBundlesToLS(mergedJa, mergedEn)

  const resetAt =
    cloudResetAt > 0 ? cloudResetAt : Number(localStorage.getItem('jp_reset_at') || '0')
  return {
    uploaded: buildV2Payload(mergedJa, mergedEn, resetAt > 0 ? resetAt : undefined),
  }
}

async function pullAndMerge(): Promise<boolean> {
  if (!userId.value || !db) return false
  try {
    const snap = await db.ref('users/' + userId.value + '/data').once('value')
    if (!snap.exists()) return false
    const cloud = snap.val()
    const { uploaded } = mergeCloudIntoLocal(cloud)
    await db.ref('users/' + userId.value + '/data').set(uploaded)
    return true
  } catch {
    return false
  }
}

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
  if (!db) {
    return { success: false, message: t('loginFail') }
  }

  try {
    const snap = await db.ref('users/' + name + '/profile').once('value')
    if (snap.exists()) {
      return { success: false, message: t('usernameTaken') }
    }

    const hash = await hashPassword(password)
    await db.ref('users/' + name + '/profile').set({ passwordHash: hash })

    const { ja, en } = readBothBundlesFromLS()
    if (langBundleHasAny(ja) || langBundleHasAny(en)) {
      const resetAt = Number(localStorage.getItem('jp_reset_at') || '0')
      await db
        .ref('users/' + name + '/data')
        .set(buildV2Payload(ja, en, resetAt > 0 ? resetAt : undefined))
    }

    userId.value = name
    localStorage.setItem('jp_user_id', name)
    return { success: true, message: t('registerSuccess') }
  } catch {
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
  if (!db) {
    return { success: false, message: t('loginFail') }
  }

  try {
    const snap = await db.ref('users/' + name + '/profile').once('value')
    if (!snap.exists()) {
      return { success: false, message: t('userNotFound') }
    }

    const hash = await hashPassword(password)
    const profile = snap.val()
    if (profile.passwordHash !== hash) {
      return { success: false, message: t('wrongPassword') }
    }

    userId.value = name
    localStorage.setItem('jp_user_id', name)

    const cloudSnap = await db.ref('users/' + name + '/data').once('value')
    if (cloudSnap.exists()) {
      const cloud = cloudSnap.val()
      const { uploaded } = mergeCloudIntoLocal(cloud)
      await db.ref('users/' + name + '/data').set(uploaded)
    }

    return { success: true, message: t('loginFound') }
  } catch {
    return { success: false, message: t('loginFail') }
  }
}

function logout() {
  userId.value = ''
  localStorage.removeItem('jp_user_id')
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
