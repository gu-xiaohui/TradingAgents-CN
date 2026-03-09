<template>
  <div class="min-h-screen bg-primary-dark flex items-center justify-center p-4">
    <!-- Background effects -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-success/10 to-transparent rounded-full blur-3xl" />
      <div class="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-cta/10 to-transparent rounded-full blur-3xl" />
    </div>
    
    <!-- Login card -->
    <div class="w-full max-w-md relative">
      <!-- Logo & Title -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-success to-cta mb-4">
          <!-- Chart icon -->
          <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-text-primary">TradingAgents-CN</h1>
        <p class="text-text-muted mt-2">AI 多智能体股票分析系统</p>
      </div>
      
      <!-- Login form -->
      <TCard variant="glass" padding="lg">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <TInput
            v-model="username"
            label="用户名"
            placeholder="请输入用户名"
            :icon-left="UserIcon"
            required
          />
          
          <TInput
            v-model="password"
            label="密码"
            type="password"
            placeholder="请输入密码"
            :icon-left="LockIcon"
            required
          />
          
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 text-text-secondary cursor-pointer">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="w-4 h-4 rounded border-border bg-primary-dark text-success focus:ring-success"
              />
              记住我
            </label>
            <a href="#" class="text-success hover:text-success/80 transition-colors">
              忘记密码？
            </a>
          </div>
          
          <TButton
            type="submit"
            variant="primary"
            size="lg"
            block
            :loading="loading"
          >
            登录
          </TButton>
        </form>
        
        <!-- Divider -->
        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-border" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-4 bg-primary-dark text-text-muted">或</span>
          </div>
        </div>
        
        <!-- Social login -->
        <div class="grid grid-cols-2 gap-3">
          <TButton variant="secondary" size="sm">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.879V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.989C18.343 21.129 22 16.99 22 12c0-5.523-4.477-10-10-10z" />
            </svg>
            微信登录
          </TButton>
          <TButton variant="secondary" size="sm">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
            Twitter 登录
          </TButton>
        </div>
      </TCard>
      
      <!-- Footer -->
      <p class="text-center text-text-muted text-sm mt-6">
        还没有账号？
        <a href="#" class="text-success hover:text-success/80 transition-colors">
          立即注册
        </a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TCard from '@/components/base/TCard.vue'
import TInput from '@/components/base/TInput.vue'
import TButton from '@/components/base/TButton.vue'

// Icons
const UserIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>`
}
const LockIcon = {
  template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>`
}

const router = useRouter()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  
  // Simulate login
  setTimeout(() => {
    loading.value = false
    router.push('/dashboard')
  }, 1500)
}
</script>
