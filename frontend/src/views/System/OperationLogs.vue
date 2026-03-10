<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        操作日志
      </h1>
      <p class="text-[var(--text-secondary)] mt-1">系统操作日志查看、过滤和分析</p>
    </div>

    <!-- 筛选控制面板 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-4 mb-6">
      <div class="flex flex-wrap items-end gap-4">
        <div class="flex-1 min-w-[200px]">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">时间范围</label>
          <input type="datetime-local" v-model="filterForm.startDate" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
        </div>
        <div class="flex-1 min-w-[200px]">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">至</label>
          <input type="datetime-local" v-model="filterForm.endDate" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
        </div>
        <div class="w-40">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">操作类型</label>
          <select v-model="filterForm.actionType" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option value="">全部类型</option>
            <option value="stock_analysis">股票分析</option>
            <option value="config_management">配置管理</option>
            <option value="cache_operation">缓存操作</option>
            <option value="data_import">数据导入</option>
            <option value="data_export">数据导出</option>
            <option value="system_settings">系统设置</option>
          </select>
        </div>
        <div class="w-32">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">操作状态</label>
          <select v-model="filterForm.success" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option value="">全部状态</option>
            <option value="true">成功</option>
            <option value="false">失败</option>
          </select>
        </div>
        <div class="flex-1 min-w-[180px]">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">关键词</label>
          <input type="text" v-model="filterForm.keyword" placeholder="搜索操作内容" 
                 class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm"
                 @keyup.enter="loadLogs">
        </div>
        <div class="flex gap-2">
          <button @click="loadLogs" :disabled="loading" 
                  class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            查询
          </button>
          <button @click="resetFilter" 
                  class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            重置
          </button>
          <button @click="exportLogs" 
                  class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            导出
          </button>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#22C55E]">{{ stats.totalLogs }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">总日志数</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#3B82F6]">{{ stats.successLogs }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">成功操作</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#EF4444]">{{ stats.failedLogs }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">失败操作</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#8B5CF6]">{{ stats.successRate }}%</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">成功率</div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">操作类型分布</h3>
        <div ref="actionTypeChart" style="height: 250px;"></div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">操作趋势</h3>
        <div ref="operationTrendChart" style="height: 250px;"></div>
      </div>
    </div>

    <!-- 日志列表 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">操作日志列表</h3>
        <div class="flex gap-2">
          <button @click="loadLogs" :disabled="loading" 
                  class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-1.5">
            <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            刷新
          </button>
          <button @click="clearLogs" 
                  class="px-3 py-1.5 text-sm bg-[#EF4444] hover:bg-[#DC2626] text-white rounded-lg transition-colors">
            清空日志
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex items-center justify-center py-8">
        <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else-if="logs.length === 0" class="text-center py-12 text-[var(--text-secondary)]">
        <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        <p>暂无操作日志</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">时间</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作类型</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作内容</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">状态</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">耗时</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">IP地址</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id" 
                class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)] cursor-pointer"
                @click="viewLogDetails(log)">
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatDateTime(log.timestamp) }}</td>
              <td class="py-3 px-4">
                <span :class="getActionTypeClass(log.action_type)" class="px-2 py-1 rounded text-xs font-medium">
                  {{ getActionTypeName(log.action_type) }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="font-medium">{{ log.action }}</div>
                <div v-if="log.details?.stock_symbol" class="text-xs text-[var(--text-secondary)]">
                  股票: {{ log.details.stock_symbol }}
                </div>
              </td>
              <td class="py-3 px-4 text-center">
                <span :class="log.success ? 'bg-[#22C55E]/20 text-[#22C55E]' : 'bg-[#EF4444]/20 text-[#EF4444]'" 
                      class="px-2 py-1 rounded text-xs font-medium">
                  {{ log.success ? '成功' : '失败' }}
                </span>
              </td>
              <td class="py-3 px-4 text-right text-sm">{{ log.duration_ms ? log.duration_ms + 'ms' : '-' }}</td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)] font-mono">{{ log.ip_address || '-' }}</td>
              <td class="py-3 px-4 text-center">
                <button @click.stop="viewLogDetails(log)" class="text-[#3B82F6] hover:text-[#2563EB] text-sm">
                  详情
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="logs.length > 0" class="flex items-center justify-between mt-4 pt-4 border-t border-[var(--border-color)]">
        <div class="text-sm text-[var(--text-secondary)]">共 {{ totalLogs }} 条记录</div>
        <div class="flex items-center gap-2">
          <select v-model="pageSize" @change="loadLogs" class="px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
            <option :value="100">100 条/页</option>
            <option :value="200">200 条/页</option>
          </select>
          <button v-for="p in Math.min(5, Math.ceil(totalLogs / pageSize))" :key="p"
                  @click="currentPage = p; loadLogs()"
                  :class="currentPage === p ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)]'"
                  class="w-8 h-8 rounded-lg text-sm transition-colors">
            {{ p }}
          </button>
        </div>
      </div>
    </div>

    <!-- 日志详情弹窗 -->
    <div v-if="detailDialogVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="detailDialogVisible = false">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 w-full max-w-xl mx-4" @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">操作日志详情</h3>
          <button @click="detailDialogVisible = false" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="selectedLog" class="space-y-4">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-[var(--text-secondary)]">操作时间:</span>
              <span class="ml-2">{{ formatDateTime(selectedLog.timestamp) }}</span>
            </div>
            <div>
              <span class="text-[var(--text-secondary)]">操作类型:</span>
              <span :class="getActionTypeClass(selectedLog.action_type)" class="ml-2 px-2 py-0.5 rounded text-xs">
                {{ getActionTypeName(selectedLog.action_type) }}
              </span>
            </div>
            <div>
              <span class="text-[var(--text-secondary)]">操作状态:</span>
              <span :class="selectedLog.success ? 'text-[#22C55E]' : 'text-[#EF4444]'" class="ml-2">
                {{ selectedLog.success ? '成功' : '失败' }}
              </span>
            </div>
            <div>
              <span class="text-[var(--text-secondary)]">耗时:</span>
              <span class="ml-2">{{ selectedLog.duration_ms ? selectedLog.duration_ms + 'ms' : '-' }}</span>
            </div>
            <div>
              <span class="text-[var(--text-secondary)]">IP地址:</span>
              <span class="ml-2 font-mono">{{ selectedLog.ip_address || '-' }}</span>
            </div>
            <div>
              <span class="text-[var(--text-secondary)]">会话ID:</span>
              <span class="ml-2 font-mono text-xs">{{ selectedLog.session_id || '-' }}</span>
            </div>
          </div>
          
          <div>
            <span class="text-[var(--text-secondary)] text-sm">操作内容:</span>
            <p class="mt-1">{{ selectedLog.action }}</p>
          </div>
          
          <div v-if="!selectedLog.success && selectedLog.error_message" class="p-3 bg-[#EF4444]/10 border border-[#EF4444]/20 rounded-lg">
            <div class="text-sm font-medium text-[#EF4444] mb-1">错误信息</div>
            <div class="text-sm">{{ selectedLog.error_message }}</div>
          </div>
          
          <div v-if="selectedLog.details">
            <span class="text-[var(--text-secondary)] text-sm">详细信息:</span>
            <pre class="mt-1 p-3 bg-[var(--bg-tertiary)] rounded-lg text-xs overflow-x-auto">{{ JSON.stringify(selectedLog.details, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'
import {
  OperationLogsApi,
  type OperationLog,
  type OperationLogStats,
  getActionTypeName,
  getActionTypeTagColor,
  formatDateTime
} from '@/api/operationLogs'

// 响应式数据
const loading = ref(false)
const detailDialogVisible = ref(false)
const selectedLog = ref<OperationLog | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const totalLogs = ref(0)

// 图表引用
const actionTypeChart = ref()
const operationTrendChart = ref()

// 筛选表单
const filterForm = reactive({
  startDate: '',
  endDate: '',
  actionType: '',
  success: '',
  keyword: ''
})

// 统计数据
const stats = reactive({
  totalLogs: 0,
  successLogs: 0,
  failedLogs: 0,
  successRate: 0
})

// 日志数据
const logs = ref<OperationLog[]>([])
const statsData = ref<OperationLogStats | null>(null)

// 方法
const getActionTypeClass = (actionType: string): string => {
  const colorMap: Record<string, string> = {
    'stock_analysis': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'config_management': 'bg-[#8B5CF6]/20 text-[#8B5CF6]',
    'cache_operation': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'data_import': 'bg-[#22C55E]/20 text-[#22C55E]',
    'data_export': 'bg-[#22C55E]/20 text-[#22C55E]',
    'system_settings': 'bg-[#EF4444]/20 text-[#EF4444]'
  }
  return colorMap[actionType] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const loadLogs = async () => {
  loading.value = true
  try {
    const queryParams = {
      page: currentPage.value,
      page_size: pageSize.value,
      start_date: filterForm.startDate || undefined,
      end_date: filterForm.endDate || undefined,
      action_type: filterForm.actionType || undefined,
      success: filterForm.success !== '' ? filterForm.success === 'true' : undefined,
      keyword: filterForm.keyword || undefined
    }

    const response = await OperationLogsApi.getOperationLogs(queryParams)
    if (response.success) {
      logs.value = response.data.logs
      totalLogs.value = response.data.total
      await loadStats()
      await nextTick()
      renderCharts()
    }
  } catch (error) {
    console.error('加载操作日志失败:', error)
    ElMessage.error('加载操作日志失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await OperationLogsApi.getOperationLogStats(30)
    if (response.success) {
      statsData.value = response.data
      stats.totalLogs = response.data.total_logs
      stats.successLogs = response.data.success_logs
      stats.failedLogs = response.data.failed_logs
      stats.successRate = response.data.success_rate
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const resetFilter = () => {
  Object.assign(filterForm, { startDate: '', endDate: '', actionType: '', success: '', keyword: '' })
  loadLogs()
}

const exportLogs = async () => {
  try {
    loading.value = true
    const params = { start_date: filterForm.startDate, end_date: filterForm.endDate, action_type: filterForm.actionType }
    const blob = await OperationLogsApi.exportOperationLogsCSV(params)
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `operation_logs_${new Date().toISOString().slice(0, 10)}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('操作日志导出成功')
  } catch (error) {
    console.error('导出操作日志失败:', error)
    ElMessage.error('导出操作日志失败')
  } finally {
    loading.value = false
  }
}

const clearLogs = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有操作日志吗？此操作无法恢复！', '确认清空', { type: 'error' })
    loading.value = true
    const response = await OperationLogsApi.clearOperationLogs()
    if (response.success) {
      ElMessage.success(response.message)
      loadLogs()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空操作日志失败:', error)
      ElMessage.error('清空操作日志失败')
    }
  } finally {
    loading.value = false
  }
}

const viewLogDetails = (log: OperationLog) => {
  selectedLog.value = log
  detailDialogVisible.value = true
}

const renderCharts = () => {
  if (!statsData.value) return

  if (actionTypeChart.value) {
    const chart1 = echarts.init(actionTypeChart.value)
    const pieData = Object.entries(statsData.value.action_type_distribution).map(([type, count]) => ({
      value: count,
      name: getActionTypeName(type)
    }))
    chart1.setOption({
      tooltip: { trigger: 'item' },
      series: [{ type: 'pie', radius: '60%', data: pieData }]
    })
  }

  if (operationTrendChart.value) {
    const chart2 = echarts.init(operationTrendChart.value)
    const hourlyData = statsData.value.hourly_distribution
    chart2.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: hourlyData.map((item: any) => item.hour) },
      yAxis: { type: 'value' },
      series: [{ data: hourlyData.map((item: any) => item.count), type: 'line', smooth: true, areaStyle: {} }]
    })
  }
}

onMounted(() => {
  loadLogs()
})
</script>
