import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false, minimum: 0.2, easing: 'ease', speed: 500 })

// 路由配置 - 统一使用新布局
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  // 主布局路由
  {
    path: '/',
    component: () => import('@/layouts/BasicLayoutNew.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard/index.vue'), meta: { title: '仪表板' } },
      { path: 'analysis', name: 'Analysis', component: () => import('@/views/Analysis/SingleAnalysis.vue'), meta: { title: '单股分析' } },
      { path: 'screening', name: 'Screening', component: () => import('@/views/Screening/index.vue'), meta: { title: '股票筛选' } },
      { path: 'tasks', name: 'Tasks', component: () => import('@/views/Tasks/TaskCenter.vue'), meta: { title: '任务中心' } },
      { path: 'settings', name: 'Settings', component: () => import('@/views/Settings/index.vue'), meta: { title: '设置' } },
      { path: 'learning', name: 'Learning', component: () => import('@/views/Learning/index.vue'), meta: { title: '学习中心', requiresAuth: false } },
      { path: 'about', name: 'About', component: () => import('@/views/About/index.vue'), meta: { title: '关于', requiresAuth: false } },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/Favorites/index.vue'), meta: { title: '我的自选股' } },
      { path: 'paper', name: 'Paper', component: () => import('@/views/PaperTrading/index.vue'), meta: { title: '模拟交易' } },
      { path: 'reports', name: 'Reports', component: () => import('@/views/Reports/index.vue'), meta: { title: '分析报告' } },
      { path: 'reports/:id', name: 'ReportDetail', component: () => import('@/views/Reports/ReportDetail.vue'), meta: { title: '报告详情' } },
    ]
  },
  // 登录页（独立）
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Auth/Login.vue'),
    meta: { title: '登录', hideInMenu: true }
  },
  // 兼容旧路由重定向
  { path: '/new/dashboard', redirect: '/dashboard' },
  { path: '/new/analysis', redirect: '/analysis' },
  { path: '/new/screening', redirect: '/screening' },
  { path: '/new/tasks', redirect: '/tasks' },
  { path: '/new/settings', redirect: '/settings' },
  { path: '/new/learning', redirect: '/learning' },
  { path: '/new/about', redirect: '/about' },
  { path: '/analysis/single', redirect: '/analysis' },
  { path: '/queue', redirect: '/tasks' },
  { path: '/analysis/history', redirect: '/tasks' },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Error/404.vue'),
    meta: { title: '页面不存在', hideInMenu: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start()
  const authStore = useAuthStore()
  const appStore = useAppStore()

  const title = to.meta.title as string
  if (title) document.title = `${title} - TradingAgents-CN`

  // 检查认证
  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    authStore.setRedirectPath(to.fullPath)
    next('/login')
    return
  }

  // 已登录访问登录页，跳转首页
  if (authStore.isAuthenticated && to.name === 'Login') {
    next('/dashboard')
    return
  }

  appStore.setCurrentRoute(to)
  next()
})

router.afterEach(() => NProgress.done())
router.onError((error) => {
  console.error('路由错误:', error)
  NProgress.done()
  ElMessage.error('页面加载失败')
})

export default router
