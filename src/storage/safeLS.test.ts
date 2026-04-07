import { describe, expect, it, beforeEach } from 'vitest'
import {
  safeGet,
  safeSet,
  safeRemove,
  safeGetJSON,
  safeSetJSON,
  safeGetNumber,
} from './safeLS'

describe('safeLS', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  describe('safeGet / safeSet / safeRemove', () => {
    it('round-trips a string value', () => {
      expect(safeSet('k', 'hello')).toBe(true)
      expect(safeGet('k')).toBe('hello')
    })

    it('returns null for missing key', () => {
      expect(safeGet('missing')).toBeNull()
    })

    it('safeRemove deletes the key', () => {
      safeSet('k', 'v')
      safeRemove('k')
      expect(safeGet('k')).toBeNull()
    })

    it('safeRemove on missing key does not throw', () => {
      expect(() => safeRemove('nope')).not.toThrow()
    })
  })

  describe('safeGetJSON / safeSetJSON', () => {
    it('round-trips a JSON object', () => {
      safeSetJSON('obj', { a: 1, b: [2, 3] })
      expect(safeGetJSON('obj', null)).toEqual({ a: 1, b: [2, 3] })
    })

    it('returns fallback for missing key', () => {
      expect(safeGetJSON('missing', { default: true })).toEqual({ default: true })
    })

    it('returns fallback for malformed JSON', () => {
      safeSet('bad', '{not json')
      expect(safeGetJSON('bad', [])).toEqual([])
    })

    it('round-trips primitive values', () => {
      safeSetJSON('num', 42)
      expect(safeGetJSON('num', 0)).toBe(42)
    })
  })

  describe('safeGetNumber', () => {
    it('parses stored numeric strings', () => {
      safeSet('n', '123')
      expect(safeGetNumber('n', 0)).toBe(123)
    })

    it('returns fallback for missing key', () => {
      expect(safeGetNumber('missing', 7)).toBe(7)
    })

    it('returns fallback for non-numeric value', () => {
      safeSet('n', 'abc')
      expect(safeGetNumber('n', 99)).toBe(99)
    })
  })
})
