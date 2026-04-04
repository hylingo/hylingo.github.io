import { onMounted, onUnmounted } from 'vue'

const SWIPE_THRESHOLD = 80

export function useSwipe(onSwipe: (direction: 'left' | 'right') => void) {
  let startX = 0
  let startY = 0

  function handleTouchStart(e: TouchEvent) {
    startX = e.changedTouches[0].screenX
    startY = e.changedTouches[0].screenY
  }

  function handleTouchEnd(e: TouchEvent) {
    const dx = e.changedTouches[0].screenX - startX
    const dy = e.changedTouches[0].screenY - startY
    // Only trigger if horizontal movement exceeds threshold and is greater than vertical
    if (Math.abs(dx) > SWIPE_THRESHOLD && Math.abs(dx) > Math.abs(dy)) {
      onSwipe(dx > 0 ? 'right' : 'left')
    }
  }

  onMounted(() => {
    document.addEventListener('touchstart', handleTouchStart, { passive: true })
    document.addEventListener('touchend', handleTouchEnd, { passive: true })
  })

  onUnmounted(() => {
    document.removeEventListener('touchstart', handleTouchStart)
    document.removeEventListener('touchend', handleTouchEnd)
  })
}
