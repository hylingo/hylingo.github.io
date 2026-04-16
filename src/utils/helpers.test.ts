import { describe, expect, it } from 'vitest'
import { escHtml, todayKey, formatListenTime } from './helpers'

describe('escHtml', () => {
  it('escapes the standard HTML special chars', () => {
    expect(escHtml('<div class="x">a&b\'c</div>')).toBe(
      '&lt;div class=&quot;x&quot;&gt;a&amp;b&#39;c&lt;/div&gt;',
    )
  })

  it('returns the input unchanged when nothing to escape', () => {
    expect(escHtml('plain text 123')).toBe('plain text 123')
  })

  it('coerces non-strings via String()', () => {
    expect(escHtml(42 as unknown as string)).toBe('42')
  })
})

describe('todayKey', () => {
  it('returns YYYY-MM-DD shape', () => {
    expect(todayKey()).toMatch(/^\d{4}-\d{2}-\d{2}$/)
  })
})

describe('formatListenTime', () => {
  // Simple identity translator for unit-friendly assertions
  const t = (k: string) => k

  it('formats sub-minute as 0min', () => {
    expect(formatListenTime(0, t)).toBe('0min')
    expect(formatListenTime(45, t)).toBe('0min')
    expect(formatListenTime(59.4, t)).toBe('0min')
  })

  it('rounds seconds before formatting', () => {
    expect(formatListenTime(59.6, t)).toBe('1min')
  })

  it('formats minutes (<60) without seconds', () => {
    expect(formatListenTime(60, t)).toBe('1min')
    expect(formatListenTime(75, t)).toBe('1min')
    expect(formatListenTime(3599, t)).toBe('59min')
  })

  it('formats hours and remaining minutes for >=1h', () => {
    expect(formatListenTime(3600, t)).toBe('1hour0min')
    expect(formatListenTime(3660, t)).toBe('1hour1min')
    expect(formatListenTime(7325, t)).toBe('2hour2min')
  })

  it('treats falsy/invalid input as 0min', () => {
    expect(formatListenTime(0, t)).toBe('0min')
    expect(formatListenTime(NaN, t)).toBe('0min')
  })
})
