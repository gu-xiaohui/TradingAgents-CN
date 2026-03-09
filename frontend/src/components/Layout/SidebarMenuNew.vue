<template>
  <nav class="h-full py-4 overflow-y-auto">
    <div class="space-y-1 px-3">
      <template v-for="item in menuItems" :key="item.path">
        <!-- 有子菜单 -->
        <div v-if="item.children" class="mb-2">
          <button
            @click="toggleSubmenu(item.path)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5 transition-colors"
            :class="{ 'text-[#F8FAFC] bg-white/5': isSubmenuOpen(item.path) }"
          >
            <div class="flex items-center gap-3">
              <component :is="item.icon" class="w-5 h-5" />
              <span v-show="!collapsed" class="text-sm font-medium">{{ item.title }}</span>
            </div>
            <svg 
              v-show="!collapsed"
              class="w-4 h-4 transition-transform" 
              :class="{ 'rotate-180': isSubmenuOpen(item.path) }"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <!-- 子菜单 -->
          <div v-show="!collapsed && isSubmenuOpen(item.path)" class="mt-1 ml-4 space-y-1">
            <button
              v-for="child in item.children"
              :key="child.path"
              @click="navigate(child.path)"
              class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors"
              :class="isActive(child.path) 
                ? 'text-[#22C55E] bg-[#22C55E]/10' 
                : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="isActive(child.path) ? 'bg-[#22C55E]' : 'bg-[#64748B]'"></span>
              {{ child.title }}
            </button>
          </div>
        </div>
        
        <!-- 无子菜单 -->
        <button
          v-else
          @click="navigate(item.path)"
          class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors"
          :class="isActive(item.path) 
            ? 'text-[#22C55E] bg-[#22C55E]/10' 
            : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-white/5'"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span v-show="!collapsed" class="text-sm font-medium">{{ item.title }}</span>
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

// SVG 图标组件
const IconDashboard = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
])

const IconBook = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const IconChart = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const IconList = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01' })
])

const IconSearch = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
])

const IconStar = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' })
])

const IconWallet = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z' })
])

const IconSettings = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
])

const IconInfo = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const IconDocument = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
])

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

const collapsed = computed(() => appStore.sidebarCollapsed)

// 菜单配置
const menuItems = [
  { path: '/new/dashboard', title: '仪表板', icon: IconDashboard },
  { path: '/new/learning', title: '学习中心', icon: IconBook },
  {
    path: '/analysis',
    title: '股票分析',
    icon: IconChart,
    children: [
      { path: '/new/analysis', title: '单股分析' },
      { path: '/analysis/batch', title: '批量分析' },
      { path: '/reports', title: '分析报告' },
    ]
  },
  { path: '/new/tasks', title: '任务中心', icon: IconList },
  { path: '/new/screening', title: '股票筛选', icon: IconSearch },
  { path: '/favorites', title: '我的自选股', icon: IconStar },
  { path: '/paper', title: '模拟交易', icon: IconWallet },
  {
    path: '/settings',
    title: '设置',
    icon: IconSettings,
    children: [
      { path: '/new/settings', title: '通用设置' },
      { path: '/settings/config', title: '配置管理' },
      { path: '/settings/database', title: '数据库管理' },
      { path: '/settings/logs', title: '操作日志' },
    ]
  },
  { path: '/about', title: '关于', icon: IconInfo },
]

// 展开的子菜单
const openSubmenus = ref<string[]>(['/analysis', '/settings'])

const toggleSubmenu = (path: string) => {
  const index = openSubmenus.value.indexOf(path)
  if (index > -1) {
    openSubmenus.value.splice(index, 1)
  } else {
    openSubmenus.value.push(path)
  }
}

const isSubmenuOpen = (path: string) => openSubmenus.value.includes(path)

const isActive = (path: string) => {
  if (path === '/dashboard/new' && route.path === '/') return true
  return route.path === path || route.path.startsWith(path + '/')
}

const navigate = (path: string) => {
  router.push(path)
}
</script>
