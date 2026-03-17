<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6 space-y-6 transition-colors duration-300">
    <!-- 欢迎区域 -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#22C55E]/20 via-[#8B5CF6]/20 to-[#22C55E]/20 p-8">
      <div class="absolute inset-0 bg-gradient-to-r from-[#22C55E]/10 to-[#8B5CF6]/10" />
      <div class="relative flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold flex items-center gap-3">
            TradingAgents-CN
            <span class="text-sm font-normal px-3 py-1 rounded-full bg-white/10 text-[var(--text-secondary)]">v1.0.0-preview</span>
          </h1>
          <p class="text-[var(--text-secondary)] mt-2 text-lg">AI 多智能体股票分析系统</p>
        </div>
        <div class="flex gap-3">
          <button @click="quickAnalysis" class="btn-primary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            快速分析
          </button>
          <button @click="goToScreening" class="btn-secondary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            股票筛选
          </button>
        </div>
      </div>
    </div>

    <!-- 学习中心推荐 -->
    <div class="glass rounded-2xl p-6 border-2 border-[#22C55E]/30">
      <div class="flex items-center gap-6">
        <div class="flex-shrink-0 w-16 h-16 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <div class="flex-1">
          <h2 class="text-xl font-semibold text-[var(--text-primary)]">AI 股票分析学习中心</h2>
          <p class="text-[var(--text-secondary)] mt-1">从零开始学习 AI、大语言模型和智能股票分析</p>
          <div class="flex flex-wrap gap-2 mt-3">
            <span class="badge-success">AI 基础知识</span>
            <span class="badge-success">提示词工程</span>
            <span class="badge-success">模型选择</span>
            <span class="badge-success">分析原理</span>
            <span class="badge-success">风险认知</span>
          </div>
        </div>
        <button @click="goToLearning" class="btn-primary flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          开始学习
        </button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：快速操作 + 最近分析 -->
      <div class="col-span-8 space-y-6">
        <!-- 快速操作 -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            快速操作
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div 
              v-for="action in quickActions" 
              :key="action.title"
              @click="action.handler"
              class="flex items-center gap-4 p-4 rounded-xl border border-white/10 bg-white/5 hover:bg-[#22C55E]/10 hover:border-[#22C55E]/30 cursor-pointer transition-all group"
            >
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[#22C55E]/20 to-[#8B5CF6]/20 flex items-center justify-center text-[#22C55E] group-hover:from-[#22C55E]/30 group-hover:to-[#8B5CF6]/30">
                <component :is="action.icon" />
              </div>
              <div class="flex-1">
                <h4 class="font-medium text-[var(--text-primary)]">{{ action.title }}</h4>
                <p class="text-sm text-[var(--text-muted)]">{{ action.desc }}</p>
              </div>
              <svg class="w-5 h-5 text-[var(--text-muted)] group-hover:text-[#22C55E] group-hover:translate-x-1 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>

        <!-- 最近分析 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold flex items-center gap-2">
              <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              最近分析
            </h3>
            <button @click="goToHistory" class="text-sm text-[#22C55E] hover:text-[#22C55E]/80 flex items-center gap-1">
              查看全部
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          
          <div v-if="recentAnalyses.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/10 text-left">
                  <th class="pb-3 text-sm font-medium text-[var(--text-muted)]">股票代码</th>
                  <th class="pb-3 text-sm font-medium text-[var(--text-muted)]">股票名称</th>
                  <th class="pb-3 text-sm font-medium text-[var(--text-muted)]">状态</th>
                  <th class="pb-3 text-sm font-medium text-[var(--text-muted)]">创建时间</th>
                  <th class="pb-3 text-sm font-medium text-[var(--text-muted)]">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="analysis in recentAnalyses" :key="analysis.task_id" class="border-b border-white/5 hover:bg-white/5">
                  <td class="py-3 text-[var(--text-primary)] font-mono">{{ analysis.stock_code }}</td>
                  <td class="py-3 text-[var(--text-secondary)]">{{ analysis.stock_name }}</td>
                  <td class="py-3">
                    <span :class="getStatusBadgeClass(analysis.status)">
                      {{ getStatusText(analysis.status) }}
                    </span>
                  </td>
                  <td class="py-3 text-[var(--text-muted)] text-sm">{{ formatTime(analysis.start_time) }}</td>
                  <td class="py-3">
                    <button @click="viewAnalysis(analysis)" class="text-[#22C55E] hover:text-[#22C55E]/80 text-sm mr-3">查看</button>
                    <button v-if="analysis.status === 'completed'" @click="downloadReport(analysis)" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)] text-sm">下载</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="text-center py-8 text-[var(--text-muted)]">
            <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>暂无分析记录</p>
          </div>
        </div>

        <!-- 市场快讯 -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            市场快讯
          </h3>
          
          <div v-if="marketNews.length > 0" class="space-y-3">
            <div 
              v-for="news in marketNews" 
              :key="news.id" 
              @click="openNewsUrl(news.url)"
              class="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
            >
              <p class="text-[var(--text-primary)] text-sm">{{ news.title }}</p>
              <p class="text-[var(--text-muted)] text-xs mt-1">{{ formatTime(news.time) }}</p>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-[var(--text-muted)]">
            <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            <p>暂无市场快讯</p>
          </div>
        </div>
      </div>

      <!-- 右侧：自选股 + 模拟账户 -->
      <div class="col-span-4 space-y-6">
        <!-- 我的自选股 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold flex items-center gap-2">
              <svg class="w-5 h-5 text-[#F59E0B]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              我的自选股
            </h3>
            <button @click="goToFavorites" class="text-sm text-[#22C55E] hover:text-[#22C55E]/80">查看全部</button>
          </div>
          
          <div v-if="favoriteStocks.length > 0" class="space-y-2">
            <div 
              v-for="stock in favoriteStocks.slice(0, 5)" 
              :key="stock.stock_code"
              @click="viewStockDetail(stock)"
              class="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
            >
              <div>
                <p class="font-mono text-[var(--text-primary)]">{{ stock.stock_code }}</p>
                <p class="text-xs text-[var(--text-muted)]">{{ stock.stock_name }}</p>
              </div>
              <div class="text-right">
                <p class="font-medium text-[var(--text-primary)]">¥{{ stock.current_price }}</p>
                <p :class="getPriceChangeClass(stock.change_percent)" class="text-sm">
                  {{ stock.change_percent > 0 ? '+' : '' }}{{ Number(stock.change_percent).toFixed(2) }}%
                </p>
              </div>
            </div>
            
            <button v-if="favoriteStocks.length > 5" @click="goToFavorites" class="w-full text-center text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] py-2">
              查看全部 {{ favoriteStocks.length }} 只自选股
            </button>
          </div>
          
          <div v-else class="text-center py-6 text-[var(--text-muted)]">
            <svg class="w-10 h-10 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
            <p class="text-sm">暂无自选股</p>
            <button @click="goToFavorites" class="mt-2 text-sm text-[#22C55E]">添加自选股</button>
          </div>
        </div>

        <!-- 模拟交易账户 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold flex items-center gap-2">
              <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              模拟交易
            </h3>
            <button @click="goToPaperTrading" class="text-sm text-[#22C55E] hover:text-[#22C55E]/80">查看详情</button>
          </div>
          
          <div v-if="paperAccount" class="space-y-4">
            <!-- A股账户 -->
            <div class="p-3 rounded-lg bg-white/5 border border-white/10">
              <p class="text-xs text-[var(--text-muted)] mb-2 flex items-center gap-1">
                🇨🇳 A股账户
              </p>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-[var(--text-secondary)]">现金</span>
                  <span class="text-[var(--text-primary)]">¥{{ formatMoney(paperAccount.cash?.CNY || paperAccount.cash) }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-[var(--text-secondary)]">持仓市值</span>
                  <span class="text-[var(--text-primary)]">¥{{ formatMoney(paperAccount.positions_value?.CNY || paperAccount.positions_value) }}</span>
                </div>
                <div class="flex justify-between text-sm pt-2 border-t border-white/10">
                  <span class="text-[var(--text-secondary)]">总资产</span>
                  <span class="text-[#22C55E] font-semibold">¥{{ formatMoney(paperAccount.equity?.CNY || paperAccount.equity) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-6 text-[var(--text-muted)]">
            <svg class="w-10 h-10 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
            <p class="text-sm">暂无账户信息</p>
            <button @click="goToPaperTrading" class="mt-2 text-sm text-[#22C55E]">查看模拟交易</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import type { AnalysisTask, AnalysisStatus } from '@/types/analysis'
import { favoritesApi } from '@/api/favorites'
import { analysisApi } from '@/api/analysis'
import { newsApi } from '@/api/news'
import { paperApi, type PaperAccountSummary } from '@/api/paper'
import { formatDateTime } from '@/utils/datetime'
import { extractSymbol } from '@/utils/stock'
import { getMarketByStockCode } from '@/utils/market'

const router = useRouter()
const authStore = useAuthStore()

// 图标组件
const IconDocument = () => h('svg', { class: 'w-6 h-6', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
])
const IconFiles = () => h('svg', { class: 'w-6 h-6', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })
])
const IconSearch = () => h('svg', { class: 'w-6 h-6', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
])
const IconList = () => h('svg', { class: 'w-6 h-6', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M4 6h16M4 10h16M4 14h16M4 18h16' })
])

// 快速操作
const quickActions = [
  { title: '单股分析', desc: '深度分析单只股票', icon: IconDocument, handler: () => router.push('/analysis/single') },
  { title: '批量分析', desc: '同时分析多只股票', icon: IconFiles, handler: () => router.push('/analysis/batch') },
  { title: '股票筛选', desc: '多维度条件筛选', icon: IconSearch, handler: () => router.push('/screening') },
  { title: '任务中心', desc: '查看管理任务', icon: IconList, handler: () => router.push('/tasks') },
]

// 数据
const recentAnalyses = ref<AnalysisTask[]>([])
const favoriteStocks = ref<any[]>([])
const marketNews = ref<any[]>([])
const paperAccount = ref<PaperAccountSummary | null>(null)

// 导航方法
const quickAnalysis = () => router.push('/analysis/single')
const goToScreening = () => router.push('/screening')
const goToHistory = () => router.push('/tasks?tab=completed')
const goToLearning = () => router.push('/learning')
const goToFavorites = () => router.push('/favorites')
const goToPaperTrading = () => router.push('/paper')

const viewAnalysis = (analysis: AnalysisTask) => {
  if ((analysis as any)?.status === 'completed') {
    router.push({ name: 'ReportDetail', params: { id: analysis.task_id } })
  } else {
    router.push('/tasks?tab=running')
  }
}

const viewStockDetail = (stock: any) => {
  const rawCode = String(stock?.stock_code || stock?.symbol || stock?.code || '').trim()
  const code = extractSymbol(rawCode)
  if (!code) {
    ElMessage.warning('股票代码缺失，无法打开详情')
    return
  }

  router.push({ name: 'StockDetail', params: { code }, query: { market: getMarketByStockCode(rawCode) } })
}

const openNewsUrl = (url?: string) => {
  if (url) window.open(url, '_blank')
  else ElMessage.info('该新闻暂无详情链接')
}

const downloadReport = async (analysis: AnalysisTask) => {
  try {
    const reportId = analysis.task_id
    const res = await fetch(`/api/reports/${reportId}/download?format=markdown`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) {
      ElMessage.error('下载失败，报告可能尚未生成')
      return
    }
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const code = (analysis as any).stock_code || 'stock'
    const dateStr = (analysis as any).analysis_date || ''
    a.download = `${code}_分析报告_${String(dateStr).slice(0,10)}.md`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    ElMessage.success('报告已开始下载')
  } catch (err) {
    ElMessage.error('下载失败，请稍后重试')
  }
}

// 工具方法
const formatTime = (time: string) => formatDateTime(time)

const formatMoney = (value: number) => {
  return value?.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') || '0.00'
}

const getStatusText = (status: string | AnalysisStatus) => {
  const map: Record<string, string> = {
    pending: '等待中', processing: '处理中', running: '处理中',
    completed: '已完成', failed: '失败', cancelled: '已取消'
  }
  return map[status] || String(status)
}

const getStatusBadgeClass = (status: string | AnalysisStatus) => {
  const map: Record<string, string> = {
    pending: 'badge-info', processing: 'badge-warning', running: 'badge-warning',
    completed: 'badge-success', failed: 'badge-danger', cancelled: 'badge-info'
  }
  return map[status] || 'badge-info'
}

const getPriceChangeClass = (changePercent: number) => {
  if (changePercent > 0) return 'text-[#EF4444]'
  if (changePercent < 0) return 'text-[#22C55E]'
  return 'text-[var(--text-secondary)]'
}

// 加载数据
const loadFavoriteStocks = async () => {
  try {
    const response = await favoritesApi.list()
    if (response.success && response.data) {
      favoriteStocks.value = response.data.map((item: any) => ({
        stock_code: item.stock_code,
        stock_name: item.stock_name,
        current_price: item.current_price || 0,
        change_percent: item.change_percent || 0
      }))
    }
  } catch (error) {
    console.error('加载自选股失败:', error)
  }
}

const loadRecentAnalyses = async () => {
  try {
    const res = await analysisApi.getTaskList({ limit: 10, offset: 0 })
    const body: any = (res as any)?.data?.data || (res as any)?.data || res || {}
    recentAnalyses.value = body.tasks || []
  } catch (error) {
    console.error('加载最近分析失败:', error)
  }
}

const loadMarketNews = async () => {
  try {
    let response = await newsApi.getLatestNews(undefined, 10, 24)
    if (response.success && response.data && response.data.news.length === 0) {
      response = await newsApi.getLatestNews(undefined, 10, 24 * 365)
    }
    if (response.success && response.data) {
      marketNews.value = response.data.news.map((item: any) => ({
        id: item.id || item.title,
        title: item.title,
        time: item.publish_time,
        url: item.url,
        source: item.source
      }))
    }
  } catch (error) {
    console.error('加载市场快讯失败:', error)
  }
}

const loadPaperAccount = async () => {
  try {
    const response = await paperApi.getAccount()
    if (response.success && response.data) {
      paperAccount.value = response.data.account
    }
  } catch (error) {
    console.error('加载模拟交易账户失败:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    loadFavoriteStocks(),
    loadRecentAnalyses(),
    loadMarketNews(),
    loadPaperAccount()
  ])
})
</script>

<style scoped>
/* 使用 Tailwind 的 glass 类需要确保在 tailwind.css 中定义 */
</style>
