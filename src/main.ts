import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import './style.css'
// 主 bundle 同步引入 firebase，避免进"我的"页时现场拉 500KB 异步 chunk
import '@/composables/useFirebase'

const app = createApp(App)
app.use(createPinia())
app.use(router)
// 等首次路由解析完成再挂载，避免 store 在 route 未就绪时被读取
router.isReady().then(() => app.mount('#app'))
