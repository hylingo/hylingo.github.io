export { makeItemKey, parseItemKey } from './itemKey'
export {
  milestoneStateTick,
  recordStudy,
  markMastered,
  unmarkMastered,
  hasMasteryQuizPassed,
  getMasteryQuizPassedMap,
  isItemMastered,
  srsIntervalDays,
  // 旧 API（已废弃，仅作为兼容 shim 保留）
  markPracticeAnswerKnown,
  markPracticeAnswerUnknown,
  hasPracticeRecognized,
} from './milestones'
export {
  starredTick,
  isStarred,
  toggleStar,
  getStarredMap,
  getStarredCount,
} from './starred'
