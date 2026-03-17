<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        股票筛选
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">多维度筛选条件，快速找到符合投资策略的优质股票</p>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：筛选条件 -->
      <div class="col-span-3">
        <div class="card sticky top-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold">筛选条件</h2>
            <button @click="resetFilters" class="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)]">重置</button>
          </div>

          <!-- 市场类型 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">市场类型</label>
            <select v-model="filters.market" class="input">
              <option value="A股">🇨🇳 A股市场</option>
            </select>
          </div>

          <!-- 行业分类 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">行业分类</label>
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <label v-for="industry in industryOptions" :key="industry.value" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 cursor-pointer">
                <input type="checkbox" v-model="filters.industries" :value="industry.value" class="w-4 h-4 accent-[#22C55E]" />
                <span class="text-sm text-[var(--text-primary)]">{{ industry.label }}</span>
              </label>
            </div>
          </div>

          <!-- 市值范围 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">市值范围</label>
            <select v-model="filters.marketCapRange" class="input">
              <option value="">全部</option>
              <option value="small">小盘股 (&lt; 100亿)</option>
              <option value="medium">中盘股 (100-500亿)</option>
              <option value="large">大盘股 (&gt; 500亿)</option>
            </select>
          </div>

          <!-- 市盈率 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">市盈率 (PE)</label>
            <div class="flex items-center gap-2">
              <input v-model.number="filters.peMin" type="number" placeholder="最小" class="input text-sm w-20" />
              <span class="text-[var(--text-muted)]">-</span>
              <input v-model.number="filters.peMax" type="number" placeholder="最大" class="input text-sm w-20" />
            </div>
          </div>

          <!-- 涨跌幅 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">今日涨跌幅</label>
            <div class="flex items-center gap-2">
              <input v-model.number="filters.changeMin" type="number" placeholder="最小%" class="input text-sm w-20" />
              <span class="text-[var(--text-muted)]">-</span>
              <input v-model.number="filters.changeMax" type="number" placeholder="最大%" class="input text-sm w-20" />
            </div>
          </div>

          <!-- 筛选按钮 -->
          <button @click="applyFilters" class="btn-primary w-full flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            开始筛选
          </button>
        </div>
      </div>

      <!-- 右侧：筛选结果 -->
      <div class="col-span-9">
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-lg font-semibold">筛选结果</h2>
              <p class="text-sm text-[var(--text-muted)] mt-1">共找到 {{ filteredStocks.length }} 只符合条件的股票</p>
            </div>
            <div class="flex items-center gap-3">
              <select v-model="sortBy" class="input text-sm w-40">
                <option value="change_desc">涨跌幅 ↓</option>
                <option value="change_asc">涨跌幅 ↑</option>
                <option value="market_cap_desc">市值 ↓</option>
                <option value="pe_asc">市盈率 ↑</option>
              </select>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading" class="text-center py-16">
            <svg class="animate-spin w-8 h-8 mx-auto mb-4 text-[#22C55E]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <p class="text-[var(--text-muted)]">正在加载股票数据...</p>
          </div>

          <!-- 股票列表 -->
          <div v-else-if="filteredStocks.length > 0" class="space-y-3">
            <div
              v-for="stock in filteredStocks"
              :key="stock.code"
              class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
              @click="goToDetail(stock.code)"
            >
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[#22C55E]/20 to-[#8B5CF6]/20 flex items-center justify-center">
                  <span class="text-lg font-bold text-[#22C55E]">{{ stock.code.slice(-2) }}</span>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="font-mono font-medium text-[var(--text-primary)]">{{ stock.code }}</span>
                    <span class="badge-info text-xs">{{ stock.industry }}</span>
                  </div>
                  <div class="text-sm text-[var(--text-secondary)] mt-1">{{ stock.name }}</div>
                </div>
              </div>
              
              <div class="flex items-center gap-8">
                <div class="text-right">
                  <div class="text-sm text-[var(--text-muted)]">现价</div>
                  <div class="text-lg font-semibold text-[var(--text-primary)]">¥{{ stock.price.toFixed(2) }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[var(--text-muted)]">涨跌幅</div>
                  <div :class="stock.change >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'" class="text-lg font-semibold">
                    {{ stock.change >= 0 ? '+' : '' }}{{ stock.change.toFixed(2) }}%
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[var(--text-muted)]">市盈率</div>
                  <div class="text-lg font-semibold text-[var(--text-primary)]">{{ stock.pe.toFixed(2) }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[var(--text-muted)]">市值</div>
                  <div class="text-lg font-semibold text-[var(--text-primary)]">{{ formatMarketCap(stock.marketCap) }}</div>
                </div>
                <div class="flex items-center gap-3">
                  <button
                    class="text-sm text-blue-400 hover:text-blue-300"
                    @click.stop="goToDetail(stock.code)"
                  >
                    详情
                  </button>
                  <button
                    class="text-sm text-emerald-400 hover:text-emerald-300"
                    @click.stop="goToAnalysis(stock.code)"
                  >
                    分析
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else class="text-center py-16">
            <svg class="w-16 h-16 mx-auto mb-4 text-[var(--text-muted)] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <p class="text-[var(--text-muted)]">暂无符合条件的股票</p>
            <p class="text-sm text-[var(--text-muted)] mt-2">请调整筛选条件后重试</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMarketByStockCode } from '@/utils/market'
import { screeningApi } from '@/api/screening'

const router = useRouter()

const loading = ref(false)

const filters = reactive({
  market: 'A股',
  industries: [] as string[],
  marketCapRange: '',
  peMin: null as number | null,
  peMax: null as number | null,
  changeMin: null as number | null,
  changeMax: null as number | null,
})

const sortBy = ref('change_desc')

const industryOptions = ref([
  { value: 'technology', label: '科技' },
  { value: 'finance', label: '金融' },
  { value: 'healthcare', label: '医疗' },
  { value: 'consumer', label: '消费' },
  { value: 'energy', label: '能源' },
  { value: 'materials', label: '材料' },
  { value: 'industrial', label: '工业' },
  { value: 'realestate', label: '房地产' },
])

const allStocks = ref<Array<{ code: string; name: string; price: number; change: number; pe: number; marketCap: number; industry: string }>>([])

// 从后端加载行业选项
const loadIndustries = async () => {
  try {
    const res = await screeningApi.getIndustries()
    if (res.success && res.data?.industries?.length) {
      industryOptions.value = res.data.industries.map((item: any) => ({
        value: item.value || item.label,
        label: item.label
      }))
    }
  } catch {
    // 保持默认行业选项
  }
}

// 构建筛选条件并调用后端 API
const fetchStocks = async () => {
  loading.value = true
  try {
    const conditions: Record<string, any> = {}

    // 市值筛选条件（单位：万元，需要转换）
    if (filters.marketCapRange === 'small') {
      conditions.total_mv = { max: 1000000 } // < 100亿 = 1000000万元
    } else if (filters.marketCapRange === 'medium') {
      conditions.total_mv = { min: 1000000, max: 5000000 } // 100-500亿
    } else if (filters.marketCapRange === 'large') {
      conditions.total_mv = { min: 5000000 } // > 500亿
    }

    // PE 筛选
    if (filters.peMin !== null || filters.peMax !== null) {
      conditions.pe = {}
      if (filters.peMin !== null) conditions.pe.min = filters.peMin
      if (filters.peMax !== null) conditions.pe.max = filters.peMax
    }

    // 涨跌幅筛选
    if (filters.changeMin !== null || filters.changeMax !== null) {
      conditions.pct_chg = {}
      if (filters.changeMin !== null) conditions.pct_chg.min = filters.changeMin
      if (filters.changeMax !== null) conditions.pct_chg.max = filters.changeMax
    }

    // 排序映射
    const orderByMap: Record<string, { field: string; direction: 'asc' | 'desc' }[]> = {
      'change_desc': [{ field: 'pct_chg', direction: 'desc' }],
      'change_asc': [{ field: 'pct_chg', direction: 'asc' }],
      'market_cap_desc': [{ field: 'total_mv', direction: 'desc' }],
      'pe_asc': [{ field: 'pe', direction: 'asc' }],
    }

    const res = await screeningApi.run({
      market: 'CN',
      conditions,
      order_by: orderByMap[sortBy.value] || [{ field: 'pct_chg', direction: 'desc' }],
      limit: 50,
      offset: 0,
    })

    if (res.success && res.data) {
      allStocks.value = (res.data.items || []).map((item: any) => ({
        code: item.code || '',
        name: item.name || '',
        price: item.close ?? 0,
        change: item.pct_chg ?? 0,
        pe: item.pe ?? 0,
        marketCap: (item.total_mv ?? 0) * 10000, // 万元转元
        industry: item.industry || '-',
      }))
    }
  } catch {
    ElMessage.error('加载股票数据失败，请检查后端服务是否正常')
  } finally {
    loading.value = false
  }
}

const filteredStocks = computed(() => {
  let result = [...allStocks.value]

  // 行业筛选（前端过滤，因为后端可能不支持行业条件）
  if (filters.industries.length > 0) {
    result = result.filter(s => filters.industries.some(ind => s.industry.includes(ind)))
  }

  return result
})

const resetFilters = () => {
  filters.industries = []
  filters.marketCapRange = ''
  filters.peMin = null
  filters.peMax = null
  filters.changeMin = null
  filters.changeMax = null
  fetchStocks()
}

const applyFilters = () => {
  fetchStocks()
}

onMounted(() => {
  loadIndustries()
  fetchStocks()
})

const formatMarketCap = (cap: number) => {
  if (cap >= 1000000000000) {
    return (cap / 1000000000000).toFixed(2) + '万亿'
  } else if (cap >= 100000000) {
    return (cap / 100000000).toFixed(2) + '亿'
  }
  return (cap / 10000).toFixed(2) + '万'
}

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
</script>
