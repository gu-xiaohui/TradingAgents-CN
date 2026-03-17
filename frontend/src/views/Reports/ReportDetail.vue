<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 加载状态 -->
    <div v-if="loading" class="space-y-6">
      <div class="card p-6 animate-pulse">
        <div class="h-8 bg-white/10 rounded w-1/3 mb-4"></div>
        <div class="h-4 bg-white/10 rounded w-1/2 mb-2"></div>
        <div class="h-4 bg-white/10 rounded w-2/3"></div>
      </div>
      <div class="grid grid-cols-3 gap-4">
        <div class="card p-6 animate-pulse">
          <div class="h-20 bg-white/10 rounded"></div>
        </div>
        <div class="card p-6 animate-pulse">
          <div class="h-20 bg-white/10 rounded"></div>
        </div>
        <div class="card p-6 animate-pulse">
          <div class="h-20 bg-white/10 rounded"></div>
        </div>
      </div>
    </div>

    <!-- 报告内容 -->
    <div v-else-if="report" class="space-y-6">
      <!-- 报告头部 -->
      <div class="card p-6">
        <div class="flex items-start justify-between gap-6">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#8B5CF6] flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-bold">{{ report.stock_name || report.stock_symbol }} 分析报告</h1>
                <div class="flex items-center gap-3 mt-1 text-sm text-[var(--text-secondary)]">
                  <span class="px-2 py-0.5 rounded-lg bg-[#3B82F6]/20 text-[#3B82F6] font-mono">{{ report.stock_symbol }}</span>
                  <span v-if="report.stock_name && report.stock_name !== report.stock_symbol" class="px-2 py-0.5 rounded-lg bg-white/10">{{ report.stock_name }}</span>
                  <span class="px-2 py-0.5 rounded-lg bg-[#22C55E]/20 text-[#22C55E]">{{ getStatusText(report.status) }}</span>
                </div>
              </div>
            </div>
            
            <div class="flex flex-wrap items-center gap-4 text-sm text-[var(--text-secondary)]">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{{ formatTime(report.created_at) }}</span>
              </div>
              <div v-if="report.analysts && report.analysts.length" class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span>{{ formatAnalysts(report.analysts) }}</span>
              </div>
              <div v-if="report.model_info && report.model_info !== 'Unknown'" class="flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span class="px-2 py-0.5 rounded-lg bg-[#8B5CF6]/20 text-[#8B5CF6]">{{ report.model_info }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <button
              v-if="canApplyToTrading"
              @click="applyToTrading"
              class="btn-primary flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              应用到交易
            </button>
            <div class="relative">
              <button @click="showDownloadMenu = !showDownloadMenu" class="btn-secondary flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                下载报告
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-if="showDownloadMenu" class="absolute right-0 mt-2 w-48 bg-[var(--bg-secondary)] rounded-xl shadow-xl border border-white/10 overflow-hidden z-10">
                <button @click="downloadReport('markdown')" class="w-full px-4 py-2 text-left text-sm hover:bg-white/5 flex items-center gap-2">
                  <svg class="w-4 h-4 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Markdown
                </button>
                <button @click="downloadReport('pdf')" class="w-full px-4 py-2 text-left text-sm hover:bg-white/5 flex items-center gap-2">
                  <svg class="w-4 h-4 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                  PDF
                </button>
                <button @click="downloadReport('json')" class="w-full px-4 py-2 text-left text-sm hover:bg-white/5 flex items-center gap-2">
                  <svg class="w-4 h-4 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  JSON
                </button>
              </div>
            </div>
            <button @click="goBack" class="btn-ghost flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              返回
            </button>
          </div>
        </div>
      </div>

      <!-- 风险提示 -->
      <div class="bg-gradient-to-r from-[#F59E0B]/10 to-[#EF4444]/10 rounded-xl p-4 border border-[#F59E0B]/30">
        <div class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-lg bg-[#F59E0B]/20 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-[#F59E0B]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div class="text-sm">
            <p class="font-semibold text-[#F59E0B] mb-2">⚠️ 重要风险提示</p>
            <ul class="text-[var(--text-secondary)] space-y-1 list-disc list-inside">
              <li>本系统为股票分析辅助工具，所有分析结果仅供参考，不构成投资建议</li>
              <li>股票投资存在风险，可能导致本金损失</li>
              <li>请基于自身风险承受能力独立做出投资决策</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 关键指标 -->
      <div class="grid grid-cols-3 gap-4">
        <!-- 分析建议 -->
        <div class="card p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-[#3B82F6]/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span class="font-medium">分析参考</span>
          </div>
          <div class="text-lg font-medium text-[var(--text-primary)]" v-html="renderMarkdown(report.recommendation || '暂无')"></div>
          <span class="inline-block mt-3 text-xs px-2 py-1 rounded-lg bg-white/10 text-[var(--text-muted)]">仅供参考</span>
        </div>

        <!-- 风险评估 -->
        <div class="card p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-[#EF4444]/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <span class="font-medium">风险评估</span>
          </div>
          <div class="flex items-center gap-2 mb-2">
            <svg v-for="star in 5" :key="star" class="w-5 h-5" :class="star <= getRiskStars(report.risk_level || '中等') ? 'text-[#F59E0B]' : 'text-white/20'" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
            </svg>
          </div>
          <div class="text-lg font-bold" :style="{ color: getRiskColor(report.risk_level || '中等') }">
            {{ report.risk_level || '中等' }}风险
          </div>
        </div>

        <!-- 模型置信度 -->
        <div class="card p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-[#8B5CF6]/20 flex items-center justify-center">
              <svg class="w-4 h-4 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <span class="font-medium">模型置信度</span>
          </div>
          <div class="flex items-center gap-4">
            <div class="relative w-20 h-20">
              <svg class="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
                <path class="text-white/10" stroke="currentColor" stroke-width="3" fill="none" d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path 
                  :stroke="getConfidenceColor(normalizeConfidenceScore(report.confidence_score || 0))" 
                  stroke-width="3" 
                  stroke-linecap="round"
                  fill="none"
                  :stroke-dasharray="`${normalizeConfidenceScore(report.confidence_score || 0)}, 100`"
                  d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831a 15.9155 15.9155 0 0 1 0 -31.831" 
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xl font-bold">{{ normalizeConfidenceScore(report.confidence_score || 0) }}</span>
              </div>
            </div>
            <div class="text-sm text-[var(--text-secondary)]">
              {{ getConfidenceLabel(normalizeConfidenceScore(report.confidence_score || 0)) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 报告摘要 -->
      <div v-if="report.summary" class="card p-6">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-8 h-8 rounded-lg bg-[#22C55E]/20 flex items-center justify-center">
            <svg class="w-4 h-4 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <span class="font-medium">执行摘要</span>
        </div>
        <div class="prose prose-invert max-w-none text-[var(--text-secondary)]" v-html="renderMarkdown(report.summary)"></div>
      </div>

      <!-- 分析报告模块 -->
      <div class="card">
        <div class="flex items-center gap-2 p-6 border-b border-white/10">
          <div class="w-8 h-8 rounded-lg bg-[#3B82F6]/20 flex items-center justify-center">
            <svg class="w-4 h-4 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <span class="font-medium">分析报告</span>
        </div>
        
        <!-- 标签页 -->
        <div class="flex items-center gap-1 px-6 pt-4 border-b border-white/10 overflow-x-auto">
          <button
            v-for="(content, moduleName) in report.reports"
            :key="moduleName"
            @click="activeModule = moduleName"
            class="px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors border-b-2 -mb-px"
            :class="activeModule === moduleName 
              ? 'text-[#22C55E] border-[#22C55E]' 
              : 'text-[var(--text-secondary)] border-transparent hover:text-[var(--text-primary)]'"
          >
            {{ getModuleDisplayName(moduleName) }}
          </button>
        </div>

        <!-- 报告内容 -->
        <div class="p-6">
          <div v-if="report.reports && report.reports[activeModule]" class="prose prose-invert max-w-none text-[var(--text-secondary)]">
            <div v-if="typeof report.reports[activeModule] === 'string'" v-html="renderMarkdown(report.reports[activeModule])"></div>
            <pre v-else class="bg-white/5 p-4 rounded-xl overflow-x-auto text-sm">{{ JSON.stringify(report.reports[activeModule], null, 2) }}</pre>
          </div>
          <div v-else class="text-center py-12 text-[var(--text-muted)]">
            暂无报告内容
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="card p-12 text-center">
      <div class="w-16 h-16 rounded-full bg-[#EF4444]/20 flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h2 class="text-xl font-bold mb-2">报告加载失败</h2>
      <p class="text-[var(--text-secondary)] mb-6">请检查报告ID是否正确或稍后重试</p>
      <button @click="goBack" class="btn-primary">返回列表</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { marked } from 'marked'

// 配置 marked
marked.setOptions({ breaks: true, gfm: true })

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 状态
const loading = ref(true)
const report = ref<any>(null)
const activeModule = ref('')
const showDownloadMenu = ref(false)

// 获取报告详情
const fetchReportDetail = async () => {
  loading.value = true
  try {
    const reportId = route.params.id as string
    const response = await fetch(`/api/reports/${reportId}/detail`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) throw new Error(`HTTP ${response.status}`)

    const result = await response.json()
    if (result.success) {
      report.value = result.data
      // 设置默认激活的模块
      const reports = result.data.reports || {}
      const moduleNames = Object.keys(reports)
      if (moduleNames.length > 0) {
        activeModule.value = moduleNames[0]
      }
    } else {
      throw new Error(result.message || '获取报告详情失败')
    }
  } catch (error) {
    console.error('获取报告详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 下载报告
const downloadReport = async (format: string) => {
  showDownloadMenu.value = false
  try {
    // 使用 task_id 作为报告标识符（更稳定）
    const reportId = report.value.task_id || report.value.id
    
    // 所有格式都直接下载
    const response = await fetch(`/api/reports/${reportId}/download?format=${format}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })

    if (!response.ok) throw new Error(`HTTP ${response.status}`)

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const ext = { markdown: 'md', pdf: 'pdf', json: 'json' }[format] || 'txt'
    a.download = `${report.value.stock_symbol || report.value.stock_code || 'report'}_分析报告.${ext}`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (error) {
    console.error('下载报告失败:', error)
  }
}

// 判断是否可以应用到交易
const canApplyToTrading = computed(() => {
  if (!report.value) return false
  const rec = report.value.recommendation || ''
  return rec.includes('买入') || rec.includes('卖出') || rec.toLowerCase().includes('buy') || rec.toLowerCase().includes('sell')
})

// 应用到交易
const applyToTrading = () => {
  // TODO: 实现交易逻辑
  alert('功能开发中...')
}

// 返回
const goBack = () => {
  router.push('/reports')
}

// 工具函数
const getStatusText = (status: string) => {
  const map: Record<string, string> = { completed: '已完成', processing: '生成中', failed: '失败' }
  return map[status] || status
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

const formatAnalysts = (analysts: string[]) => {
  const map: Record<string, string> = {
    market: '市场分析师', fundamentals: '基本面分析师', news: '新闻分析师',
    social: '社媒分析师', sentiment: '情绪分析师', technical: '技术分析师'
  }
  return analysts.map(a => map[a] || a).join('、')
}

const getModuleDisplayName = (name: string) => {
  const map: Record<string, string> = {
    market_report: '📈 市场技术分析', sentiment_report: '💭 市场情绪分析',
    news_report: '📰 新闻事件分析', fundamentals_report: '💰 基本面分析',
    bull_researcher: '🐂 多头研究员', bear_researcher: '🐻 空头研究员',
    research_team_decision: '🔬 研究经理决策', trader_investment_plan: '💼 交易员计划',
    risky_analyst: '⚡ 激进分析师', safe_analyst: '🛡️ 保守分析师',
    neutral_analyst: '⚖️ 中性分析师', risk_management_decision: '👔 投资组合经理',
    final_trade_decision: '🎯 最终交易决策'
  }
  return map[name] || name.replace(/_/g, ' ')
}

const renderMarkdown = (content: string) => {
  if (!content) return ''
  try {
    return marked.parse(content) as string
  } catch {
    return `<pre style="white-space: pre-wrap;">${content}</pre>`
  }
}

const normalizeConfidenceScore = (score: number) => score > 1 ? Math.round(score) : Math.round(score * 100)

const getConfidenceColor = (score: number) => {
  if (score >= 80) return '#22C55E'
  if (score >= 60) return '#3B82F6'
  if (score >= 40) return '#F59E0B'
  return '#EF4444'
}

const getConfidenceLabel = (score: number) => {
  if (score >= 80) return '较高'
  if (score >= 60) return '中上'
  if (score >= 40) return '中等'
  return '较低'
}

const getRiskStars = (level: string) => {
  const map: Record<string, number> = { '低': 1, '中低': 2, '中等': 3, '中高': 4, '高': 5 }
  return map[level] || 3
}

const getRiskColor = (level: string) => {
  const map: Record<string, string> = { '低': '#22C55E', '中低': '#84CC16', '中等': '#F59E0B', '中高': '#F97316', '高': '#EF4444' }
  return map[level] || '#F59E0B'
}

// 点击外部关闭下载菜单
const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (!target.closest('.relative')) {
    showDownloadMenu.value = false
  }
}

onMounted(() => {
  fetchReportDetail()
  document.addEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.prose :deep(h1) { font-size: 1.5rem; font-weight: 700; margin: 1.5rem 0 1rem; }
.prose :deep(h2) { font-size: 1.25rem; font-weight: 600; margin: 1.25rem 0 0.75rem; }
.prose :deep(h3) { font-size: 1.125rem; font-weight: 600; margin: 1rem 0 0.5rem; }
.prose :deep(p) { margin: 0.5rem 0; line-height: 1.7; }
.prose :deep(ul), .prose :deep(ol) { margin: 0.5rem 0; padding-left: 1.5rem; }
.prose :deep(li) { margin: 0.25rem 0; }
.prose :deep(code) { background: rgba(255,255,255,0.1); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.875rem; }
.prose :deep(pre) { background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 0.75rem; overflow-x: auto; }
.prose :deep(blockquote) { border-left: 3px solid rgba(255,255,255,0.2); padding-left: 1rem; margin: 1rem 0; color: var(--text-secondary); }
.prose :deep(table) { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.prose :deep(th), .prose :deep(td) { border: 1px solid rgba(255,255,255,0.1); padding: 0.5rem; text-align: left; }
.prose :deep(th) { background: rgba(255,255,255,0.05); }
</style>
