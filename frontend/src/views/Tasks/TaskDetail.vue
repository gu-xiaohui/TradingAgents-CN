<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="w-16 h-16 border-4 border-[#3B82F6] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-[var(--text-secondary)]">加载任务详情...</p>
      </div>
    </div>

    <!-- 任务内容 -->
    <div v-else-if="task" class="p-6 max-w-4xl mx-auto space-y-6">
      <!-- 头部信息 -->
      <div class="card p-6">
        <div class="flex items-start justify-between gap-4">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#8B5CF6] flex items-center justify-center">
              <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold">{{ task.stock_name || task.stock_code }} 分析任务</h1>
              <div class="flex items-center gap-3 mt-2">
                <span class="px-3 py-1 rounded-lg bg-[#3B82F6]/20 text-[#3B82F6] font-mono text-sm">{{ task.stock_code }}</span>
                <span :class="statusClass" class="px-3 py-1 rounded-lg text-sm font-medium">{{ statusText }}</span>
              </div>
            </div>
          </div>
          <button @click="goBack" class="btn-ghost flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            返回列表
          </button>
        </div>
      </div>

      <!-- 进度展示 -->
      <div v-if="task.status === 'running' || task.status === 'pending'" class="card p-6">
        <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-[#F59E0B]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#F59E0B] animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          分析进行中
        </h2>
        
        <!-- 进度条 -->
        <div class="mb-4">
          <div class="flex justify-between text-sm mb-2">
            <span class="text-[var(--text-secondary)]">分析进度</span>
            <span class="font-medium">{{ progress }}%</span>
          </div>
          <div class="h-3 bg-white/10 rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-[#3B82F6] to-[#8B5CF6] transition-all duration-500 rounded-full"
              :style="{ width: `${progress}%` }"
            ></div>
          </div>
        </div>

        <!-- 当前步骤 -->
        <div class="p-4 rounded-xl bg-[var(--bg-secondary)]">
          <div class="flex items-center gap-3">
            <div class="w-2 h-2 rounded-full bg-[#22C55E] animate-pulse"></div>
            <span class="text-[var(--text-secondary)]">{{ currentStep }}</span>
          </div>
        </div>

        <!-- 预计时间 -->
        <div class="mt-4 flex items-center gap-2 text-sm text-[var(--text-muted)]">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>预计剩余时间：{{ estimatedTime }}</span>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="task.status === 'completed'" class="space-y-6">
        <!-- 关键指标 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="card p-4">
            <div class="text-sm text-[var(--text-muted)] mb-1">投资建议</div>
            <div :class="recommendationClass" class="text-xl font-bold">{{ recommendation }}</div>
          </div>
          <div class="card p-4">
            <div class="text-sm text-[var(--text-muted)] mb-1">置信度</div>
            <div class="text-xl font-bold text-[#3B82F6]">{{ confidence }}%</div>
          </div>
          <div class="card p-4">
            <div class="text-sm text-[var(--text-muted)] mb-1">风险评估</div>
            <div :class="riskClass" class="text-xl font-bold">{{ task.result?.risk_level || '中等' }}</div>
          </div>
          <div class="card p-4">
            <div class="text-sm text-[var(--text-muted)] mb-1">分析用时</div>
            <div class="text-xl font-bold">{{ executionTime }}</div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-semibold mb-1">分析报告已生成</h3>
              <p class="text-sm text-[var(--text-muted)]">点击查看完整报告或下载 PDF</p>
            </div>
            <div class="flex gap-3">
              <button @click="viewReport" class="btn-primary flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看报告
              </button>
              <button @click="downloadPDF" class="btn-secondary flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                下载 PDF
              </button>
            </div>
          </div>
        </div>

        <!-- 摘要 -->
        <div v-if="task.result?.summary" class="card p-6">
          <h3 class="font-semibold mb-3 flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-[#22C55E]/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            执行摘要
          </h3>
          <p class="text-[var(--text-secondary)] leading-relaxed">{{ task.result.summary }}</p>
        </div>
      </div>

      <!-- 失败状态 -->
      <div v-if="task.status === 'failed'" class="card p-6 border border-[#EF4444]/30">
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 rounded-xl bg-[#EF4444]/20 flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="font-semibold text-[#EF4444] mb-1">分析失败</h3>
            <p class="text-[var(--text-secondary)] text-sm mb-4">{{ task.error || '分析过程中发生错误，请重试' }}</p>
            <button @click="retryAnalysis" class="btn-primary">重新分析</button>
          </div>
        </div>
      </div>

      <!-- 任务信息 -->
      <div class="card p-6">
        <h3 class="font-semibold mb-4 flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-[#8B5CF6]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          任务信息
        </h3>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-[var(--text-muted)]">任务 ID</span>
            <p class="font-mono mt-1">{{ task.task_id }}</p>
          </div>
          <div>
            <span class="text-[var(--text-muted)]">创建时间</span>
            <p class="mt-1">{{ formatTime(task.created_at) }}</p>
          </div>
          <div>
            <span class="text-[var(--text-muted)]">分析深度</span>
            <p class="mt-1">{{ depthText }}</p>
          </div>
          <div>
            <span class="text-[var(--text-muted)]">分析师团队</span>
            <p class="mt-1">{{ analystsText }}</p>
          </div>
          <div v-if="task.completed_at">
            <span class="text-[var(--text-muted)]">完成时间</span>
            <p class="mt-1">{{ formatTime(task.completed_at) }}</p>
          </div>
          <div v-if="task.result?.model_info">
            <span class="text-[var(--text-muted)]">分析模型</span>
            <p class="mt-1">{{ task.result.model_info }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="w-16 h-16 rounded-full bg-[#EF4444]/20 flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 class="text-xl font-bold mb-2">任务不存在</h2>
        <p class="text-[var(--text-secondary)] mb-4">请检查任务 ID 是否正确</p>
        <button @click="goBack" class="btn-primary">返回列表</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const task = ref<any>(null)
let pollInterval: number | null = null

// 获取任务详情
const fetchTask = async () => {
  try {
    const taskId = route.params.id as string
    const response = await fetch(`/api/analysis/tasks/${taskId}/details`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const result = await response.json()
    // 后端直接返回任务数据，不包装在 success/data 中
    if (response.ok && result.task_id) {
      task.value = result
    }
  } catch (error) {
    console.error('获取任务详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 计算属性
const statusText = computed(() => {
  const map: Record<string, string> = {
    pending: '等待中',
    running: '分析中',
    completed: '已完成',
    failed: '失败'
  }
  return map[task.value?.status] || task.value?.status
})

const statusClass = computed(() => {
  const map: Record<string, string> = {
    pending: 'bg-[#F59E0B]/20 text-[#F59E0B]',
    running: 'bg-[#3B82F6]/20 text-[#3B82F6]',
    completed: 'bg-[#22C55E]/20 text-[#22C55E]',
    failed: 'bg-[#EF4444]/20 text-[#EF4444]'
  }
  return map[task.value?.status] || ''
})

const progress = computed(() => {
  if (!task.value) return 0
  if (task.value.status === 'completed') return 100
  if (task.value.status === 'failed') return 0
  // 模拟进度
  const elapsed = Date.now() - new Date(task.value.created_at).getTime()
  const estimated = 5 * 60 * 1000 // 5分钟
  return Math.min(95, Math.floor((elapsed / estimated) * 100))
})

const currentStep = computed(() => {
  const steps = [
    '正在收集市场数据...',
    '分析技术指标...',
    '评估基本面...',
    '生成分析报告...',
    '风险评级中...'
  ]
  const step = Math.floor(progress.value / 25)
  return steps[Math.min(step, steps.length - 1)]
})

const estimatedTime = computed(() => {
  if (!task.value) return '计算中...'
  const remaining = 100 - progress.value
  const minutes = Math.ceil(remaining / 20)
  return `${minutes} 分钟`
})

const recommendation = computed(() => {
  const rec = task.value?.result?.recommendation || ''
  if (rec.includes('买入') || rec.toLowerCase().includes('buy')) return '买入'
  if (rec.includes('卖出') || rec.toLowerCase().includes('sell')) return '卖出'
  return '持有'
})

const recommendationClass = computed(() => {
  const rec = recommendation.value
  if (rec === '买入') return 'text-[#22C55E]'
  if (rec === '卖出') return 'text-[#EF4444]'
  return 'text-[#F59E0B]'
})

const confidence = computed(() => {
  const score = task.value?.result?.confidence_score || 0
  return score > 1 ? Math.round(score) : Math.round(score * 100)
})

const riskClass = computed(() => {
  const risk = task.value?.result?.risk_level || '中等'
  const map: Record<string, string> = {
    '低': 'text-[#22C55E]',
    '中低': 'text-[#84CC16]',
    '中等': 'text-[#F59E0B]',
    '中高': 'text-[#F97316]',
    '高': 'text-[#EF4444]'
  }
  return map[risk] || 'text-[#F59E0B]'
})

const executionTime = computed(() => {
  if (!task.value?.created_at || !task.value?.completed_at) return '-'
  const start = new Date(task.value.created_at).getTime()
  const end = new Date(task.value.completed_at).getTime()
  const seconds = Math.floor((end - start) / 1000)
  if (seconds < 60) return `${seconds}秒`
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分${seconds % 60}秒`
})

const depthText = computed(() => {
  const map: Record<string, string> = {
    'quick': '快速 (2-5分钟)',
    'basic': '基础 (3-6分钟)',
    'standard': '标准 (4-8分钟)',
    'deep': '深度 (6-11分钟)',
    'comprehensive': '全面 (8-16分钟)'
  }
  return map[task.value?.analysis_depth] || '标准'
})

const analystsText = computed(() => {
  const analysts = task.value?.analysts || []
  const map: Record<string, string> = {
    'market': '市场分析师',
    'fundamentals': '基本面分析师',
    'news': '新闻分析师',
    'sentiment': '情绪分析师'
  }
  return analysts.map((a: string) => map[a] || a).join('、') || '默认团队'
})

// 方法
const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const goBack = () => {
  router.push('/tasks')
}

const viewReport = () => {
  router.push(`/reports/${task.value.task_id}`)
}

const downloadPDF = async () => {
  const token = authStore.token
  const url = `/api/reports/${task.value.task_id}/preview?token=${token}`
  window.open(url, '_blank')
}

const retryAnalysis = () => {
  router.push(`/analysis?code=${task.value.stock_code}`)
}

// 轮询更新（分析中时）
onMounted(() => {
  fetchTask()
  
  if (task.value?.status === 'running' || task.value?.status === 'pending') {
    pollInterval = window.setInterval(fetchTask, 5000)
  }
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})
</script>
