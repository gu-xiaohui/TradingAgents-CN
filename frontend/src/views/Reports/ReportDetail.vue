<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <svg class="w-10 h-10 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <!-- 报告内容 -->
    <div v-else-if="report" class="p-6 space-y-6">
      <!-- 头部 -->
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <h1 class="text-2xl font-bold">{{ report.stock_name || report.stock_symbol }} 分析报告</h1>
              <span class="badge-success">已完成</span>
            </div>
            <div class="flex items-center gap-4 text-sm text-[var(--text-muted)]">
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
                </svg>
                {{ report.stock_symbol }}
              </span>
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
                </svg>
                {{ formatTime(report.created_at || report.start_time) }}
              </span>
              <span v-if="report.model_info" class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75a2.25 2.25 0 0 0-2.25-2.25H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Zm.75-12h9v9h-9v-9Z" />
                </svg>
                {{ report.model_info }}
              </span>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <button @click="goBack" class="btn-secondary">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
              </svg>
              返回
            </button>
            <button @click="downloadReport('markdown')" class="btn-primary">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
              </svg>
              下载报告
            </button>
          </div>
        </div>
      </div>

      <!-- 风险提示 -->
      <div class="p-4 rounded-xl bg-[#F59E0B]/10 border border-[#F59E0B]/20">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-[#F59E0B] flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
          </svg>
          <div class="text-sm">
            <p class="font-medium text-[#F59E0B] mb-1">⚠️ 重要风险提示</p>
            <p class="text-[var(--text-secondary)]">本报告仅为 AI 分析参考，不构成投资建议。投资有风险，决策需谨慎。</p>
          </div>
        </div>
      </div>

      <!-- 报告主体 -->
      <div class="grid grid-cols-12 gap-6">
        <!-- 左侧：报告内容 -->
        <div class="col-span-8">
          <div class="card prose prose-invert max-w-none">
            <div v-html="renderedContent" class="report-markdown"></div>
          </div>
        </div>

        <!-- 右侧：摘要和评分 -->
        <div class="col-span-4 space-y-6">
          <!-- 投资评分 -->
          <div v-if="report.rating" class="card">
            <h3 class="text-lg font-semibold mb-4">投资评分</h3>
            <div class="flex items-center justify-center py-4">
              <div 
                class="w-24 h-24 rounded-full flex items-center justify-center text-3xl font-bold"
                :class="getRatingClass(report.rating)"
              >
                {{ report.rating }}
              </div>
            </div>
            <div class="text-center text-sm text-[var(--text-muted)]">
              {{ getRatingText(report.rating) }}
            </div>
          </div>

          <!-- 报告摘要 -->
          <div class="card">
            <h3 class="text-lg font-semibold mb-4">报告摘要</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-[var(--text-muted)]">股票代码</span>
                <span class="font-mono">{{ report.stock_symbol }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-[var(--text-muted)]">股票名称</span>
                <span>{{ report.stock_name || '-' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-[var(--text-muted)]">分析深度</span>
                <span>{{ report.research_depth || '标准' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-[var(--text-muted)]">分析时间</span>
                <span>{{ formatTime(report.start_time) }}</span>
              </div>
              <div v-if="report.analysts" class="flex justify-between">
                <span class="text-[var(--text-muted)]">参与分析师</span>
                <span>{{ formatAnalysts(report.analysts) }}</span>
              </div>
            </div>
          </div>

          <!-- 快速导航 -->
          <div v-if="tocItems.length > 0" class="card">
            <h3 class="text-lg font-semibold mb-4">目录</h3>
            <nav class="space-y-2">
              <a
                v-for="item in tocItems"
                :key="item.id"
                :href="'#' + item.id"
                class="block text-sm text-[var(--text-secondary)] hover:text-[#22C55E] transition-colors"
                :class="{ 'pl-4': item.level > 1 }"
              >
                {{ item.text }}
              </a>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="flex flex-col items-center justify-center py-20">
      <svg class="w-16 h-16 text-[var(--text-muted)] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
      </svg>
      <p class="text-[var(--text-muted)] mt-4">报告加载失败或不存在</p>
      <button @click="goBack" class="btn-secondary mt-4">返回列表</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const report = ref<any>(null)

const reportId = computed(() => route.params.id as string)

// 渲染 Markdown 内容
const renderedContent = computed(() => {
  if (!report.value?.content) return ''
  // 简单的 Markdown 渲染（实际项目中应使用 marked 或 markdown-it）
  let content = report.value.content
  // 标题
  content = content.replace(/^### (.*$)/gm, '<h3 class="text-lg font-semibold mt-6 mb-3">$1</h3>')
  content = content.replace(/^## (.*$)/gm, '<h2 class="text-xl font-semibold mt-8 mb-4">$1</h2>')
  content = content.replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-8 mb-4">$1</h1>')
  // 粗体
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  // 斜体
  content = content.replace(/\*(.*?)\*/g, '<em>$1</em>')
  // 列表
  content = content.replace(/^- (.*$)/gm, '<li class="ml-4">$1</li>')
  // 段落
  content = content.replace(/\n\n/g, '</p><p class="my-3">')
  content = `<p class="my-3">${content}</p>`
  return content
})

// 目录
const tocItems = computed(() => {
  if (!report.value?.content) return []
  const items: { id: string; text: string; level: number }[] = []
  const regex = /^(#{1,3})\s+(.+)$/gm
  let match
  while ((match = regex.exec(report.value.content)) !== null) {
    items.push({
      id: match[2].toLowerCase().replace(/\s+/g, '-'),
      text: match[2],
      level: match[1].length
    })
  }
  return items
})

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const formatAnalysts = (analysts: string | string[]) => {
  if (!analysts) return '-'
  if (Array.isArray(analysts)) return analysts.join(', ')
  return analysts
}

const getRatingClass = (rating: number) => {
  if (rating >= 8) return 'bg-[#22C55E]/20 text-[#22C55E]'
  if (rating >= 6) return 'bg-[#F59E0B]/20 text-[#F59E0B]'
  return 'bg-[#EF4444]/20 text-[#EF4444]'
}

const getRatingText = (rating: number) => {
  if (rating >= 9) return '强烈推荐'
  if (rating >= 8) return '推荐买入'
  if (rating >= 6) return '中性观望'
  if (rating >= 4) return '谨慎关注'
  return '风险较高'
}

const goBack = () => {
  router.push('/reports')
}

const downloadReport = async (format: string) => {
  try {
    const res = await fetch(`/api/reports/${reportId.value}/download?format=${format}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) {
      ElMessage.error('下载失败')
      return
    }
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${report.value?.stock_symbol || 'report'}_分析报告.${format === 'markdown' ? 'md' : format}`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    ElMessage.success('报告已下载')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const loadReport = async () => {
  loading.value = true
  try {
    const res = await fetch(`/api/reports/${reportId.value}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
      const data = await res.json()
      report.value = data.data || data
    } else {
      ElMessage.error('加载报告失败')
    }
  } catch (error) {
    console.error('加载报告失败:', error)
    ElMessage.error('加载报告失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadReport()
})
</script>

<style scoped>
.report-markdown :deep(h1) {
  @apply text-2xl font-bold mt-8 mb-4;
}
.report-markdown :deep(h2) {
  @apply text-xl font-semibold mt-6 mb-3;
}
.report-markdown :deep(h3) {
  @apply text-lg font-semibold mt-4 mb-2;
}
.report-markdown :deep(p) {
  @apply my-3 leading-relaxed;
}
.report-markdown :deep(ul) {
  @apply list-disc list-inside my-3;
}
.report-markdown :deep(li) {
  @apply my-1;
}
.report-markdown :deep(strong) {
  @apply font-semibold text-[var(--text-primary)];
}
.report-markdown :deep(code) {
  @apply bg-white/10 px-1 py-0.5 rounded text-sm;
}
.report-markdown :deep(blockquote) {
  @apply border-l-4 border-[#22C55E] pl-4 my-4 text-[var(--text-secondary)];
}
</style>
