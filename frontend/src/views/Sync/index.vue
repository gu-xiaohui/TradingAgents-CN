<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#3B82F6] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </div>
        数据同步
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">同步股票基础信息、实时行情和财务数据</p>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：同步控制面板 -->
      <div class="col-span-4">
        <div class="card">
          <h2 class="text-lg font-semibold mb-6 flex items-center gap-2">
            <svg class="w-5 h-5 text-[var(--text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            同步选项
          </h2>

          <!-- 数据源选择 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-2">数据源</label>
            <select v-model="syncOptions.dataSource" class="input">
              <option value="akshare">AKShare (免费)</option>
              <option value="baostock">BaoStock (免费)</option>
              <option value="tushare">Tushare (需Token)</option>
            </select>
          </div>

          <!-- 同步类型 -->
          <div class="mb-6">
            <label class="block text-sm text-[var(--text-secondary)] mb-3">同步类型</label>
            <div class="space-y-3">
              <label class="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors">
                <input type="checkbox" v-model="syncOptions.syncStockList" class="w-5 h-5 accent-blue-500" />
                <div>
                  <div class="font-medium">股票列表</div>
                  <div class="text-xs text-[var(--text-muted)]">同步 A 股所有股票基本信息</div>
                </div>
              </label>
              
              <label class="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors">
                <input type="checkbox" v-model="syncOptions.syncRealtime" class="w-5 h-5 accent-blue-500" />
                <div>
                  <div class="font-medium">实时行情</div>
                  <div class="text-xs text-[var(--text-muted)]">同步当日所有股票行情数据</div>
                </div>
              </label>

              <label class="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors">
                <input type="checkbox" v-model="syncOptions.syncHistorical" class="w-5 h-5 accent-blue-500" />
                <div>
                  <div class="font-medium">历史数据</div>
                  <div class="text-xs text-[var(--text-muted)]">同步股票历史 K 线数据</div>
                </div>
              </label>

              <label class="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors">
                <input type="checkbox" v-model="syncOptions.syncFinancial" class="w-5 h-5 accent-blue-500" />
                <div>
                  <div class="font-medium">财务数据</div>
                  <div class="text-xs text-[var(--text-muted)]">同步股票财务报表数据</div>
                </div>
              </label>
            </div>
          </div>

          <!-- 同步按钮 -->
          <button 
            @click="startSync" 
            :disabled="isSyncing || !hasSelectedSync"
            class="btn-primary w-full flex items-center justify-center gap-2"
          >
            <svg v-if="isSyncing" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ isSyncing ? '同步中...' : '开始同步' }}
          </button>

          <!-- 进度条 -->
          <div v-if="isSyncing" class="mt-4">
            <div class="flex justify-between text-sm mb-2">
              <span class="text-[var(--text-secondary)]">{{ syncProgress.message }}</span>
              <span class="text-[var(--text-primary)]">{{ syncProgress.percent }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-2">
              <div 
                class="progress-fill h-2 rounded-full transition-all duration-300"
                :style="progressStyle"
              ></div>
            </div>
          </div>
        </div>

        <!-- 数据源状态 -->
        <div class="card mt-6">
          <h2 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-[var(--text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            数据源状态
          </h2>
          <div class="space-y-3">
            <div v-for="source in dataSources" :key="source.name" class="flex items-center justify-between p-3 rounded-lg bg-white/5">
              <div class="flex items-center gap-3">
                <div class="status-dot" :class="getStatusClass(source.status)"></div>
                <span>{{ source.name }}</span>
              </div>
              <span class="status-text" :class="getStatusTextClass(source.status)">
                {{ source.statusText }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：同步历史和统计 -->
      <div class="col-span-8">
        <!-- 数据统计 -->
        <div class="grid grid-cols-4 gap-4 mb-6">
          <div class="card text-center">
            <div class="text-3xl font-bold text-[var(--text-primary)]">{{ formatNumber(stats.totalStocks) }}</div>
            <div class="text-sm text-[var(--text-secondary)] mt-1">股票总数</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-green-400">{{ formatNumber(stats.quotesCount) }}</div>
            <div class="text-sm text-[var(--text-secondary)] mt-1">行情数据</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-blue-400">{{ formatNumber(stats.financialCount) }}</div>
            <div class="text-sm text-[var(--text-secondary)] mt-1">财务数据</div>
          </div>
          <div class="card text-center">
            <div class="text-3xl font-bold text-purple-400">{{ stats.latestDate || '-' }}</div>
            <div class="text-sm text-[var(--text-secondary)] mt-1">最新数据日期</div>
          </div>
        </div>

        <!-- 同步历史 -->
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold flex items-center gap-2">
              <svg class="w-5 h-5 text-[var(--text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              同步历史
            </h2>
            <button @click="clearHistory" class="text-sm text-[var(--text-secondary)] hover:text-red-400 transition-colors">
              清空历史
            </button>
          </div>

          <div v-if="syncHistory.length === 0" class="text-center py-12 text-[var(--text-muted)]">
            <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>暂无同步记录</p>
          </div>

          <div v-else class="space-y-3">
            <div 
              v-for="(record, index) in syncHistory" 
              :key="index"
              class="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            >
              <div class="flex items-center gap-4">
                <div class="record-icon" :class="getRecordIconClass(record.status)">
                  <svg v-if="record.status === 'success'" class="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else-if="record.status === 'failed'" class="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <svg v-else class="w-5 h-5 text-yellow-400 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                </div>
                <div>
                  <div class="font-medium">{{ record.type }}</div>
                  <div class="text-sm text-[var(--text-muted)]">{{ record.message }}</div>
                </div>
              </div>
              <div class="text-right">
                <div class="text-sm text-[var(--text-primary)]">{{ record.count }} 条</div>
                <div class="text-xs text-[var(--text-muted)]">{{ record.time }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速同步按钮 -->
        <div class="grid grid-cols-3 gap-4 mt-6">
          <button 
            @click="quickSync('realtime')" 
            :disabled="isSyncing"
            class="card hover:bg-white/10 transition-colors text-center py-6"
          >
            <svg class="w-8 h-8 mx-auto mb-2 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <div class="font-medium">快速同步行情</div>
            <div class="text-xs text-[var(--text-muted)] mt-1">仅同步当日实时数据</div>
          </button>

          <button 
            @click="quickSync('stocks')" 
            :disabled="isSyncing"
            class="card hover:bg-white/10 transition-colors text-center py-6"
          >
            <svg class="w-8 h-8 mx-auto mb-2 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <div class="font-medium">同步股票列表</div>
            <div class="text-xs text-[var(--text-muted)] mt-1">更新所有股票基本信息</div>
          </button>

          <button 
            @click="quickSync('full')" 
            :disabled="isSyncing"
            class="card hover:bg-white/10 transition-colors text-center py-6"
          >
            <svg class="w-8 h-8 mx-auto mb-2 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <div class="font-medium">全量同步</div>
            <div class="text-xs text-[var(--text-muted)] mt-1">同步所有数据（耗时较长）</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getSyncStatus,
  getDataSourcesStatus,
  runStockBasicsSync,
  getSyncHistory as fetchSyncHistory
} from '@/api/sync'

// 同步选项
const syncOptions = ref({
  dataSource: 'akshare',
  syncStockList: false,
  syncRealtime: true,
  syncHistorical: false,
  syncFinancial: false
})

// 是否有选中的同步项
const hasSelectedSync = computed(() => {
  return syncOptions.value.syncStockList || 
         syncOptions.value.syncRealtime || 
         syncOptions.value.syncHistorical || 
         syncOptions.value.syncFinancial
})

// 同步状态
const isSyncing = ref(false)
const syncProgress = ref({
  percent: 0,
  message: '准备同步...'
})

// 进度条样式
const progressStyle = computed(() => {
  return `width: ${syncProgress.value.percent}%`
})

// 数据统计
const stats = ref({
  totalStocks: 0,
  quotesCount: 0,
  financialCount: 0,
  latestDate: '-'
})

// 数据源状态
const dataSources = ref([
  { name: 'AKShare', status: 'warning', statusText: '检查中...' },
  { name: 'BaoStock', status: 'warning', statusText: '检查中...' },
  { name: 'Tushare', status: 'warning', statusText: '检查中...' }
])

// 从后端加载数据源状态
const loadDataSourcesStatus = async () => {
  try {
    const res = await getDataSourcesStatus()
    if (res.success && Array.isArray(res.data)) {
      dataSources.value = res.data.map((ds: any) => ({
        name: ds.name || ds.source || '',
        status: ds.available ? 'healthy' : 'error',
        statusText: ds.available ? '正常' : '不可用'
      }))
    }
  } catch {
    // 回退：通过配置接口检查
    await checkDataSourcesFallback()
  }
}

// 回退方案：检查数据源配置
const checkDataSourcesFallback = async () => {
  try {
    const response = await fetch('/api/config/datasource', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('auth-token')}` }
    })
    if (response.ok) {
      const configs = await response.json()
      const tushareConfig = configs.find((c: any) => 
        c.type === 'tushare' || 
        c.name?.toLowerCase() === 'tushare'
      )
      
      // AKShare and BaoStock are always available (free, no token)
      const akSource = dataSources.value.find(s => s.name === 'AKShare')
      if (akSource) { akSource.status = 'healthy'; akSource.statusText = '正常' }
      const bsSource = dataSources.value.find(s => s.name === 'BaoStock')
      if (bsSource) { bsSource.status = 'healthy'; bsSource.statusText = '正常' }
      
      const tushareSource = dataSources.value.find(s => s.name === 'Tushare')
      if (tushareSource) {
        if (tushareConfig && tushareConfig.api_key) {
          tushareSource.status = 'healthy'
          tushareSource.statusText = '已配置'
        } else {
          tushareSource.status = 'warning'
          tushareSource.statusText = '未配置Token'
        }
      }
    }
  } catch {
    const tushareSource = dataSources.value.find(s => s.name === 'Tushare')
    if (tushareSource) {
      tushareSource.status = 'warning'
      tushareSource.statusText = '未配置Token'
    }
  }
}

// 从后端加载同步状态和统计数据
const loadSyncStatus = async () => {
  try {
    const res = await getSyncStatus()
    if (res.success && res.data) {
      const data = res.data
      stats.value = {
        totalStocks: data.total || stats.value.totalStocks,
        quotesCount: data.inserted || data.updated || stats.value.quotesCount,
        financialCount: stats.value.financialCount,
        latestDate: data.last_trade_date || data.finished_at?.substring(0, 10) || stats.value.latestDate
      }
    }
  } catch {
    // 保持默认状态
  }
}

// 页面加载时检查数据源状态
onMounted(async () => {
  await Promise.all([
    loadDataSourcesStatus(),
    loadSyncStatus(),
    loadSyncHistory()
  ])
})

// 同步历史
const syncHistory = ref<Array<{
  type: string
  message: string
  count: number
  status: string
  time: string
}>>([])

// 加载同步历史
const loadSyncHistory = async () => {
  try {
    const res = await fetchSyncHistory({ page: 1, page_size: 10 })
    if (res.success && res.data?.records) {
      syncHistory.value = res.data.records.map((r: any) => ({
        type: r.job || '数据同步',
        message: r.message || (r.status === 'success' ? '同步完成' : r.status),
        count: r.total || r.inserted || 0,
        status: r.status === 'success' || r.status === 'success_with_errors' ? 'success' : r.status === 'failed' ? 'failed' : 'pending',
        time: r.finished_at ? new Date(r.finished_at).toLocaleString('zh-CN') : r.started_at ? new Date(r.started_at).toLocaleString('zh-CN') : '-'
      }))
    }
  } catch {
    // 保持空列表
  }
}
// 辅助函数
const formatNumber = (num: number) => num.toLocaleString()

const getStatusClass = (status: string) => {
  if (status === 'healthy') return 'bg-green-500'
  if (status === 'error') return 'bg-red-500'
  return 'bg-yellow-500'
}

const getStatusTextClass = (status: string) => {
  if (status === 'healthy') return 'text-green-400'
  if (status === 'error') return 'text-red-400'
  return 'text-yellow-400'
}

const getRecordIconClass = (status: string) => {
  if (status === 'success') return 'bg-green-500/20'
  if (status === 'failed') return 'bg-red-500/20'
  return 'bg-yellow-500/20'
}

// 开始同步
const startSync = async () => {
  if (!hasSelectedSync.value) {
    ElMessage.warning('请至少选择一项同步内容')
    return
  }

  isSyncing.value = true
  syncProgress.value = { percent: 0, message: '正在初始化...' }

  try {
    // 调用后端同步API
    syncProgress.value = { percent: 10, message: '正在连接数据源...' }

    const preferredSource = syncOptions.value.dataSource || 'akshare'
    const res = await runStockBasicsSync({
      force: false,
      preferred_sources: preferredSource
    })

    if (res.success && res.data) {
      const result = res.data
      syncProgress.value = { percent: 100, message: '同步完成！' }

      // 更新统计数据
      if (result.total) {
        stats.value.totalStocks = result.total
      }
      if (result.last_trade_date) {
        stats.value.latestDate = result.last_trade_date
      }

      // 添加同步历史
      syncHistory.value.unshift({
        type: '股票基础信息',
        message: result.message || '同步完成',
        count: result.total || result.inserted || 0,
        status: result.status === 'success' || result.status === 'success_with_errors' ? 'success' : 'failed',
        time: new Date().toLocaleString('zh-CN')
      })

      ElMessage.success(result.message || '数据同步完成')
    } else {
      syncProgress.value = { percent: 0, message: '同步失败' }
      ElMessage.error(res.message || '数据同步失败')
    }
  } catch (error) {
    const err = error as Error
    syncProgress.value.message = `同步失败: ${err.message}`
    ElMessage.error('数据同步失败，请检查后端服务')
  } finally {
    setTimeout(() => {
      isSyncing.value = false
    }, 1000)
  }
}

// 快速同步
const quickSync = async (type: string) => {
  if (type === 'realtime') {
    syncOptions.value.syncRealtime = true
    syncOptions.value.syncStockList = false
    syncOptions.value.syncHistorical = false
    syncOptions.value.syncFinancial = false
  } else if (type === 'stocks') {
    syncOptions.value.syncStockList = true
    syncOptions.value.syncRealtime = false
    syncOptions.value.syncHistorical = false
    syncOptions.value.syncFinancial = false
  } else if (type === 'full') {
    syncOptions.value.syncStockList = true
    syncOptions.value.syncRealtime = true
    syncOptions.value.syncHistorical = true
    syncOptions.value.syncFinancial = true
  }
  
  await startSync()
}

// 清空历史
const clearHistory = () => {
  syncHistory.value = []
  ElMessage.success('历史记录已清空')
}

// 加载统计数据
const loadStats = async () => {
  // TODO: 从后端 API 获取实际统计数据
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
}

.input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s;
}

.input:focus {
  outline: none;
  border-color: #3B82F6;
  background: rgba(255, 255, 255, 0.1);
}

.btn-primary {
  padding: 12px 24px;
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.progress-fill {
  background: linear-gradient(90deg, #3B82F6, #8B5CF6);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-text {
  font-size: 14px;
}

.record-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
