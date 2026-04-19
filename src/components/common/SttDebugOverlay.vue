<script setup lang="ts">
import { ref } from 'vue'
import { sttDebugLog, sttDebugVisible, clearSttDebug, formatSttDebug } from '@/utils/sttDebug'
import { safeGet, safeSet, safeRemove } from '@/storage/safeLS'
import { LS } from '@/storage/keys'

const copied = ref(false)
const localSttUrl = ref(safeGet(LS.LOCAL_STT_URL) || '')
const savedHint = ref('')

function saveLocalSttUrl() {
  const v = localSttUrl.value.trim()
  if (v) safeSet(LS.LOCAL_STT_URL, v)
  else safeRemove(LS.LOCAL_STT_URL)
  savedHint.value = '已保存，刷新后生效'
  setTimeout(() => (savedHint.value = ''), 2000)
}

async function copyAll() {
  const text = formatSttDebug()
  try {
    await navigator.clipboard.writeText(text)
    copied.value = true
    setTimeout(() => (copied.value = false), 1200)
  } catch {
    // 兜底：选中 textarea 让用户长按复制
    const ta = document.getElementById('stt-debug-fallback-ta') as HTMLTextAreaElement | null
    if (ta) { ta.value = text; ta.select() }
  }
}
</script>

<template>
  <button class="stt-debug-fab" @click="sttDebugVisible = !sttDebugVisible" title="STT debug">
    🐞<span v-if="sttDebugLog.length" class="badge">{{ sttDebugLog.length }}</span>
  </button>
  <div v-if="sttDebugVisible" class="stt-debug-modal" @click.self="sttDebugVisible = false">
    <div class="stt-debug-card">
      <header>
        <strong>STT Debug</strong>
        <div class="actions">
          <button @click="copyAll">{{ copied ? '已复制' : '复制' }}</button>
          <button @click="clearSttDebug">清空</button>
          <button @click="sttDebugVisible = false">×</button>
        </div>
      </header>
      <div class="local-stt-setting">
        <label>本地 whisper 服务器</label>
        <div class="row-form">
          <input
            v-model="localSttUrl"
            type="text"
            placeholder="http://localhost:8080/inference（留空=用 Web Speech）"
            spellcheck="false"
            autocapitalize="off"
          />
          <button @click="saveLocalSttUrl">保存</button>
        </div>
        <div v-if="savedHint" class="hint">{{ savedHint }}</div>
      </div>
      <div class="log">
        <div v-if="!sttDebugLog.length" class="empty">(暂无日志)</div>
        <div v-for="(e, i) in sttDebugLog" :key="i" class="row">
          <span class="ts">{{ new Date(e.ts).toLocaleTimeString() }}</span>
          <span class="tag" :data-tag="e.tag">[{{ e.tag }}]</span>
          <span class="msg">{{ e.msg }}</span>
        </div>
      </div>
      <textarea id="stt-debug-fallback-ta" class="fallback" readonly></textarea>
    </div>
  </div>
</template>

<style scoped>
.stt-debug-fab {
  position: fixed; right: 12px; bottom: 88px; z-index: 9998;
  width: 44px; height: 44px; border-radius: 50%;
  border: 1px solid rgba(0,0,0,.15); background: #fff8ef;
  font-size: 20px; line-height: 1; cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,.15);
  display: flex; align-items: center; justify-content: center;
  position: fixed;
}
.badge {
  position: absolute; top: -4px; right: -4px;
  min-width: 18px; height: 18px; padding: 0 5px;
  border-radius: 9px; background: #c45a3e; color: #fff;
  font-size: 11px; line-height: 18px; text-align: center;
}
.stt-debug-modal {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,.45);
  display: flex; align-items: flex-end; justify-content: center;
}
.stt-debug-card {
  width: 100%; max-width: 720px; height: 80vh; max-height: 80vh;
  background: #fff; border-radius: 12px 12px 0 0;
  display: flex; flex-direction: column; min-height: 0;
  box-shadow: 0 -4px 20px rgba(0,0,0,.2);
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
header { flex-shrink: 0; }
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; border-bottom: 1px solid #eee;
}
header .actions { display: flex; gap: 6px; }
header button {
  padding: 4px 10px; border: 1px solid #ccc; background: #f7f3ec;
  border-radius: 6px; font-size: 13px; cursor: pointer;
}
.log {
  flex: 1 1 auto; min-height: 0;
  overflow-y: auto; -webkit-overflow-scrolling: touch;
  padding: 8px 12px;
  font: 12px/1.5 ui-monospace, Menlo, Consolas, monospace;
}
.empty { color: #999; padding: 12px; text-align: center; }
.row { padding: 2px 0; word-break: break-all; }
.ts { color: #888; margin-right: 6px; }
.tag { margin-right: 6px; color: #4f8a6f; }
.tag[data-tag="error"] { color: #c45a3e; }
.tag[data-tag="end"] { color: #c49a3c; }
.fallback {
  position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0;
}
.local-stt-setting {
  flex-shrink: 0;
  padding: 10px 14px;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}
.local-stt-setting label {
  display: block; color: #555; margin-bottom: 4px; font-size: 12px;
}
.local-stt-setting .row-form {
  display: flex; gap: 6px;
}
.local-stt-setting input {
  flex: 1; min-width: 0;
  padding: 6px 8px; border: 1px solid #ccc; border-radius: 6px;
  font: 12px ui-monospace, Menlo, monospace;
}
.local-stt-setting button {
  padding: 6px 12px; border: 1px solid #ccc; background: #f7f3ec;
  border-radius: 6px; font-size: 13px; cursor: pointer;
}
.local-stt-setting .hint {
  margin-top: 4px; color: #4f8a6f; font-size: 11px;
}
</style>
