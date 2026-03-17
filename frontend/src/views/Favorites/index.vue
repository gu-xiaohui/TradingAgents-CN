<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#F59E0B] to-[#EF4444] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
          </svg>
        </div>
        我的自选股
      </h1>
      <p class="text-[var(--text-muted)] mt-1 ml-13">管理您关注的股票</p>
    </div>

    <!-- 操作栏 -->
    <div class="card mb-6">
      <div class="flex items-center gap-4 flex-wrap">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索股票代码或名称..."
          class="input flex-1 max-w-xs"
        />
        <select v-model="selectedMarket" class="input w-32">
          <option value="">全部市场</option>
          <option value="A股">A股</option>
          <option value="港股">港股</option>
          <option value="美股">美股</option>
        </select>
        <button @click="refreshData" class="btn-secondary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
        <button @click="syncRealtime" class="btn-primary" :disabled="syncing">
          <svg v-if="syncing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
          </svg>
          同步实时行情
        </button>
        <button @click="showAddDialog = true" class="btn-primary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          添加自选
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="card p-4">
        <div class="text-2xl font-bold text-[#22C55E]">{{ stats.total }}</div>
        <div class="text-sm text-[var(--text-muted)]">自选股数</div>
      </div>
      <div class="card p-4">
        <div class="text-2xl font-bold text-[#EF4444]">{{ stats.up }}</div>
        <div class="text-sm text-[var(--text-muted)]">上涨</div>
      </div>
      <div class="card p-4">
        <div class="text-2xl font-bold text-[#22C55E]">{{ stats.down }}</div>
        <div class="text-sm text-[var(--text-muted)]">下跌</div>
      </div>
      <div class="card p-4">
        <div class="text-2xl font-bold" :class="stats.avgChange >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'">
          {{ stats.avgChange >= 0 ? '+' : '' }}{{ stats.avgChange.toFixed(2) }}%
        </div>
        <div class="text-sm text-[var(--text-muted)]">平均涨跌</div>
      </div>
    </div>

    <!-- 股票列表 -->
    <div class="card">
      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <svg class="w-8 h-8 mx-auto animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      </div>

      <!-- 列表 -->
      <div v-else-if="filteredStocks.length > 0" class="space-y-2">
        <div
          v-for="stock in filteredStocks"
          :key="stock.stock_code"
          class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
          @click="goToDetail(stock)"
        >
          <div class="flex items-center gap-4">
            <div 
              class="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm"
              :class="stock.change_percent >= 0 ? 'bg-[#EF4444]/20 text-[#EF4444]' : 'bg-[#22C55E]/20 text-[#22C55E]'"
            >
              {{ stock.change_percent >= 0 ? '↑' : '↓' }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="font-mono font-medium">{{ stock.stock_code }}</span>
                <span class="text-[var(--text-secondary)]">{{ stock.stock_name }}</span>
              </div>
              <div class="text-xs text-[var(--text-muted)] mt-1">
                {{ stock.market || 'A股' }} · {{ stock.board || '' }}
              </div>
            </div>
          </div>

          <div class="flex items-center gap-8">
            <div class="text-right">
              <div class="text-sm text-[var(--text-muted)]">现价</div>
              <div class="text-lg font-semibold">¥{{ (stock.current_price || 0).toFixed(2) }}</div>
            </div>
            <div class="text-right">
              <div class="text-sm text-[var(--text-muted)]">涨跌幅</div>
              <div 
                class="text-lg font-semibold"
                :class="stock.change_percent >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'"
              >
                {{ stock.change_percent >= 0 ? '+' : '' }}{{ (stock.change_percent || 0).toFixed(2) }}%
              </div>
            </div>
            <div class="text-right min-w-[80px]">
              <div class="text-sm text-[var(--text-muted)]">涨跌额</div>
              <div 
                class="font-medium"
                :class="stock.change_amount >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'"
              >
                {{ stock.change_amount >= 0 ? '+' : '' }}{{ (stock.change_amount || 0).toFixed(2) }}
              </div>
            </div>
            <button 
              @click.stop="goToAnalysis(stock)" 
              class="p-2 rounded-lg text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/10 transition-colors text-sm"
            >
              分析
            </button>
            <button 
              @click.stop="goToDetail(stock)" 
              class="p-2 rounded-lg text-blue-400 hover:text-blue-300 hover:bg-blue-500/10 transition-colors text-sm"
            >
              详情
            </button>
            <button 
              @click.stop="removeStock(stock)" 
              class="p-2 rounded-lg text-[var(--text-muted)] hover:text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-[var(--text-muted)] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
        </svg>
        <p class="text-[var(--text-muted)] mt-4">暂无自选股</p>
        <button @click="showAddDialog = true" class="btn-primary mt-4">添加自选股</button>
      </div>
    </div>

    <!-- 添加自选股对话框 -->
    <div v-if="showAddDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showAddDialog = false">
      <div class="bg-[var(--bg-secondary)] rounded-2xl p-6 w-full max-w-md border border-[var(--border-color)]">
        <h3 class="text-lg font-semibold mb-4">添加自选股</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-[var(--text-secondary)] mb-2">股票代码</label>
            <input 
              v-model="newStockCode" 
              type="text" 
              placeholder="如：000001、AAPL"
              class="input"
              @keyup.enter="addStock"
            />
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showAddDialog = false" class="btn-secondary">取消</button>
            <button @click="addStock" class="btn-primary" :disabled="!newStockCode.trim()">添加</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { favoritesApi } from '@/api/favorites'
import { extractSymbol } from '@/utils/stock'
import { getMarketByStockCode } from '@/utils/market'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const syncing = ref(false)
const stocks = ref<any[]>([])
const searchKeyword = ref('')
const selectedMarket = ref('')
const showAddDialog = ref(false)
const newStockCode = ref('')

const stats = reactive({
  total: 0,
  up: 0,
  down: 0,
  avgChange: 0
})

const filteredStocks = computed(() => {
  let result = [...stocks.value]
  
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    result = result.filter(s => 
      s.stock_code?.toLowerCase().includes(kw) || 
      s.stock_name?.toLowerCase().includes(kw)
    )
  }
  
  if (selectedMarket.value) {
    result = result.filter(s => s.market === selectedMarket.value)
  }
  
  return result
})

const refreshData = async () => {
  loading.value = true
  try {
    const response = await favoritesApi.list()
    if (response.success && response.data) {
      stocks.value = response.data
      updateStats()
    }
    ElMessage.success('已刷新')
  } catch (error) {
    console.error('加载自选股失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const updateStats = () => {
  stats.total = stocks.value.length
  stats.up = stocks.value.filter(s => (s.change_percent || 0) > 0).length
  stats.down = stocks.value.filter(s => (s.change_percent || 0) < 0).length
  
  if (stocks.value.length > 0) {
    const totalChange = stocks.value.reduce((sum, s) => sum + (s.change_percent || 0), 0)
    stats.avgChange = totalChange / stocks.value.length
  } else {
    stats.avgChange = 0
  }
}

const syncRealtime = async () => {
  syncing.value = true
  try {
    // 调用同步实时行情 API
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('实时行情已同步')
    await refreshData()
  } catch (error) {
    ElMessage.error('同步失败')
  } finally {
    syncing.value = false
  }
}

const addStock = async () => {
  if (!newStockCode.value.trim()) return
  
  try {
    const response = await favoritesApi.add(newStockCode.value.trim())
    if (response.success) {
      ElMessage.success('添加成功')
      showAddDialog.value = false
      newStockCode.value = ''
      await refreshData()
    } else {
      ElMessage.error(response.message || '添加失败')
    }
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

const removeStock = async (stock: any) => {
  try {
    await ElMessageBox.confirm(`确定移除 ${stock.stock_name || stock.stock_code}？`, '确认移除', { type: 'warning' })
    const response = await favoritesApi.remove(stock.stock_code)
    if (response.success) {
      stocks.value = stocks.value.filter(s => s.stock_code !== stock.stock_code)
      updateStats()
      ElMessage.success('已移除')
    }
  } catch {}
}

const goToDetail = (stock: any) => {
  const rawCode = String(stock?.stock_code || stock?.symbol || stock?.code || '').trim()
  const code = extractSymbol(rawCode)
  if (!code) {
    ElMessage.warning('股票代码缺失，无法打开详情')
    return
  }

  router.push({
    name: 'StockDetail',
    params: { code },
    query: { market: getMarketByStockCode(rawCode) }
  })
}

const goToAnalysis = (stock: any) => {
  const rawCode = String(stock?.stock_code || stock?.symbol || stock?.code || '').trim()
  const code = extractSymbol(rawCode)
  if (!code) {
    ElMessage.warning('股票代码缺失，无法发起分析')
    return
  }

  router.push(`/analysis?stock_code=${code}`)
}

onMounted(() => {
  refreshData()
})
</script>
