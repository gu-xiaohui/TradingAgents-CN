<template>
  <nav class="h-full py-4 overflow-y-auto">
    <div class="space-y-1 px-3">
      <template v-for="item in menuItems" :key="item.path">
        <!-- 有子菜单 -->
        <div v-if="item.children" class="mb-2">
          <button
            @click="toggleSubmenu(item.path)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5 transition-colors"
            :class="{ 'text-[var(--text-primary)] bg-white/5': isSubmenuOpen(item.path) }"
          >
            <div class="flex items-center gap-3">
              <component :is="item.icon" />
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
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="isActive(child.path) ? 'bg-[#22C55E]' : 'bg-[var(--text-muted)]'"></span>
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
            : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'"
        >
          <component :is="item.icon" />
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

// 统一的图标样式 - Heroicons outline 风格
const iconClass = 'w-5 h-5'
const iconAttrs = { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '1.5', class: iconClass }

// SVG 图标组件 - 全部使用 Heroicons outline 风格
const IconDashboard = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'm2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25' })
])

const IconBook = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25' })
])

const IconChart = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z' })
])

const IconList = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z' })
])

const IconSearch = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'm21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z' })
])

const IconStar = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z' })
])

const IconWallet = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M21 12a2.25 2.25 0 0 0-2.25-2.25H15a3 3 0 1 1-6 0H5.25A2.25 2.25 0 0 0 3 12m18 0v6a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 9m18 0V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v3' })
])

const IconSettings = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z' })
])

const IconSync = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99' })
])

const IconRankings = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z' })
])

const IconInfo = () => h('svg', iconAttrs, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'm11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z' })
])

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

const collapsed = computed(() => appStore.sidebarCollapsed)

// 菜单配置
const menuItems = [
  { path: '/dashboard', title: '仪表板', icon: IconDashboard },
  { path: '/sync', title: '数据同步', icon: IconSync },
  { path: '/rankings', title: '实时行情榜', icon: IconRankings },
  { path: '/learning', title: '学习中心', icon: IconBook },
  {
    path: '/analysis',
    title: '股票分析',
    icon: IconChart,
    children: [
      { path: '/analysis', title: '单股分析' },
      { path: '/reports', title: '分析报告' },
    ]
  },
  { path: '/tasks', title: '任务中心', icon: IconList },
  { path: '/screening', title: '股票筛选', icon: IconSearch },
  { path: '/favorites', title: '我的自选股', icon: IconStar },
  { path: '/paper', title: '模拟交易', icon: IconWallet },
  {
    path: '/settings',
    title: '设置',
    icon: IconSettings,
    children: [
      { path: '/settings', title: '通用设置' },
      { path: '/settings/config', title: '配置管理' },
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
  // 精确匹配或前缀匹配（但避免 / 匹配所有）
  if (route.path === path) return true
  if (path !== '/' && route.path.startsWith(path + '/')) return true
  return false
}

const navigate = (path: string) => {
  router.push(path)
}
</script>
