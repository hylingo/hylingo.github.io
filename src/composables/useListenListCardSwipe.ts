import { ref, computed } from 'vue'
import { isInQuizQueue, addToQuizQueue, quizQueueTick } from '@/learning'

/** 左滑露出的「加入测验」区宽度（px），与模板 `w-[100px]` 一致 */
export const LIST_CARD_QUIZ_ACTION_PX = 100

const HORIZONTAL_BIAS = 1.35

/**
 * 听列表卡片：左滑露出加入测验、点击卡片朗读（排除横向拖拽误触）
 */
export function useListenListCardSwipe(
  getCat: () => string,
  getId: () => number,
  onSpeak: () => void,
) {
  const offsetPx = ref(0)
  const dragging = ref(false)
  let touchStartX = 0
  let touchStartY = 0
  let touchStartOffset = 0
  let hadHorizontalDrag = false
  let activePointerId: number | null = null
  let dragAxis: 'x' | 'y' | null = null

  const maxOffset = -LIST_CARD_QUIZ_ACTION_PX

  function onWindowPointerMove(e: PointerEvent) {
    if (!dragging.value || activePointerId !== e.pointerId) return
    const dx = e.clientX - touchStartX
    const dy = e.clientY - touchStartY
    if (!dragAxis && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) {
      dragAxis = Math.abs(dx) * HORIZONTAL_BIAS >= Math.abs(dy) ? 'x' : 'y'
    }
    if (dragAxis === 'x') {
      e.preventDefault()
      if (Math.abs(dx) > 10) hadHorizontalDrag = true
      let next = touchStartOffset + dx
      if (next > 0) next = 0
      if (next < maxOffset) next = maxOffset
      offsetPx.value = next
    }
  }

  function detachWindowPointerListeners() {
    window.removeEventListener('pointermove', onWindowPointerMove)
    window.removeEventListener('pointerup', onWindowPointerEnd)
    window.removeEventListener('pointercancel', onWindowPointerEnd)
  }

  function onWindowPointerEnd(e: PointerEvent) {
    if (!dragging.value || activePointerId !== e.pointerId) return
    dragging.value = false
    activePointerId = null
    detachWindowPointerListeners()
    if (offsetPx.value < -40) {
      offsetPx.value = maxOffset
    } else {
      offsetPx.value = 0
    }
  }

  const inQueue = computed(() => {
    quizQueueTick.value
    return isInQuizQueue(getCat(), getId())
  })

  function onAddQuiz() {
    addToQuizQueue(getCat(), getId())
    offsetPx.value = 0
  }

  function onPointerDown(e: PointerEvent) {
    if (e.pointerType === 'mouse' && e.button !== 0) return
    dragging.value = true
    hadHorizontalDrag = false
    dragAxis = null
    activePointerId = e.pointerId
    touchStartX = e.clientX
    touchStartY = e.clientY
    touchStartOffset = offsetPx.value
    const el = e.currentTarget
    if (el instanceof HTMLElement) {
      try {
        el.setPointerCapture(e.pointerId)
      } catch {
        /* ignore */
      }
    }
    window.addEventListener('pointermove', onWindowPointerMove, { passive: false })
    window.addEventListener('pointerup', onWindowPointerEnd)
    window.addEventListener('pointercancel', onWindowPointerEnd)
  }

  function onCardClick() {
    if (hadHorizontalDrag) {
      hadHorizontalDrag = false
      return
    }
    if (offsetPx.value < -20) {
      offsetPx.value = 0
      return
    }
    onSpeak()
  }

  const cardTransform = computed(() => ({ transform: `translateX(${offsetPx.value}px)` }))

  const cardTransitionClass = computed(() => {
    if (dragging.value) return ''
    return 'transition-transform duration-200 ease-out'
  })

  return {
    offsetPx,
    dragging,
    onPointerDown,
    onCardClick,
    onAddQuiz,
    inQueue,
    cardTransform,
    cardTransitionClass,
  }
}
