<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 头部 -->
    <div class="flex items-start justify-between mb-6">
      <div class="flex items-center gap-4">
        <div class="text-3xl font-bold">{{ code }}</div>
        <div class="text-xl">{{ stockName || '-' }}</div>
        <span :class="getMarketClass()" class="px-2 py-1 rounded text-sm">{{ market || '-' }}</span>
      </div>
      <div class="flex gap-2">
        <button @click="onToggleFavorite" 
                :class="isFav ? 'bg-[#F59E0B] hover:bg-[#D97706]' : 'bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)]'"
                class="px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
          </svg>
          {{ isFav ? '已自选' : '加自选' }}
        </button>
        <button v-if="market !== 'HK' && market !== 'US'" @click="showSyncDialog" :disabled="syncLoading"
                class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          同步数据
        </button>
        <button @click="goPaperTrading" 
                class="px-4 py-2 bg-[#8B5CF6] hover:bg-[#7C3AED] text-white rounded-lg transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
          </svg>
          模拟交易
        </button>
      </div>
    </div>

    <!-- 报价卡片 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 mb-6">
      <div class="flex items-center gap-6 mb-4">
        <div :class="changeClass" class="text-4xl font-bold">{{ fmtPrice(quote.price) }}</div>
        <div :class="changeClass" class="text-xl">{{ fmtPercent(quote.changePercent) }}</div>
        <span class="text-sm text-[var(--text-secondary)]">{{ refreshText }}</span>
        <button @click="refreshQuote" class="px-3 py-1 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded transition-colors">
          刷新
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4 text-sm">
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">今开</div>
          <div class="font-semibold mt-1">{{ fmtPrice(quote.open) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">最高</div>
          <div class="font-semibold mt-1 text-[#EF4444]">{{ fmtPrice(quote.high) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">最低</div>
          <div class="font-semibold mt-1 text-[#22C55E]">{{ fmtPrice(quote.low) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">昨收</div>
          <div class="font-semibold mt-1">{{ fmtPrice(quote.prevClose) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">成交量</div>
          <div class="font-semibold mt-1">{{ fmtVolume(quote.volume) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">成交额</div>
          <div class="font-semibold mt-1">{{ fmtAmount(quote.amount) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">换手率</div>
          <div class="font-semibold mt-1">{{ fmtPercent(quote.turnover) }}</div>
        </div>
        <div class="text-center p-3 bg-[var(--bg-tertiary)] rounded-lg">
          <div class="text-[var(--text-secondary)]">振幅</div>
          <div class="font-semibold mt-1">{{ quote.amplitude ? quote.amplitude.toFixed(2) + '%' : '-' }}</div>
        </div>
      </div>
    </div>

    <!-- Tab 导航 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] overflow-hidden">
      <div class="flex border-b border-[var(--border-color)]">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
                :class="activeTab === tab.key ? 'bg-[var(--bg-tertiary)] text-[#22C55E] border-b-2 border-[#22C55E]' : ''"
                class="px-6 py-3 text-sm font-medium transition-colors hover:bg-[var(--bg-hover)]">
          {{ tab.label }}
        </button>
      </div>

      <div class="p-6">
        <!-- 概览 -->
        <div v-if="activeTab === 'overview'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="font-semibold mb-3">基本信息</h3>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
                  <span class="text-[var(--text-secondary)]">行业</span>
                  <span>{{ basicInfo.industry || '-' }}</span>
                </div>
                <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
                  <span class="text-[var(--text-secondary)]">总市值</span>
                  <span>{{ fmtAmount(basicInfo.marketCap) }}</span>
                </div>
                <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
                  <span class="text-[var(--text-secondary)]">市盈率</span>
                  <span>{{ basicInfo.pe || '-' }}</span>
                </div>
                <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
                  <span class="text-[var(--text-secondary)]">市净率</span>
                  <span>{{ basicInfo.pb || '-' }}</span>
                </div>
              </div>
            </div>
            <div>
              <h3 class="font-semibold mb-3">公司简介</h3>
              <p class="text-sm text-[var(--text-secondary)] leading-relaxed">{{ basicInfo.description || '暂无简介' }}</p>
            </div>
          </div>
        </div>

        <!-- K线图 -->
        <div v-if="activeTab === 'chart'" class="h-[400px]">
          <div ref="chartRef" class="w-full h-full"></div>
        </div>

        <!-- 分析报告 -->
        <div v-if="activeTab === 'analysis'" class="space-y-4">
          <div v-if="reports.length === 0" class="text-center py-12 text-[var(--text-secondary)]">
            暂无分析报告
          </div>
          <div v-for="report in reports" :key="report.id" 
               class="p-4 bg-[var(--bg-tertiary)] rounded-lg hover:bg-[var(--bg-hover)] transition-colors cursor-pointer"
               @click="viewReport(report)">
            <div class="flex items-center justify-between mb-2">
              <span class="font-semibold">{{ report.title }}</span>
              <span :class="getRecommendationClass(report.recommendation)" class="px-2 py-1 rounded text-xs">
                {{ report.recommendation }}
              </span>
            </div>
            <p class="text-sm text-[var(--text-secondary)] line-clamp-2">{{ report.summary }}</p>
            <div class="text-xs text-[var(--text-secondary)] mt-2">{{ formatTime(report.created_at) }}</div>
          </div>
        </div>

        <!-- 财务数据 -->
        <div v-if="activeTab === 'financial'" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-[var(--border-color)]">
                <th class="text-left py-3 px-4">指标</th>
                <th v-for="col in financialData.columns" :key="col" class="text-right py-3 px-4">{{ col }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in financialData.rows" :key="row.name" class="border-b border-[var(--border-color)]">
                <td class="py-3 px-4">{{ row.name }}</td>
                <td v-for="(val, idx) in row.values" :key="idx" class="text-right py-3 px-4">{{ val }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 新闻 -->
        <div v-if="activeTab === 'news'" class="space-y-4">
          <div v-if="news.length === 0" class="text-center py-12 text-[var(--text-secondary)]">
            暂无新闻
          </div>
          <a v-for="item in news" :key="item.id" :href="item.url" target="_blank"
             class="block p-4 bg-[var(--bg-tertiary)] rounded-lg hover:bg-[var(--bg-hover)] transition-colors">
            <div class="font-semibold mb-1">{{ item.title }}</div>
            <div class="text-sm text-[var(--text-secondary)]">{{ item.source }} · {{ formatTime(item.time) }}</div>
          </a>
        </div>
      </div>
    </div>

    <!-- 同步弹窗 -->
    <div v-if="syncDialogVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="syncDialogVisible = false">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 w-full max-w-md mx-4" @click.stop>
        <h3 class="text-lg font-semibold mb-4">同步数据</h3>
        <div class="space-y-4">
          <div>
            <label class="text-sm text-[var(--text-secondary)] block mb-1.5">数据类型</label>
            <select v-model="syncType" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
              <option value="basic">基础信息</option>
              <option value="quote">行情数据</option>
              <option value="all">全部数据</option>
            </select>
          </div>
          <div class="flex gap-2">
            <button @click="syncDialogVisible = false" class="flex-1 px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
              取消
            </button>
            <button @click="doSync" :disabled="syncLoading" 
                    class="flex-1 px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors disabled:opacity-50">
              确认同步
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { stockApi } from '@/api/stock'

const route = useRoute()
const router = useRouter()

const code = computed(() => route.params.code as string)
const market = computed(() => route.query.market as string || 'A')

const stockName = ref('')
const isFav = ref(false)
const syncLoading = ref(false)
const syncDialogVisible = ref(false)
const syncType = ref('all')

const activeTab = ref('overview')
const tabs = [
  { key: 'overview', label: '概览' },
  { key: 'chart', label: 'K线图' },
  { key: 'analysis', label: '分析报告' },
  { key: 'financial', label: '财务数据' },
  { key: 'news', label: '新闻' }
]

const quote = ref({
  price: 0,
  changePercent: 0,
  open: 0,
  high: 0,
  low: 0,
  prevClose: 0,
  volume: 0,
  amount: 0,
  turnover: 0,
  amplitude: 0
})

const basicInfo = ref({
  industry: '',
  marketCap: 0,
  pe: '',
  pb: '',
  description: ''
})

const reports = ref<any[]>([])
const news = ref<any[]>([])
const financialData = ref({ columns: [] as string[], rows: [] as any[] })
const chartRef = ref<HTMLElement>()

const refreshText = computed(() => quote.value.price ? '实时' : '暂无数据')
const changeClass = computed(() => {
  if (quote.value.changePercent > 0) return 'text-[#EF4444]'
  if (quote.value.changePercent < 0) return 'text-[#22C55E]'
  return ''
})

const getMarketClass = (): string => {
  const classMap: Record<string, string> = {
    'A': 'bg-[#EF4444]/20 text-[#EF4444]',
    'HK': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'US': 'bg-[#3B82F6]/20 text-[#3B82F6]'
  }
  return classMap[market.value] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const fmtPrice = (v: number) => v ? v.toFixed(2) : '-'
const fmtPercent = (v: number) => v ? (v > 0 ? '+' : '') + v.toFixed(2) + '%' : '-'
const fmtVolume = (v: number) => v >= 1e8 ? (v / 1e8).toFixed(2) + '亿' : v >= 1e4 ? (v / 1e4).toFixed(2) + '万' : String(v)
const fmtAmount = (v: number) => v >= 1e8 ? (v / 1e8).toFixed(2) + '亿' : v >= 1e4 ? (v / 1e4).toFixed(2) + '万' : String(v)
const formatTime = (t: string) => new Date(t).toLocaleString('zh-CN')

const getRecommendationClass = (rec: string): string => {
  const classMap: Record<string, string> = {
    '买入': 'bg-[#EF4444]/20 text-[#EF4444]',
    '持有': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    '卖出': 'bg-[#22C55E]/20 text-[#22C55E]'
  }
  return classMap[rec] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const loadStockData = async () => {
  try {
    const res = await stockApi.getDetail(code.value, market.value)
    stockName.value = res.data?.name || ''
    quote.value = res.data?.quote || quote.value
    basicInfo.value = res.data?.basic || basicInfo.value
    reports.value = res.data?.reports || []
    news.value = res.data?.news || []
    financialData.value = res.data?.financial || financialData.value
    isFav.value = res.data?.isFavorite || false
  } catch (error) {
    console.error('加载股票数据失败:', error)
  }
}

const refreshQuote = async () => {
  try {
    const res = await stockApi.getQuote(code.value, market.value)
    quote.value = res.data || quote.value
    ElMessage.success('已刷新')
  } catch (error) {
    ElMessage.error('刷新失败')
  }
}

const onToggleFavorite = async () => {
  try {
    await stockApi.toggleFavorite(code.value)
    isFav.value = !isFav.value
    ElMessage.success(isFav.value ? '已添加自选' : '已移除自选')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const showSyncDialog = () => syncDialogVisible.value = true

const doSync = async () => {
  syncLoading.value = true
  try {
    await stockApi.syncData(code.value, syncType.value)
    ElMessage.success('同步成功')
    syncDialogVisible.value = false
    loadStockData()
  } catch (error) {
    ElMessage.error('同步失败')
  } finally {
    syncLoading.value = false
  }
}

const goPaperTrading = () => router.push(`/paper?code=${code.value}`)
const viewReport = (report: any) => router.push(`/reports/${report.id}`)

const renderChart = () => {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: [] },
    yAxis: { type: 'value', scale: true },
    series: [{ type: 'candlestick', data: [] }]
  })
}

watch(code, loadStockData, { immediate: true })
watch(activeTab, (tab) => {
  if (tab === 'chart') {
    setTimeout(renderChart, 100)
  }
})
</script>
