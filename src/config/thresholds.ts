/**
 * 产品侧可调阈值集中配置（改数字主要改这里即可）。
 */

/** 统计「近 N 天」滚动窗口：学习状态卡与周图共用 */
const STATS_ROLLING_DAYS = 7

/** 「我」页学习状态卡片：懒惰 / 还不错 / 厉害 / 刷题过猛 */
export const studyStatus = {
  /** 从首次有统计日期起满 N 天，才开始显示上述评定（未满则提示「满 N 天起…」） */
  minHistoryDays: 3,
  /** 滚动窗口天数 */
  rollingDays: STATS_ROLLING_DAYS,
  /** 窗口内日均练习次数（练习+测验）&lt; 该值 → 懒惰 */
  dailyAvgLazyBelow: 20,
  /** &lt; 该值 → 还不错 */
  dailyAvgOkBelow: 50,
  /** &lt; 该值 → 厉害；否则 → 刷题过猛 */
  dailyAvgGoodBelow: 100,
} as const

/** 最近 N 天学习图表（柱状比例尺下限） */
export const weeklyChart = {
  days: STATS_ROLLING_DAYS,
  practiceScaleMin: 50,
  listenScaleMin: 30,
} as const

/** 练页：「新词」每批抽题数量 */
export const quiz = {
  newBatchSize: 20,
} as const

/** 听列表分页 */
export const list = {
  pageSize: 50,
} as const

/** 易错词列表：累计错次门槛与展示条数（wrongTitle 文案用 {n} 占位，与 topN 一致） */
export const wrongWords = {
  minMissCount: 7,
  topN: 20,
} as const

/** 练习点「认识」后推迟复习的天数 */
export const practice = {
  knownDelayDays: 1,
} as const

/** 写入 Firebase 前的防抖间隔 */
export const cloudSync = {
  debounceMs: 2000,
} as const
