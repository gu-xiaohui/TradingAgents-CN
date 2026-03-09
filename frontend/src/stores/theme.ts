import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export type ThemeMode = 'light' | 'dark' | 'system'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref<ThemeMode>(getStoredTheme())
  
  // 获取存储的主题
  function getStoredTheme(): ThemeMode {
    const stored = localStorage.getItem('theme')
    if (stored === 'light' || stored === 'dark' || stored === 'system') {
      return stored
    }
    return 'system'
  }
  
  // 获取实际主题（解析 system）
  function getActualTheme(): 'light' | 'dark' {
    if (theme.value === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return theme.value
  }
  
  // 应用主题
  function applyTheme() {
    const actualTheme = getActualTheme()
    if (actualTheme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }
  
  // 设置主题
  function setTheme(newTheme: ThemeMode) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }
  
  // 监听系统主题变化
  function watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', () => {
      if (theme.value === 'system') {
        applyTheme()
      }
    })
  }
  
  // 初始化
  watch(theme, () => {
    applyTheme()
  }, { immediate: true })
  
  watchSystemTheme()
  
  return {
    theme,
    setTheme,
    getActualTheme,
    applyTheme,
  }
})
