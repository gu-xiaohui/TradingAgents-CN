<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#8B5CF6] to-[#EC4899] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 0 0-2.25-2.25H15a3 3 0 1 1-6 0H5.25A2.25 2.25 0 0 0 3 12m18 0v6a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 9m18 0V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v3" />
          </svg>
        </div>
        模拟交易
      </h1>
      <p class="text-[var(--text-muted)] mt-1 ml-13">零风险练习股票交易策略</p>
    </div>

    <!-- 账户概览 -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-[#22C55E]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75-.75H5.25A.75.75 0 0 0 4.5 18v.75c0 .414.336.75.75.75h.75m-1.5-1.5h14.5" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-[var(--text-muted)]">总资产</div>
            <div class="text-xl font-bold text-[#22C55E]">¥{{ formatMoney(account.totalEquity) }}</div>
          </div>
        </div>
      </div>
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-[#3B82F6]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75-.75H5.25A.75.75 0 0 0 4.5 18v.75c0 .414.336.75.75.75h.75m-1.5-1.5h14.5" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-[var(--text-muted)]">可用资金</div>
            <div class="text-xl font-bold">¥{{ formatMoney(account.cash) }}</div>
          </div>
        </div>
      </div>
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-[#8B5CF6]/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-[var(--text-muted)]">持仓市值</div>
            <div class="text-xl font-bold">¥{{ formatMoney(account.positionsValue) }}</div>
          </div>
        </div>
      </div>
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="account.totalReturn >= 0 ? 'bg-[#EF4444]/20' : 'bg-[#22C55E]/20'">
            <svg class="w-5 h-5" :class="account.totalReturn >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-[var(--text-muted)]">总收益</div>
            <div class="text-xl font-bold" :class="account.totalReturn >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'">
              {{ account.totalReturn >= 0 ? '+' : '' }}{{ formatMoney(account.totalReturn) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex items-center gap-4 mb-6">
      <button @click="showBuyDialog = true" class="btn-primary">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        买入
      </button>
      <button @click="showSellDialog = true" class="btn-secondary">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
        </svg>
        卖出
      </button>
      <button @click="refreshAccount" class="btn-secondary">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
        </svg>
        刷新
      </button>
    </div>

    <!-- 持仓列表 -->
    <div class="card">
      <h2 class="text-lg font-semibold mb-4">我的持仓</h2>
      
      <div v-if="positions.length > 0" class="space-y-3">
        <div
          v-for="pos in positions"
          :key="pos.stock_code"
          class="flex items-center justify-between p-4 rounded-xl bg-white/5"
        >
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
              <span class="font-bold text-sm">{{ pos.stock_code.slice(-2) }}</span>
            </div>
            <div>
              <div class="font-mono font-medium">{{ pos.stock_code }}</div>
              <div class="text-sm text-[var(--text-muted)]">{{ pos.stock_name }}</div>
            </div>
          </div>
          
          <div class="flex items-center gap-8">
            <div class="text-right">
              <div class="text-sm text-[var(--text-muted)]">持仓数量</div>
              <div class="font-medium">{{ pos.quantity }} 股</div>
            </div>
            <div class="text-right">
              <div class="text-sm text-[var(--text-muted)]">成本价</div>
              <div class="font-medium">¥{{ pos.cost_price.toFixed(2) }}</div>
            </div>
            <div class="text-right">
              <div class="text-sm text-[var(--text-muted)]">现价</div>
              <div class="font-medium">¥{{ (pos.current_price || 0).toFixed(2) }}</div>
            </div>
            <div class="text-right min-w-[80px]">
              <div class="text-sm text-[var(--text-muted)]">盈亏</div>
              <div class="font-medium" :class="pos.profit >= 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'">
                {{ pos.profit >= 0 ? '+' : '' }}{{ formatMoney(pos.profit) }}
              </div>
            </div>
            <button @click="sellPosition(pos)" class="btn-secondary text-sm">卖出</button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 text-[var(--text-muted)]">
        暂无持仓
      </div>
    </div>

    <!-- 买入对话框 -->
    <div v-if="showBuyDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showBuyDialog = false">
      <div class="bg-[var(--bg-secondary)] rounded-2xl p-6 w-full max-w-md border border-[var(--border-color)]">
        <h3 class="text-lg font-semibold mb-4">买入股票</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-[var(--text-secondary)] mb-2">股票代码</label>
            <input v-model="tradeForm.stockCode" type="text" placeholder="如：000001" class="input" />
          </div>
          <div>
            <label class="block text-sm text-[var(--text-secondary)] mb-2">买入价格</label>
            <input v-model.number="tradeForm.price" type="number" step="0.01" placeholder="价格" class="input" />
          </div>
          <div>
            <label class="block text-sm text-[var(--text-secondary)] mb-2">买入数量</label>
            <input v-model.number="tradeForm.quantity" type="number" placeholder="数量（股）" class="input" />
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showBuyDialog = false" class="btn-secondary">取消</button>
            <button @click="executeBuy" class="btn-primary">确认买入</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { paperApi } from '@/api/paper'

const authStore = useAuthStore()

const account = reactive({
  totalEquity: 1000000,
  cash: 800000,
  positionsValue: 200000,
  totalReturn: 0
})

const positions = ref<any[]>([])
const showBuyDialog = ref(false)
const showSellDialog = ref(false)

const tradeForm = reactive({
  stockCode: '',
  price: 0,
  quantity: 0
})

const formatMoney = (value: number) => {
  return (value || 0).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const refreshAccount = async () => {
  try {
    const response = await paperApi.getAccount()
    if (response.success && response.data) {
      const data = response.data.account || response.data
      account.totalEquity = data.equity?.CNY || data.equity || 1000000
      account.cash = data.cash?.CNY || data.cash || 800000
      account.positionsValue = data.positions_value?.CNY || data.positions_value || 200000
      account.totalReturn = data.total_return || 0
      positions.value = data.positions || []
    }
    ElMessage.success('已刷新')
  } catch (error) {
    console.error('加载账户失败:', error)
  }
}

const executeBuy = async () => {
  if (!tradeForm.stockCode || !tradeForm.price || !tradeForm.quantity) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  try {
    const response = await paperApi.buy({
      symbol: tradeForm.stockCode,
      price: tradeForm.price,
      quantity: tradeForm.quantity
    })
    
    if (response.success) {
      ElMessage.success('买入成功')
      showBuyDialog.value = false
      tradeForm.stockCode = ''
      tradeForm.price = 0
      tradeForm.quantity = 0
      await refreshAccount()
    } else {
      ElMessage.error(response.message || '买入失败')
    }
  } catch (error) {
    ElMessage.error('买入失败')
  }
}

const sellPosition = (pos: any) => {
  tradeForm.stockCode = pos.stock_code
  tradeForm.price = pos.current_price || pos.cost_price
  tradeForm.quantity = pos.quantity
  showSellDialog.value = true
}

onMounted(() => {
  refreshAccount()
})
</script>
