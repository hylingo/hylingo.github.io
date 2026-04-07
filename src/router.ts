import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { safeGet, safeSet } from '@/storage/safeLS'
import { LS } from '@/storage/keys'

// 占位组件：实际渲染由 App.vue 根据 store 派生状态控制
const Empty = { render: () => null }

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: () => {
      const lang = safeGet(LS.STUDY_LANG) || 'ja'
      const last = safeGet(LS.LAST_PATH)
      if (last && /^\/(ja|en)\//.test(last)) return last
      return `/${lang}/articles`
    },
  },
  {
    path: '/:lang(ja|en)/stats',
    name: 'stats',
    component: Empty,
  },
  {
    path: '/:lang(ja|en)/:cat/practice/:articleId',
    name: 'practice-article',
    component: Empty,
  },
  {
    path: '/:lang(ja|en)/:cat/practice',
    name: 'practice',
    component: Empty,
  },
  {
    path: '/:lang(ja|en)/:cat',
    name: 'list',
    component: Empty,
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export const router = createRouter({
  history: createWebHistory('/'),
  routes,
  scrollBehavior(_to, _from, saved) {
    return saved || { top: 0 }
  },
})

// 记住最后访问位置，便于 / 重定向恢复
router.afterEach((to) => {
  if (to.path !== '/' && to.name) {
    safeSet(LS.LAST_PATH, to.fullPath)
  }
})
