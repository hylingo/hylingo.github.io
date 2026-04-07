import { describe, expect, it } from 'vitest'
import { coerceListenCount, mergeListenCountMaps } from './listenCount'

describe('coerceListenCount', () => {
  it('passes through positive integers', () => {
    expect(coerceListenCount(5)).toBe(5)
    expect(coerceListenCount(0)).toBe(0)
  })

  it('floors fractional numbers', () => {
    expect(coerceListenCount(3.7)).toBe(3)
  })

  it('clamps negative numbers to 0', () => {
    expect(coerceListenCount(-1)).toBe(0)
    expect(coerceListenCount(-100)).toBe(0)
  })

  it('parses numeric strings', () => {
    expect(coerceListenCount('42')).toBe(42)
  })

  it('returns 0 for non-numeric strings', () => {
    expect(coerceListenCount('abc')).toBe(0)
    expect(coerceListenCount('')).toBe(0)
  })

  it('returns 0 for null / undefined / NaN', () => {
    expect(coerceListenCount(null)).toBe(0)
    expect(coerceListenCount(undefined)).toBe(0)
    expect(coerceListenCount(NaN)).toBe(0)
  })

  it('caps at 999_999 to prevent overflow', () => {
    expect(coerceListenCount(10_000_000)).toBe(999_999)
  })
})

describe('mergeListenCountMaps', () => {
  it('takes max per key (not sum)', () => {
    const local = { 'nouns:1': 3, 'nouns:2': 5 }
    const cloud = { 'nouns:1': 7, 'nouns:2': 2 }
    expect(mergeListenCountMaps(local, cloud)).toEqual({ 'nouns:1': 7, 'nouns:2': 5 })
  })

  it('keeps keys present in only one side', () => {
    const local = { 'nouns:1': 1 }
    const cloud = { 'nouns:2': 2 }
    expect(mergeListenCountMaps(local, cloud)).toEqual({ 'nouns:1': 1, 'nouns:2': 2 })
  })

  it('coerces dirty values from both sides', () => {
    const local = { 'k': '5' as unknown as number }
    const cloud = { 'k': -10 as unknown as number }
    expect(mergeListenCountMaps(local, cloud)).toEqual({ k: 5 })
  })

  it('returns empty object for two empty inputs', () => {
    expect(mergeListenCountMaps({}, {})).toEqual({})
  })
})
