import { describe, expect, it } from 'vitest'
import { srsIntervalDays } from './milestones'

describe('srsIntervalDays', () => {
  it('returns 0 for zero or negative count', () => {
    expect(srsIntervalDays(0)).toBe(0)
    expect(srsIntervalDays(-3)).toBe(0)
  })

  it('first study (count=1) → 1 day', () => {
    expect(srsIntervalDays(1)).toBe(1)
  })

  it('follows the documented schedule for early counts', () => {
    // SRS_INTERVALS = [0, 1, 2, 4, 7, 14, 30, 60, 120, 240]
    expect(srsIntervalDays(2)).toBe(2)
    expect(srsIntervalDays(3)).toBe(4)
    expect(srsIntervalDays(4)).toBe(7)
    expect(srsIntervalDays(5)).toBe(14)
  })

  it('caps at the last interval (240) for counts beyond the table', () => {
    expect(srsIntervalDays(9)).toBe(240)
    expect(srsIntervalDays(10)).toBe(240)
    expect(srsIntervalDays(100)).toBe(240)
  })

  it('is monotonically non-decreasing', () => {
    let prev = srsIntervalDays(1)
    for (let i = 2; i < 20; i++) {
      const cur = srsIntervalDays(i)
      expect(cur).toBeGreaterThanOrEqual(prev)
      prev = cur
    }
  })
})
