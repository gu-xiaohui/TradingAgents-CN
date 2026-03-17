<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        实时行情榜
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">数据日期: {{ dataDate || '加载中...' }}</p>
    </div>

    <!-- 标签切换 -->
    <div class="flex gap-2 mb-6">
      <button 
        @click="switchTab('gainers')" 
        class="tab-btn"
        :class="{ 'active': activeTab === 'gainers' }"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
        涨幅榜
      </button>
      <button 
        @click="switchTab('losers')" 
        class="tab-btn"
        :class="{ 'active': activeTab === 'losers' }"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
        </svg>
        跌幅榜
      </button>
      <button 
        @click="switchTab('volume')" 
        class="tab-btn"
        :class="{ 'active': activeTab === 'volume' }"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        成交额榜
      </button>
    </div>

    <!-- 统计信息 -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="stat-card">
        <div class="stat-value text-red-400">{{ stats.upCount }}</div>
        <div class="stat-label">上涨</div>
      </div>
      <div class="stat-card">
        <div class="stat-value text-green-400">{{ stats.downCount }}</div>
        <div class="stat-label">下跌</div>
      </div>
      <div class="stat-card">
        <div class="stat-value text-gray-400">{{ stats.flatCount }}</div>
        <div class="stat-label">平盘</div>
      </div>
      <div class="stat-card">
        <div class="stat-value text-blue-400">{{ stats.total }}</div>
        <div class="stat-label">总数</div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-20">
      <svg class="w-12 h-12 mx-auto animate-spin text-blue-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
      <p class="mt-4 text-[var(--text-secondary)]">加载中...</p>
    </div>

    <!-- 数据表格 -->
    <div v-else class="card">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-white/10">
              <th class="text-left py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">排名</th>
              <th class="text-left py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">代码</th>
              <th class="text-left py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">名称</th>
              <th class="text-right py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">最新价</th>
              <th class="text-right py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">涨跌幅</th>
              <th class="text-right py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">成交额</th>
              <th class="text-right py-3 px-4 text-sm text-[var(--text-secondary)] font-medium">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(stock, index) in stockList" 
              :key="stock.code"
              class="border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer"
              @click="goToDetail(stock.code)"
            >
              <td class="py-3 px-4">
                <span 
                  class="inline-flex items-center justify-center w-6 h-6 rounded text-xs font-bold"
                  :class="getRankClass(index)"
                >
                  {{ index + 1 }}
                </span>
              </td>
              <td class="py-3 px-4 font-mono">{{ stock.code }}</td>
              <td class="py-3 px-4 font-medium">{{ stock.name || '-' }}</td>
              <td class="py-3 px-4 text-right font-mono">¥{{ stock.close.toFixed(2) }}</td>
              <td class="py-3 px-4 text-right">
                <span 
                  class="inline-flex items-center px-2 py-1 rounded text-sm font-medium"
                  :class="getPctClass(stock.pct_chg)"
                >
                  {{ stock.pct_chg >= 0 ? '+' : '' }}{{ stock.pct_chg.toFixed(2) }}%
                </span>
              </td>
              <td class="py-3 px-4 text-right font-mono text-[var(--text-secondary)]">
                {{ formatAmount(stock.amount) }}
              </td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-3">
                  <button 
                    @click.stop="goToDetail(stock.code)"
                    class="text-blue-400 hover:text-blue-300 text-sm"
                  >
                    详情
                  </button>
                  <button 
                    @click.stop="goToAnalysis(stock.code)"
                    class="text-emerald-400 hover:text-emerald-300 text-sm"
                  >
                    分析
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 空状态 -->
      <div v-if="stockList.length === 0" class="text-center py-12 text-[var(--text-muted)]">
        <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <p>暂无数据</p>
        <p class="text-sm mt-2">请先在数据同步页面同步行情数据</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMarketByStockCode } from '@/utils/market'

const router = useRouter()

interface Stock {
  code: string
  name: string
  close: number
  pct_chg: number
  amount: number
}

const activeTab = ref('gainers')
const loading = ref(true)
const dataDate = ref('')
const stockList = ref<Stock[]>([])
const stats = ref({
  upCount: 0,
  downCount: 0,
  flatCount: 0,
  total: 0
})

// 切换标签
const switchTab = (tab: string) => {
  activeTab.value = tab
  loadStockList()
}

// 加载股票列表
const loadStockList = async () => {
  loading.value = true
  
  try {
    // 调用后端 API
    const response = await fetch(`/api/screening/rankings?type=${activeTab.value}&limit=50`)
    const result = await response.json()
    
    if (result.success) {
      stockList.value = result.data.list || []
      dataDate.value = result.data.date || ''
      stats.value = result.data.stats || stats.value
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    // 如果 API 失败，尝试直接从本地数据加载
    await loadFromLocalStorage()
  } finally {
    loading.value = false
  }
}

// 从本地存储加载（备用方案）
const loadFromLocalStorage = async () => {
  // 这里可以添加从 IndexedDB 或其他本地存储加载的逻辑
  stockList.value = []
}

// 格式化成交额
const formatAmount = (amount: number) => {
  if (!amount) return '-'
  if (amount >= 100000000) {
    return (amount / 100000000).toFixed(2) + '亿'
  } else if (amount >= 10000) {
    return (amount / 10000).toFixed(2) + '万'
  }
  return amount.toFixed(0)
}

// 获取排名样式
const getRankClass = (index: number) => {
  if (index === 0) return 'bg-yellow-500 text-black'
  if (index === 1) return 'bg-gray-400 text-black'
  if (index === 2) return 'bg-amber-600 text-white'
  return 'bg-white/10 text-[var(--text-secondary)]'
}

// 获取涨跌幅样式（涨红跌绿，符合中国股市习惯）
const getPctClass = (pct: number) => {
  if (pct > 0) return 'bg-red-500/20 text-red-400'
  if (pct < 0) return 'bg-green-500/20 text-green-400'
  return 'bg-gray-500/20 text-gray-400'
}

// 跳转到分析页面
const goToDetail = (code: string) => {
  router.push({
    name: 'StockDetail',
    params: { code: String(code).trim() },
    query: { market: getMarketByStockCode(code) }
  })
}

const goToAnalysis = (code: string) => {
  router.push(`/analysis?stock_code=${String(code).trim()}`)
}

onMounted(() => {
  loadStockList()
})
</script>

<style scoped>
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.tab-btn.active {
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  border-color: transparent;
  color: white;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}
</style>
