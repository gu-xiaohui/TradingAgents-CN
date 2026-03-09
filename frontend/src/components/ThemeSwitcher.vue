<template>
  <div class="relative">
    <button
      @click="toggleMenu"
      class="p-2 rounded-lg hover:bg-white/5 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors"
    >
      <!-- 亮色图标 -->
      <svg v-if="actualTheme === 'light'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
      <!-- 深色图标 -->
      <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      </svg>
    </button>
    
    <!-- 下拉菜单 -->
    <div
      v-if="isOpen"
      class="absolute right-0 top-full mt-2 w-40 bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl shadow-lg overflow-hidden z-50"
    >
      <button
        v-for="option in options"
        :key="option.value"
        @click="selectTheme(option.value)"
        class="w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors"
        :class="themeStore.theme === option.value 
          ? 'bg-[#22C55E]/10 text-[#22C55E]' 
          : 'text-[var(--text-secondary)] hover:bg-white/5 hover:text-[var(--text-primary)]'"
      >
        <component :is="option.icon" />
        <span>{{ option.label }}</span>
        <svg v-if="themeStore.theme === option.value" class="w-4 h-4 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, h } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
const isOpen = ref(false)

const actualTheme = computed(() => themeStore.getActualTheme())

// 图标组件
const IconLight = () => h('svg', { class: 'w-4 h-4', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' })
])

const IconDark = () => h('svg', { class: 'w-4 h-4', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z' })
])

const IconSystem = () => h('svg', { class: 'w-4 h-4', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
])

const options = [
  { value: 'light' as const, label: '亮色', icon: IconLight },
  { value: 'dark' as const, label: '深色', icon: IconDark },
  { value: 'system' as const, label: '跟随系统', icon: IconSystem },
]

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const selectTheme = (value: 'light' | 'dark' | 'system') => {
  themeStore.setTheme(value)
  isOpen.value = false
}

// 点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.theme-switcher')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
