/**
 * 文章偏好状态：模块级单例。
 *
 * 列表/详情视图都可能读写这些（列表读 voice 决定能否打开男声选项；详情写所有几项），
 * 用模块单例避免在多处 ref 之间手动同步。
 *
 * 持久化按 studyLang 分桶（jp_pref_show_zh / en_pref_show_zh ...），切语言时重读。
 */
import { ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { readArticlePrefRaw, writeArticlePrefRaw } from '@/learning/learnStorage'

type BoolPref = 'mode' | 'show_zh' | 'show_reading'

function readBool(id: BoolPref, defaultVal: boolean): boolean {
  const v = readArticlePrefRaw(useAppStore().studyLang, id)
  if (v == null) return defaultVal
  return v === '1' || v === 'true'
}

function readVoiceMale(): boolean {
  return readArticlePrefRaw(useAppStore().studyLang, 'voice') === 'male'
}

// ---- 单例 state ----
const singleMode = ref(false)
const showTranslation = ref(true)
const showReading = ref(true)
const articleVoiceMale = ref(false)

let inited = false

function initFromCurrentLang() {
  singleMode.value = readBool('mode', false)
  showTranslation.value = readBool('show_zh', true)
  showReading.value = readBool('show_reading', true)
  articleVoiceMale.value = readVoiceMale()
}

function bindWatchersOnce() {
  if (inited) return
  inited = true
  initFromCurrentLang()

  const store = useAppStore()
  // 写回 LS
  watch(singleMode, (v) => writeArticlePrefRaw(store.studyLang, 'mode', v ? '1' : '0'))
  watch(showTranslation, (v) => writeArticlePrefRaw(store.studyLang, 'show_zh', v ? '1' : '0'))
  watch(showReading, (v) => writeArticlePrefRaw(store.studyLang, 'show_reading', v ? '1' : '0'))
  watch(articleVoiceMale, (isMale) =>
    writeArticlePrefRaw(store.studyLang, 'voice', isMale ? 'male' : 'female'),
  )

  // 切学习语言：重读偏好
  watch(() => store.studyLang, () => initFromCurrentLang())
}

export function useArticlePrefs() {
  bindWatchersOnce()
  return {
    singleMode,
    showTranslation,
    showReading,
    articleVoiceMale,
  }
}
