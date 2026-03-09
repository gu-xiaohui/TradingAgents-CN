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
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
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
            <!-- 展开图标 - Heroicons outline -->
            <svg v-if="collapsed" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
            <!-- 收起图标 - Heroicons outline -->
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75 4.5 4.5m0 0 5.25 5.25M4.5 4.5v6m0 0h6m4.5 4.5 5.25-5.25m0 0-5.25 5.25M19.5 19.5v-6m0 0h-6" />
            </svg>
          </button>
          
          <!-- 面包屑 -->
          <nav class="flex items-center gap-2 text-sm">
            <svg class="w-4 h-4 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            <span class="text-[var(--text-muted)]">首页</span>
            <span v-if="currentTitle" class="text-[var(--text-muted)]">/</span>
            <span v-if="currentTitle" class="text-[var(--text-primary)]">{{ currentTitle }}</span>
          </nav>
        </div>

        <div class="flex items-center gap-3">
          <!-- 主题切换 -->
          <ThemeSwitcher />
          
          <!-- 通知 - Heroicons outline -->
          <button class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors relative">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
            </svg>
            <span class="absolute top-1 right-1 w-2 h-2 bg-[#EF4444] rounded-full"></span>
          </button>

          <!-- 退出 - Heroicons outline -->
          <button @click="handleLogout" class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[#EF4444] transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
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
        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
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
