<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] transition-colors duration-300">
    <!-- 侧边栏 -->
    <aside
      class="fixed top-0 left-0 h-full bg-[var(--bg-secondary)] border-r border-[var(--border-color)] transition-all duration-300 z-50 flex flex-col"
      :class="collapsed ? 'w-16' : 'w-64'"
    >
      <!-- Logo -->
      <div class="h-16 flex items-center px-4 border-b border-[var(--border-color)]">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <span v-show="!collapsed" class="text-[var(--text-primary)] font-semibold text-sm whitespace-nowrap">
            TradingAgents
          </span>
        </div>
      </div>

      <!-- 菜单 -->
      <SidebarMenuNew />

      <!-- 用户信息 -->
      <div class="p-3 border-t border-[var(--border-color)]">
        <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center text-white text-sm font-medium">
            {{ userInitial }}
          </div>
          <div v-show="!collapsed" class="flex-1 min-w-0">
            <p class="text-sm text-[var(--text-primary)] truncate">{{ authStore.user?.username || '用户' }}</p>
            <p class="text-xs text-[var(--text-muted)] truncate">{{ authStore.user?.email || '' }}</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- 移动端遮罩 -->
    <div
      v-if="isMobile && !collapsed"
      class="fixed inset-0 bg-black/50 z-40"
      @click="appStore.setSidebarCollapsed(true)"
    />

    <!-- 主内容区 -->
    <div class="transition-all duration-300" :class="collapsed ? 'ml-16' : 'ml-64'">
      <!-- 顶部栏 -->
      <header class="h-16 bg-[var(--bg-secondary)] border-b border-[var(--border-color)] flex items-center justify-between px-6 sticky top-0 z-30">
        <div class="flex items-center gap-4">
          <button @click="appStore.toggleSidebar()" class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
            <!-- 展开图标 -->
            <svg v-if="collapsed" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <!-- 收起图标 -->
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
          
          <!-- 面包屑 -->
          <nav class="flex items-center gap-2 text-sm">
            <svg class="w-4 h-4 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span class="text-[var(--text-muted)]">首页</span>
            <span v-if="currentTitle" class="text-[var(--text-muted)]">/</span>
            <span v-if="currentTitle" class="text-[var(--text-primary)]">{{ currentTitle }}</span>
          </nav>
        </div>

        <div class="flex items-center gap-3">
          <!-- 主题切换 -->
          <ThemeSwitcher />
          
          <!-- 通知 -->
          <button class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors relative">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span class="absolute top-1 right-1 w-2 h-2 bg-[#EF4444] rounded-full"></span>
          </button>

          <!-- 退出 -->
          <button @click="handleLogout" class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[#EF4444] transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="p-6">
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </router-view>
      </main>

      <!-- 页脚 -->
      <footer class="h-12 border-t border-[var(--border-color)] flex items-center justify-center text-xs text-[var(--text-muted)]">
        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        TradingAgents-CN v1.0.0-preview · Made with AI
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import SidebarMenuNew from '@/components/Layout/SidebarMenuNew.vue'
import ThemeSwitcher from '@/components/ThemeSwitcher.vue'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const collapsed = computed(() => appStore.sidebarCollapsed)
const isMobile = computed(() => window.innerWidth < 768)

const currentTitle = computed(() => {
  return (route.meta?.title as string) || ''
})

const userInitial = computed(() => {
  const username = authStore.user?.username || 'U'
  return username.charAt(0).toUpperCase()
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
