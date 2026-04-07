/**
 * 极简全局 toast 队列。
 * - 模块级 ref，跨组件共享一个队列
 * - 只用于"用户必须知道"的失败/恢复提示，不用于成功 confirm
 * - 不依赖任何 UI 库
 */
import { ref } from 'vue'

export type ToastKind = 'error' | 'info'

export interface Toast {
  id: number
  kind: ToastKind
  message: string
  /** 毫秒，0 表示不自动消失（带 action 时建议 0） */
  duration: number
  actionLabel?: string
  onAction?: () => void
}

const toasts = ref<Toast[]>([])
let nextId = 1

function push(t: Omit<Toast, 'id'>): number {
  const id = nextId++
  toasts.value.push({ ...t, id })
  if (t.duration > 0) {
    setTimeout(() => dismiss(id), t.duration)
  }
  return id
}

export function dismiss(id: number): void {
  toasts.value = toasts.value.filter((t) => t.id !== id)
}

export function showError(
  message: string,
  opts?: { actionLabel?: string; onAction?: () => void; duration?: number },
): number {
  return push({
    kind: 'error',
    message,
    duration: opts?.duration ?? (opts?.onAction ? 0 : 5000),
    actionLabel: opts?.actionLabel,
    onAction: opts?.onAction,
  })
}

export function showInfo(message: string, duration = 3000): number {
  return push({ kind: 'info', message, duration })
}

export function useToasts() {
  return { toasts, dismiss }
}
