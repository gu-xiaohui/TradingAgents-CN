<template>
  <div class="min-h-screen bg-[#020617] text-[#F8FAFC] p-6">
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
      <p class="text-[#94A3B8] mt-2 ml-13">多维度筛选条件，快速找到符合投资策略的优质股票</p>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：筛选条件 -->
      <div class="col-span-3">
        <div class="card sticky top-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold">筛选条件</h2>
            <button @click="resetFilters" class="text-sm text-[#94A3B8] hover:text-[#F8FAFC]">重置</button>
          </div>

          <!-- 市场类型 -->
          <div class="mb-6">
            <label class="block text-sm text-[#94A3B8] mb-2">市场类型</label>
            <select v-model="filters.market" class="input">
              <option value="A股">🇨🇳 A股市场</option>
            </select>
          </div>

          <!-- 行业分类 -->
          <div class="mb-6">
            <label class="block text-sm text-[#94A3B8] mb-2">行业分类</label>
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <label v-for="industry in industryOptions" :key="industry.value" class="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 cursor-pointer">
                <input type="checkbox" v-model="filters.industries" :value="industry.value" class="w-4 h-4 accent-[#22C55E]" />
                <span class="text-sm text-[#F8FAFC]">{{ industry.label }}</span>
              </label>
            </div>
          </div>

          <!-- 市值范围 -->
          <div class="mb-6">
            <label class="block text-sm text-[#94A3B8] mb-2">市值范围</label>
            <select v-model="filters.marketCapRange" class="input">
              <option value="">全部</option>
              <option value="small">小盘股 (&lt; 100亿)</option>
              <option value="medium">中盘股 (100-500亿)</option>
              <option value="large">大盘股 (&gt; 500亿)</option>
            </select>
          </div>

          <!-- 市盈率 -->
          <div class="mb-6">
            <label class="block text-sm text-[#94A3B8] mb-2">市盈率 (PE)</label>
            <div class="flex items-center gap-2">
              <input v-model.number="filters.peMin" type="number" placeholder="最小" class="input text-sm w-20" />
              <span class="text-[#64748B]">-</span>
              <input v-model.number="filters.peMax" type="number" placeholder="最大" class="input text-sm w-20" />
            </div>
          </div>

          <!-- 涨跌幅 -->
          <div class="mb-6">
            <label class="block text-sm text-[#94A3B8] mb-2">今日涨跌幅</label>
            <div class="flex items-center gap-2">
              <input v-model.number="filters.changeMin" type="number" placeholder="最小%" class="input text-sm w-20" />
              <span class="text-[#64748B]">-</span>
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
              <p class="text-sm text-[#64748B] mt-1">共找到 {{ filteredStocks.length }} 只符合条件的股票</p>
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

          <!-- 股票列表 -->
          <div v-if="filteredStocks.length > 0" class="space-y-3">
            <div
              v-for="stock in filteredStocks"
              :key="stock.code"
              class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
              @click="goToAnalysis(stock.code)"
            >
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[#22C55E]/20 to-[#8B5CF6]/20 flex items-center justify-center">
                  <span class="text-lg font-bold text-[#22C55E]">{{ stock.code.slice(-2) }}</span>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="font-mono font-medium text-[#F8FAFC]">{{ stock.code }}</span>
                    <span class="badge-info text-xs">{{ stock.industry }}</span>
                  </div>
                  <div class="text-sm text-[#94A3B8] mt-1">{{ stock.name }}</div>
                </div>
              </div>
              
              <div class="flex items-center gap-8">
                <div class="text-right">
                  <div class="text-sm text-[#64748B]">现价</div>
                  <div class="text-lg font-semibold text-[#F8FAFC]">¥{{ stock.price.toFixed(2) }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[#64748B]">涨跌幅</div>
                  <div :class="stock.change >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'" class="text-lg font-semibold">
                    {{ stock.change >= 0 ? '+' : '' }}{{ stock.change.toFixed(2) }}%
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[#64748B]">市盈率</div>
                  <div class="text-lg font-semibold text-[#F8FAFC]">{{ stock.pe.toFixed(2) }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm text-[#64748B]">市值</div>
                  <div class="text-lg font-semibold text-[#F8FAFC]">{{ formatMarketCap(stock.marketCap) }}</div>
                </div>
                <svg class="w-5 h-5 text-[#64748B]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else class="text-center py-16">
            <svg class="w-16 h-16 mx-auto mb-4 text-[#64748B] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <p class="text-[#64748B]">暂无符合条件的股票</p>
            <p class="text-sm text-[#64748B] mt-2">请调整筛选条件后重试</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

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

const industryOptions = [
  { value: 'technology', label: '科技' },
  { value: 'finance', label: '金融' },
  { value: 'healthcare', label: '医疗' },
  { value: 'consumer', label: '消费' },
  { value: 'energy', label: '能源' },
  { value: 'materials', label: '材料' },
  { value: 'industrial', label: '工业' },
  { value: 'realestate', label: '房地产' },
]

// 模拟数据
const allStocks = ref([
  { code: '000001', name: '平安银行', price: 12.34, change: 2.56, pe: 5.67, marketCap: 240000000000, industry: '金融' },
  { code: '000002', name: '万科A', price: 8.90, change: -1.23, pe: 8.45, marketCap: 180000000000, industry: '房地产' },
  { code: '000063', name: '中兴通讯', price: 28.50, change: 5.67, pe: 22.34, marketCap: 120000000000, industry: '科技' },
  { code: '000333', name: '美的集团', price: 56.78, change: 1.89, pe: 12.56, marketCap: 380000000000, industry: '消费' },
  { code: '000651', name: '格力电器', price: 35.20, change: -0.56, pe: 9.87, marketCap: 200000000000, industry: '消费' },
  { code: '000858', name: '五粮液', price: 145.60, change: 3.45, pe: 25.67, marketCap: 560000000000, industry: '消费' },
])

const filteredStocks = computed(() => {
  let result = [...allStocks.value]
  
  // 市值筛选
  if (filters.marketCapRange) {
    if (filters.marketCapRange === 'small') {
      result = result.filter(s => s.marketCap < 10000000000)
    } else if (filters.marketCapRange === 'medium') {
      result = result.filter(s => s.marketCap >= 10000000000 && s.marketCap <= 50000000000)
    } else if (filters.marketCapRange === 'large') {
      result = result.filter(s => s.marketCap > 50000000000)
    }
  }
  
  // PE 筛选
  if (filters.peMin !== null) {
    result = result.filter(s => s.pe >= filters.peMin!)
  }
  if (filters.peMax !== null) {
    result = result.filter(s => s.pe <= filters.peMax!)
  }
  
  // 涨跌幅筛选
  if (filters.changeMin !== null) {
    result = result.filter(s => s.change >= filters.changeMin!)
  }
  if (filters.changeMax !== null) {
    result = result.filter(s => s.change <= filters.changeMax!)
  }
  
  // 排序
  if (sortBy.value === 'change_desc') {
    result.sort((a, b) => b.change - a.change)
  } else if (sortBy.value === 'change_asc') {
    result.sort((a, b) => a.change - b.change)
  } else if (sortBy.value === 'market_cap_desc') {
    result.sort((a, b) => b.marketCap - a.marketCap)
  } else if (sortBy.value === 'pe_asc') {
    result.sort((a, b) => a.pe - b.pe)
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
}

const applyFilters = () => {
  // 筛选逻辑已在 computed 中实现
}

const formatMarketCap = (cap: number) => {
  if (cap >= 1000000000000) {
    return (cap / 1000000000000).toFixed(2) + '万亿'
  } else if (cap >= 100000000) {
    return (cap / 100000000).toFixed(2) + '亿'
  }
  return (cap / 10000).toFixed(2) + '万'
}

const goToAnalysis = (code: string) => {
  router.push(`/analysis/single?stock=${code}`)
}
</script>
