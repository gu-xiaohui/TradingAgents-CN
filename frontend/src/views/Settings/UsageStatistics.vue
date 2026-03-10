<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
        </svg>
        使用统计与计费
      </h1>
      <div class="flex items-center gap-3">
        <select v-model="selectedDays" @change="loadData" class="px-4 py-2 bg-[var(--bg-secondary)] border border-[var(--border-color)] rounded-lg text-sm">
          <option :value="7">最近7天</option>
          <option :value="30">最近30天</option>
          <option :value="90">最近90天</option>
        </select>
        <button 
          @click="loadData" 
          :disabled="loading"
          class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <div class="flex items-center gap-2 text-[var(--text-secondary)] text-sm mb-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          总请求数
        </div>
        <div class="text-2xl font-bold text-[#22C55E]">{{ statistics.total_requests.toLocaleString() }}</div>
      </div>
      
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <div class="flex items-center gap-2 text-[var(--text-secondary)] text-sm mb-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
          </svg>
          总输入 Token
        </div>
        <div class="text-2xl font-bold text-[#3B82F6]">{{ statistics.total_input_tokens.toLocaleString() }}</div>
      </div>
      
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <div class="flex items-center gap-2 text-[var(--text-secondary)] text-sm mb-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M13.5 12H3m0 0l4.5-4.5M3 12l4.5 4.5M21 12h-9m9 0l-4.5 4.5M21 12l-4.5-4.5" />
          </svg>
          总输出 Token
        </div>
        <div class="text-2xl font-bold text-[#8B5CF6]">{{ statistics.total_output_tokens.toLocaleString() }}</div>
      </div>
      
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <div class="flex items-center gap-2 text-[var(--text-secondary)] text-sm mb-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          总成本
        </div>
        <div v-if="Object.keys(statistics.cost_by_currency || {}).length > 0" class="space-y-1">
          <div v-for="(cost, currency) in statistics.cost_by_currency" :key="currency" class="flex items-baseline gap-1">
            <span class="text-2xl font-bold text-[#F59E0B]">{{ cost.toFixed(4) }}</span>
            <span class="text-sm text-[var(--text-secondary)]">{{ getCurrencySymbol(currency) }}</span>
          </div>
        </div>
        <div v-else class="flex items-baseline gap-1">
          <span class="text-2xl font-bold text-[#F59E0B]">0.0000</span>
          <span class="text-sm text-[var(--text-secondary)]">元</span>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">按供应商统计</h3>
        <div ref="providerChartRef" style="height: 300px;"></div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">按模型统计</h3>
        <div ref="modelChartRef" style="height: 300px;"></div>
      </div>
    </div>

    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 mb-6">
      <h3 class="text-lg font-semibold mb-4">每日成本趋势</h3>
      <div ref="dailyChartRef" style="height: 300px;"></div>
    </div>

    <!-- 使用记录表格 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">使用记录</h3>
        <button 
          @click="handleDeleteOldRecords"
          class="px-3 py-1.5 text-sm bg-[#EF4444] hover:bg-[#DC2626] text-white rounded-lg transition-colors"
        >
          清理旧记录
        </button>
      </div>

      <div v-if="loading" class="flex items-center justify-center py-8">
        <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">时间</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">供应商</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">模型</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">输入 Token</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">输出 Token</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">成本</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">分析类型</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">会话ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.id" class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)]">
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatTimestamp(record.timestamp) }}</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 bg-[#3B82F6]/20 text-[#3B82F6] rounded text-xs">{{ record.provider }}</span>
              </td>
              <td class="py-3 px-4 font-mono text-sm">{{ record.model_name }}</td>
              <td class="py-3 px-4 text-right">{{ record.input_tokens.toLocaleString() }}</td>
              <td class="py-3 px-4 text-right">{{ record.output_tokens.toLocaleString() }}</td>
              <td class="py-3 px-4 text-right font-medium text-[#F59E0B]">
                {{ record.cost.toFixed(4) }} {{ getCurrencySymbol(record.currency || 'CNY') }}
              </td>
              <td class="py-3 px-4 text-sm">{{ record.analysis_type }}</td>
              <td class="py-3 px-4 text-xs text-[var(--text-secondary)] font-mono truncate max-w-[120px]">{{ record.session_id }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 分页 -->
      <div v-if="records.length > 0" class="flex items-center justify-between mt-4 pt-4 border-t border-[var(--border-color)]">
        <div class="text-sm text-[var(--text-secondary)]">
          共 {{ totalRecords }} 条记录
        </div>
        <div class="flex items-center gap-2">
          <select v-model="pageSize" @change="loadRecords" class="px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option :value="10">10 条/页</option>
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
            <option :value="100">100 条/页</option>
          </select>
          <button 
            v-for="p in Math.min(5, Math.ceil(totalRecords / pageSize))" 
            :key="p"
            @click="currentPage = p; loadRecords()"
            :class="currentPage === p ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)]'"
            class="w-8 h-8 rounded-lg text-sm transition-colors"
          >
            {{ p }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'
import {
  getUsageRecords,
  getUsageStatistics,
  deleteOldRecords,
  type UsageRecord,
  type UsageStatistics
} from '@/api/usage'

// 数据
const selectedDays = ref(7)
const loading = ref(false)
const statistics = ref<UsageStatistics>({
  total_requests: 0,
  total_input_tokens: 0,
  total_output_tokens: 0,
  total_cost: 0,
  cost_by_currency: {},
  by_provider: {},
  by_model: {},
  by_date: {}
})
const records = ref<UsageRecord[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// 图表引用
const providerChartRef = ref<HTMLElement>()
const modelChartRef = ref<HTMLElement>()
const dailyChartRef = ref<HTMLElement>()

// 图表实例
let providerChart: echarts.ECharts | null = null
let modelChart: echarts.ECharts | null = null
let dailyChart: echarts.ECharts | null = null

// 格式化时间戳
const formatTimestamp = (timestamp: string) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

// 获取货币符号
const getCurrencySymbol = (currency: string) => {
  const symbols: Record<string, string> = {
    'CNY': '元',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥'
  }
  return symbols[currency] || currency
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const res = await getUsageStatistics({ days: selectedDays.value })
    if (res.success) {
      statistics.value = res.data
      await nextTick()
      renderCharts()
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

// 加载使用记录
const loadRecords = async () => {
  try {
    loading.value = true
    const res = await getUsageRecords({
      limit: pageSize.value
    })
    if (res.success) {
      records.value = res.data.records
      totalRecords.value = res.data.total
    }
  } catch (error) {
    console.error('加载使用记录失败:', error)
    ElMessage.error('加载使用记录失败')
  } finally {
    loading.value = false
  }
}

// 加载所有数据
const loadData = async () => {
  await Promise.all([loadStatistics(), loadRecords()])
}

// 渲染图表
const renderCharts = () => {
  renderProviderChart()
  renderModelChart()
  renderDailyChart()
}

// 渲染供应商图表
const renderProviderChart = () => {
  if (!providerChartRef.value) return

  if (!providerChart) {
    providerChart = echarts.init(providerChartRef.value)
  }

  const data = Object.entries(statistics.value.by_provider).map(([name, value]: [string, any]) => ({
    name,
    value: value.cost
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: ¥{c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: { color: 'var(--text-secondary)' }
    },
    series: [
      {
        name: '成本',
        type: 'pie',
        radius: '50%',
        data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }

  providerChart.setOption(option)
}

// 渲染模型图表
const renderModelChart = () => {
  if (!modelChartRef.value) return

  if (!modelChart) {
    modelChart = echarts.init(modelChartRef.value)
  }

  const data = Object.entries(statistics.value.by_model)
    .map(([name, value]: [string, any]) => ({
      name,
      value: value.cost
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10)

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        rotate: 45,
        interval: 0,
        color: 'var(--text-secondary)'
      }
    },
    yAxis: {
      type: 'value',
      name: '成本(元)',
      nameTextStyle: { color: 'var(--text-secondary)' },
      axisLabel: { color: 'var(--text-secondary)' }
    },
    series: [
      {
        data: data.map(item => item.value),
        type: 'bar',
        itemStyle: { color: '#22C55E' }
      }
    ]
  }

  modelChart.setOption(option)
}

// 渲染每日成本图表
const renderDailyChart = () => {
  if (!dailyChartRef.value) return

  if (!dailyChart) {
    dailyChart = echarts.init(dailyChartRef.value)
  }

  const sortedData = Object.entries(statistics.value.by_date)
    .sort(([a], [b]) => a.localeCompare(b))

  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: sortedData.map(([date]) => date),
      axisLabel: { color: 'var(--text-secondary)' }
    },
    yAxis: {
      type: 'value',
      name: '成本(元)',
      nameTextStyle: { color: 'var(--text-secondary)' },
      axisLabel: { color: 'var(--text-secondary)' }
    },
    series: [
      {
        data: sortedData.map(([, value]: [string, any]) => value.cost),
        type: 'line',
        smooth: true,
        itemStyle: { color: '#22C55E' },
        areaStyle: { color: 'rgba(34, 197, 94, 0.2)' }
      }
    ]
  }

  dailyChart.setOption(option)
}

// 删除旧记录
const handleDeleteOldRecords = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除90天前的旧记录吗？此操作不可恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const res = await deleteOldRecords(90)
    if (res.data?.success) {
      ElMessage.success(`已删除 ${res.data.deleted_count} 条旧记录`)
      loadData()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除旧记录失败:', error)
      ElMessage.error('删除旧记录失败')
    }
  }
}

// 组件挂载
onMounted(() => {
  loadData()
})
</script>
