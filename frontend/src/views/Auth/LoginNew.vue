<template>
  <div class="min-h-screen bg-[var(--bg-primary)] flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Background effects -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-[#22C55E]/10 to-transparent rounded-full blur-3xl" />
      <div class="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-[#8B5CF6]/10 to-transparent rounded-full blur-3xl" />
    </div>

    <!-- Login card -->
    <div class="w-full max-w-md relative z-10">
      <!-- Logo & Title -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] mb-4">
          <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">TradingAgents-CN</h1>
        <p class="text-[var(--text-secondary)] mt-2">AI 多智能体股票分析系统</p>
      </div>

      <!-- Login form card -->
      <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-[var(--text-secondary)] mb-2">用户名</label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)]">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                v-model="username"
                type="text"
                placeholder="请输入用户名"
                class="w-full pl-10 pr-4 py-3 bg-[var(--bg-primary)] border border-white/10 rounded-xl text-[var(--text-primary)] placeholder-[#64748B] focus:outline-none focus:border-[#22C55E] focus:ring-1 focus:ring-[#22C55E] transition-all"
                required
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-[var(--text-secondary)] mb-2">密码</label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)]">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                v-model="password"
                type="password"
                placeholder="请输入密码"
                class="w-full pl-10 pr-4 py-3 bg-[var(--bg-primary)] border border-white/10 rounded-xl text-[var(--text-primary)] placeholder-[#64748B] focus:outline-none focus:border-[#22C55E] focus:ring-1 focus:ring-[#22C55E] transition-all"
                required
              />
            </div>
          </div>

          <!-- Remember & Forgot -->
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 text-[var(--text-secondary)] cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 rounded border-white/10 bg-[var(--bg-primary)] text-[#22C55E] focus:ring-[#22C55E]"
              />
              记住我
            </label>
            <a href="#" class="text-[#22C55E] hover:text-[#22C55E]/80 transition-colors">忘记密码？</a>
          </div>

          <!-- Error message -->
          <div v-if="errorMsg" class="text-sm text-[#EF4444] bg-[#EF4444]/10 border border-[#EF4444]/20 rounded-lg p-3">
            {{ errorMsg }}
          </div>

          <!-- Submit button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-[#22C55E] hover:bg-[#22C55E]/90 text-white font-medium rounded-xl transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="loading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span>{{ loading ? '登录中...' : '登录' }}</span>
          </button>
        </form>

        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/10" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-transparent text-[var(--text-muted)]">或</span>
          </div>
        </div>

        <!-- Alternative login -->
        <div class="text-center">
          <p class="text-sm text-[var(--text-muted)]">
            还没有账号？
            <a href="#" class="text-[#22C55E] hover:text-[#22C55E]/80 transition-colors">立即注册</a>
          </p>
        </div>
      </div>

      <!-- Footer -->
      <p class="text-center text-[var(--text-muted)] text-xs mt-6">
        登录即表示您同意我们的
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">服务条款</a>
        和
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">隐私政策</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
    router.push('/new/dashboard')
  } catch (error: any) {
    errorMsg.value = error.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>
