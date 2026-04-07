/**
 * 集中所有 localStorage key 名称。
 *
 * 改名前请加迁移逻辑（见 src/storage/migrate.ts），否则用户旧数据会丢失。
 *
 * 命名规约（新 key 请遵守）：
 * - 应用范围全局 key：snake_case，如 `study_lang`
 * - 与 firebase 互通的旧 key：保留 `jp_` 前缀（legacy，不能改）
 * - 带变量的 key：用本文件的 builder 函数构造，不要在调用方手拼字符串
 */

// ---- 静态 key（无变量）----
export const LS = {
  /** 学习目标语言：'ja' | 'en' */
  STUDY_LANG: 'study_lang',
  /** 路由最后访问位置（用于 / 智能重定向） */
  LAST_PATH: 'last_path',
  /** 界面语言：'zh' | 'en' | 'ja'（legacy 名 jp_lang） */
  UI_LANG: 'jp_lang',
  /** 主题：dusk | warm | ink（legacy 名带 _v1） */
  THEME: 'app_theme_mode_v1',
  /** Firebase 用户名（legacy 名 jp_user_id） */
  FB_USER_ID: 'jp_user_id',
  /** Firebase 重置标记时间戳（legacy 名 jp_reset_at） */
  FB_RESET_AT: 'jp_reset_at',
  /** 循环播放调试日志（legacy 名带 _v1） */
  LOOP_DEBUG: 'loop_debug_logs_v1',
  /** LS schema 版本（用于将来迁移） */
  SCHEMA_VERSION: 'hylingo_schema_version',
} as const

// ---- 动态 key builder ----

/** 本篇精读练习槽位（按 format 区分：essay / dialogue） */
export const practiceSlotKey = {
  id: (format: string) => `practice_${format}_id`,
  title: (format: string) => `practice_${format}_title`,
  index: (format: string) => `practice_${format}_index`,
}

// 注：learn_* 家族的 key（学习进度桶）由 src/learning/learnStorage.ts
// 自有 builder 函数管理，不在此重复，避免双源。
