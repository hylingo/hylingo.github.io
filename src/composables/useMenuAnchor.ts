import { ref, watch, nextTick, onUnmounted, type Ref } from 'vue'

/** 下拉打开时根据触发按钮计算 fixed 菜单位置，滚动/缩放时跟随 */
export function useMenuAnchor(
  open: Ref<boolean>,
  triggerRef: Ref<HTMLElement | null>,
  options?: { minWidth?: number; maxWidth?: number },
) {
  const menuStyle = ref<Record<string, string>>({})
  let cleanup: (() => void) | null = null

  function measure() {
    const el = triggerRef.value
    if (!el) return
    const r = el.getBoundingClientRect()
    const minW = options?.minWidth ?? 0
    const maxW = options?.maxWidth
    const rw = Math.round(r.width)
    let w = Math.max(minW, rw)
    if (maxW != null) w = Math.min(w, maxW)
    const style: Record<string, string> = {
      position: 'fixed',
      top: `${Math.round(r.bottom + 4)}px`,
      left: `${Math.round(r.left)}px`,
      zIndex: '460',
      minWidth: `${w}px`,
    }
    if (maxW != null) style.maxWidth = `${maxW}px`
    menuStyle.value = style
  }

  watch(open, async (v) => {
    cleanup?.()
    cleanup = null
    if (!v) {
      menuStyle.value = {}
      return
    }
    await nextTick()
    measure()
    const onScrollResize = () => measure()
    window.addEventListener('scroll', onScrollResize, true)
    window.addEventListener('resize', onScrollResize)
    cleanup = () => {
      window.removeEventListener('scroll', onScrollResize, true)
      window.removeEventListener('resize', onScrollResize)
    }
  })

  onUnmounted(() => cleanup?.())

  return menuStyle
}
