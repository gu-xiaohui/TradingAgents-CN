<template>
  <div class="sync-page" :class="{ 'sync-page-dark': isDarkTheme }">
    <div class="sync-shell">
      <section class="panel sync-summary-panel">
        <div class="summary-header">
          <div class="summary-title-block">
            <div class="sync-hero-kicker">
              <div class="sync-icon-badge">
                <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <div>
              <h3 class="sync-title">数据同步</h3>
              <span>Data Pipeline Console</span>
            </div>
            </div>
          </div>

          <div class="summary-tags">
            <span class="hero-tag">优先源：{{ currentSourceLabel }}</span>
            <span class="hero-tag">已选任务：{{ selectedSyncSummary }}</span>
          </div>
        </div>

        <div class="metrics-strip compact-metrics-strip">
          <div class="metric-pill">
            <span>股票总数</span>
            <strong>{{ formatNumber(stats.totalStocks) }}</strong>
          </div>
          <div class="metric-pill metric-pill-success">
            <span>行情数据</span>
            <strong>{{ formatNumber(stats.quotesCount) }}</strong>
          </div>
          <div class="metric-pill metric-pill-info">
            <span>财务数据</span>
            <strong>{{ formatNumber(stats.financialCount) }}</strong>
          </div>
          <div class="metric-pill metric-pill-accent">
            <span>最新数据日期</span>
            <strong>{{ dayjs(stats.latestDate).format('YYYY-MM-DD') || '-' }}</strong>
          </div>
        </div>
      </section>

      <section class="workspace-section">
        <div class="panel workspace-panel">
          <div class="workspace-head">
            <div>
              <span class="section-kicker">Sync Workbench</span>
              <h2>同步工作台</h2>
            </div>

            <div class="workspace-head-actions">
              <div class="work-status-box">
                <span class="status-label">{{ isSyncing ? syncProgress.message : '待执行' }}</span>
                <span class="hero-status-badge" :class="isSyncing ? 'status-running' : 'status-idle'">
                  {{ isSyncing ? `${syncProgress.percent}%` : 'Ready' }}
                </span>
              </div>

              <div class="workspace-progress-track">
                <div class="hero-progress-fill" :style="progressStyle"></div>
              </div>

              <button
                @click="startSync"
                :disabled="isSyncing || !hasSelectedSync"
                class="btn-primary workspace-run-btn"
              >
                <svg v-if="isSyncing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {{ isSyncing ? '同步中' : '开始同步' }}
              </button>
            </div>
          </div>

          <div class="workspace-grid">
            <div class="workspace-main">
              <div class="control-grid compact-control-grid">
                <div class="control-block source-selector-block">
                  <div class="source-selector-head">
                    <div>
                      <label class="field-label">数据源</label>
                      <p class="source-selector-hint">选择数据源时直接查看可用状态与接入门槛。</p>
                    </div>
                    <span class="hero-tag">当前：{{ currentSourceLabel }}</span>
                  </div>

                  <div class="source-selection-grid">
                    <label
                      v-for="source in sourceOptions"
                      :key="source.value"
                      class="source-select-card"
                      :class="{ active: syncOptions.dataSource === source.value }"
                    >
                      <input
                        v-model="syncOptions.dataSource"
                        type="radio"
                        name="sync-data-source"
                        :value="source.value"
                        class="source-radio"
                      />

                      <div class="source-select-top">
                        <div class="source-chip-top">
                          <div class="status-dot" :class="getStatusClass(source.status)"></div>
                          <strong>{{ source.label }}</strong>
                        </div>
                        <span class="status-pill" :class="getStatusTextClass(source.status)">{{ source.statusText }}</span>
                      </div>

                      <span class="source-select-desc">{{ source.description }}</span>
                    </label>
                  </div>
                </div>

                <div class="control-note-card quick-shortcut-card">
                  <span>快捷操作</span>
                  <div class="quick-shortcut-grid">
                    <el-tooltip
                      v-for="action in quickActionOptions"
                      :key="action.type"
                      :content="action.tooltip"
                      placement="top"
                    >
                      <button
                        type="button"
                        @click="quickSync(action.type)"
                        :disabled="isSyncing"
                        class="source-select-card quick-shortcut-item"
                        :aria-label="action.label"
                      >
                        <div class="quick-shortcut-glow" :class="action.iconClass" aria-hidden="true"></div>

                        <div class="quick-shortcut-content">
                          <div class="quick-action-icon quick-shortcut-icon" :class="action.iconClass">
                            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                              <path stroke-linecap="round" stroke-linejoin="round" :d="action.iconPath" />
                            </svg>
                          </div>

                          <strong class="quick-shortcut-label">{{ action.label }}</strong>
                        </div>
                      </button>
                    </el-tooltip>
                  </div>
                </div>
              </div>

              <div class="section-heading compact-heading">
                <div>
                  <h3>同步范围</h3>
                </div>
              </div>

              <div class="sync-option-grid compact-sync-grid">
                <label class="sync-option-row" :class="{ active: syncOptions.syncStockList }">
                  <input type="checkbox" v-model="syncOptions.syncStockList" class="sync-checkbox" />
                  <div class="sync-option-copy">
                    <strong>股票列表</strong>
                    <span>同步 A 股所有股票基本信息</span>
                  </div>
                </label>

                <label class="sync-option-row" :class="{ active: syncOptions.syncRealtime }">
                  <input type="checkbox" v-model="syncOptions.syncRealtime" class="sync-checkbox" />
                  <div class="sync-option-copy">
                    <strong>实时行情</strong>
                    <span>同步当日所有股票行情数据</span>
                  </div>
                </label>

                <label class="sync-option-row" :class="{ active: syncOptions.syncHistorical }">
                  <input type="checkbox" v-model="syncOptions.syncHistorical" class="sync-checkbox" />
                  <div class="sync-option-copy">
                    <strong>历史数据</strong>
                    <span>同步股票历史 K 线数据</span>
                  </div>
                </label>

                <label class="sync-option-row" :class="{ active: syncOptions.syncFinancial }">
                  <input type="checkbox" v-model="syncOptions.syncFinancial" class="sync-checkbox" />
                  <div class="sync-option-copy">
                    <strong>财务数据</strong>
                    <span>同步股票财务报表数据</span>
                  </div>
                </label>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="history-grid">
        <div class="panel">
          <div class="section-heading">
            <div>
              <span class="section-kicker">Execution Log</span>
              <h2>同步历史</h2>
              <p>查看最近执行记录，判断是否需要重跑或切换数据源。</p>
            </div>
            <button @click="clearHistory" class="ghost-action">清空历史</button>
          </div>

          <div v-if="syncHistory.length === 0" class="empty-state">
            <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>暂无同步记录</p>
          </div>

          <div v-else class="history-list">
            <div
              v-for="(record, index) in syncHistory"
              :key="index"
              class="history-row"
            >
              <div class="history-row-main">
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

                <div class="history-copy">
                  <strong>{{ record.type }}</strong>
                  <span>{{ record.message }}</span>
                </div>
              </div>

              <div class="history-meta">
                <strong>{{ record.count }} 条</strong>
                <span>{{ record.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { dayjs, ElMessage } from 'element-plus'
import { useThemeStore } from '../../stores/theme'
import {
  getSyncStatus,
  getDataSourcesStatus,
  runStockBasicsSync,
  getSyncHistory as fetchSyncHistory
} from '@/api/sync'

const themeStore = useThemeStore()
const isDarkTheme = computed(() => themeStore.getActualTheme() === 'dark')

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

const currentSourceLabel = computed(() => {
  const sourceMap: Record<string, string> = {
    akshare: 'AKShare',
    baostock: 'BaoStock',
    tushare: 'Tushare'
  }

  return sourceMap[syncOptions.value.dataSource] || syncOptions.value.dataSource
})

const sourceOptions = computed(() => {
  const descriptions: Record<string, string> = {
    akshare: '免费接入，适合日常同步与快速验证。',
    baostock: '免费数据源，适合基础行情与批量任务。',
    tushare: '专业数据覆盖更广，使用前需配置 Token。'
  }

  return dataSources.value.map((source) => {
    const value = String(source.name || '').toLowerCase()
    return {
      ...source,
      value,
      label: formatSourceName(source.name),
      description: descriptions[value] || '可用于当前同步任务。'
    }
  })
})

const quickActionOptions = [
  {
    type: 'realtime',
    label: '行情',
    tooltip: '快速同步行情：仅同步当日实时数据',
    iconClass: 'quick-action-green',
    iconPath: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'
  },
  {
    type: 'stocks',
    label: '股票列表',
    tooltip: '同步股票列表：更新基础信息',
    iconClass: 'quick-action-blue',
    iconPath: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10'
  },
  {
    type: 'full',
    label: '全量',
    tooltip: '全量同步：股票、行情、历史、财务全部执行',
    iconClass: 'quick-action-violet',
    iconPath: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'
  }
]

const selectedSyncSummary = computed(() => {
  const selections = []
  if (syncOptions.value.syncStockList) selections.push('股票列表')
  if (syncOptions.value.syncRealtime) selections.push('实时行情')
  if (syncOptions.value.syncHistorical) selections.push('历史数据')
  if (syncOptions.value.syncFinancial) selections.push('财务数据')
  return selections.length ? selections.join(' / ') : '未选择'
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

const formatSourceName = (name: string) => {
  const normalized = String(name || '').toLowerCase()
  if (normalized === 'akshare') return 'AKShare'
  if (normalized === 'baostock') return 'BaoStock'
  if (normalized === 'tushare') return 'Tushare'
  return name
}

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

</script>

<style scoped>
.sync-page {
  --sync-surface: rgba(255, 255, 255, 0.9);
  --sync-surface-strong: rgba(255, 255, 255, 0.97);
  --sync-surface-soft: rgba(241, 245, 249, 0.92);
  --sync-surface-hover: rgba(255, 255, 255, 1);
  --sync-border: rgba(148, 163, 184, 0.24);
  --sync-border-strong: rgba(148, 163, 184, 0.34);
  --sync-shadow: 0 18px 42px rgba(15, 23, 42, 0.08), 0 8px 18px rgba(15, 23, 42, 0.05);
  --sync-shadow-soft: 0 10px 24px rgba(15, 23, 42, 0.05);
  --sync-inner-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.9);
  --sync-tag-bg: rgba(255, 255, 255, 0.86);
  --sync-track-bg: rgba(148, 163, 184, 0.2);
  --sync-status-running-bg: rgba(59, 130, 246, 0.14);
  --sync-status-running-fg: #2563eb;
  --sync-status-idle-bg: rgba(16, 185, 129, 0.14);
  --sync-status-idle-fg: #059669;
  --sync-note-accent: #3b82f6;
  --sync-option-active-bg: rgba(37, 99, 235, 0.12);
  --sync-option-active-shadow: 0 14px 30px rgba(37, 99, 235, 0.12);
  --sync-input-focus-bg: #ffffff;
  --sync-input-focus-ring: 0 0 0 4px rgba(59, 130, 246, 0.12);
  --sync-quick-green-bg: rgba(16, 185, 129, 0.16);
  --sync-quick-green-fg: #059669;
  --sync-quick-blue-bg: rgba(37, 99, 235, 0.14);
  --sync-quick-blue-fg: #2563eb;
  --sync-quick-violet-bg: rgba(139, 92, 246, 0.14);
  --sync-quick-violet-fg: #7c3aed;
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(59, 130, 246, 0.12), transparent 24%),
    radial-gradient(circle at right top, rgba(16, 185, 129, 0.1), transparent 22%),
    var(--bg-primary);
  color: var(--text-primary);
}

.sync-page.sync-page-dark {
  --sync-surface: rgba(255, 255, 255, 0.04);
  --sync-surface-strong: rgba(255, 255, 255, 0.08);
  --sync-surface-soft: rgba(255, 255, 255, 0.035);
  --sync-surface-hover: rgba(255, 255, 255, 0.07);
  --sync-border: rgba(255, 255, 255, 0.08);
  --sync-border-strong: rgba(59, 130, 246, 0.42);
  --sync-shadow: 0 20px 60px rgba(15, 23, 42, 0.12);
  --sync-shadow-soft: 0 12px 32px rgba(15, 23, 42, 0.1);
  --sync-inner-highlight: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  --sync-tag-bg: rgba(255, 255, 255, 0.05);
  --sync-track-bg: rgba(255, 255, 255, 0.08);
  --sync-status-running-bg: rgba(59, 130, 246, 0.18);
  --sync-status-running-fg: #93c5fd;
  --sync-status-idle-bg: rgba(16, 185, 129, 0.16);
  --sync-status-idle-fg: #6ee7b7;
  --sync-note-accent: #93c5fd;
  --sync-option-active-bg: rgba(37, 99, 235, 0.1);
  --sync-option-active-shadow: none;
  --sync-input-focus-bg: rgba(255, 255, 255, 0.1);
  --sync-input-focus-ring: 0 0 0 4px rgba(59, 130, 246, 0.16);
  --sync-quick-green-bg: rgba(16, 185, 129, 0.18);
  --sync-quick-green-fg: #6ee7b7;
  --sync-quick-blue-bg: rgba(37, 99, 235, 0.18);
  --sync-quick-blue-fg: #93c5fd;
  --sync-quick-violet-bg: rgba(139, 92, 246, 0.18);
  --sync-quick-violet-fg: #c4b5fd;
}

.sync-shell {
  max-width: 1380px;
  margin: 0 auto;
  padding: 24px 20px 40px;
}

.card,
.panel,
.hero-card {
  background: linear-gradient(180deg, var(--sync-surface-strong) 0%, var(--sync-surface) 100%);
  border: 1px solid var(--sync-border);
  border-radius: 24px;
  backdrop-filter: blur(16px);
  box-shadow: var(--sync-shadow), var(--sync-inner-highlight);
}

.card,
.panel {
  padding: 22px;
}

.sync-summary-panel {
  padding: 14px 16px;
}

.summary-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.summary-title-block {
  min-width: 0;
}

.summary-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
}

.sync-hero-kicker {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.sync-icon-badge {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2563eb 0%, #14b8a6 100%);
}

.sync-title {
  font-size: clamp(1.7rem, 4vw, 2.4rem);
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.sync-subtitle {
  margin-top: 6px;
  max-width: 40rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.hero-tag,
.ghost-action,
.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  border: 1px solid var(--sync-border);
  background: var(--sync-tag-bg);
  padding: 6px 10px;
  font-size: 0.76rem;
}

.hero-status-top h2,
.section-heading h2,
.compact-heading h3 {
  font-size: 0.98rem;
  font-weight: 600;
}

.hero-status-message,
.section-heading p,
.compact-heading p,
.control-note-card p,
.sync-option-copy span,
.quick-action-copy span,
.source-row span,
.history-copy span,
.history-meta span,
.empty-state {
  color: var(--text-secondary);
  line-height: 1.6;
}

.hero-status-badge {
  min-width: 62px;
  padding: 5px 9px;
  border-radius: 9999px;
  text-align: center;
  font-size: 0.74rem;
  font-weight: 600;
}

.status-running {
  background: var(--sync-status-running-bg);
  color: var(--sync-status-running-fg);
}

.status-idle {
  background: var(--sync-status-idle-bg);
  color: var(--sync-status-idle-fg);
}

.hero-progress-track {
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: var(--sync-track-bg);
  overflow: hidden;
}

.hero-progress-fill,
.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #2563eb, #14b8a6);
  transition: width 0.3s ease;
}

.metrics-strip {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
  margin-top: 10px;
}

.metric-pill {
  border-radius: 14px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface-soft);
  padding: 10px 12px;
  box-shadow: var(--sync-shadow-soft);
}

.metric-pill span,
.section-kicker,
.field-label {
  display: block;
  color: var(--text-secondary);
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.metric-pill strong {
  display: block;
  margin-top: 4px;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.metric-pill-success strong { color: #6ee7b7; }
.metric-pill-info strong { color: #93c5fd; }
.metric-pill-accent strong { color: #c4b5fd; }

.workspace-section {
  margin-top: 10px;
}
.history-grid {
  margin-top: 10px;
}

.workspace-panel {
  padding: 20px;
}

.workspace-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 16px;
  align-items: start;
  margin-bottom: 18px;
}

.workspace-head-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.work-status-box {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border-radius: 9999px;
  border: 1px solid var(--sync-border);
  background: var(--sync-tag-bg);
  padding: 6px 10px;
}

.status-label {
  color: var(--text-secondary);
  font-size: 0.82rem;
}

.workspace-progress-track {
  width: 132px;
  height: 6px;
  border-radius: 9999px;
  background: var(--sync-track-bg);
  overflow: hidden;
}

.workspace-run-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 14px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 18px;
  align-items: start;
}

.workspace-main {
  min-width: 0;
}

.workspace-mini-section {
  border-radius: 20px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface-soft);
  padding: 14px;
}

.mini-section-header {
  margin-bottom: 12px;
}

.mini-section-header h3 {
  margin-top: 6px;
  font-size: 1rem;
  font-weight: 600;
}

.compact-mini-header {
  margin-bottom: 10px;
}

.compact-mini-header h4 {
  margin-top: 4px;
  font-size: 0.92rem;
  font-weight: 600;
}

.section-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.compact-heading {
  margin-bottom: 14px;
}

.control-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 0.8fr);
  gap: 14px;
}

.compact-control-grid {
  margin-bottom: 18px;
}

.control-block,
.control-note-card {
  border-radius: 20px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface-soft);
  padding: 16px;
  box-shadow: var(--sync-shadow-soft);
}

.control-note-card span {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--sync-note-accent);
}

.control-note-card p {
  margin-top: 10px;
}

.source-selector-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.source-selector-hint,
.source-select-desc {
  color: var(--text-secondary);
  line-height: 1.6;
}

.source-selector-hint {
  margin-top: 8px;
  font-size: 0.9rem;
}

.source-selection-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.source-select-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;
  border-radius: 18px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface);
  padding: 14px;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
  box-shadow: var(--sync-shadow-soft);
}

.source-select-card:hover {
  transform: translateY(-1px);
  background: var(--sync-surface-hover);
}

.source-select-card.active {
  border-color: var(--sync-border-strong);
  background: var(--sync-option-active-bg);
  box-shadow: var(--sync-option-active-shadow);
}

.source-select-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.source-radio {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.quick-shortcut-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.quick-shortcut-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.quick-shortcut-item {
  position: relative;
  overflow: hidden;
  display: block;
  width: 100%;
  text-align: left;
  border: 1px solid var(--sync-border);
  min-height: 126px;
  padding: 18px;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--sync-surface-strong) 88%, white 12%) 0%, var(--sync-surface) 100%);
}

.quick-shortcut-item:hover:not(:disabled) {
  border-color: var(--sync-border-strong);
  box-shadow: var(--sync-shadow-soft);
}

.quick-shortcut-glow {
  position: absolute;
  top: -12px;
  right: -8px;
  width: 120px;
  height: 120px;
  border-radius: 9999px;
  opacity: 0.16;
  filter: blur(10px);
  pointer-events: none;
}

.quick-shortcut-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  min-height: 90px;
}

.quick-shortcut-icon {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28);
}

.quick-shortcut-label {
  font-size: 1.12rem;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  word-break: keep-all;
  overflow-wrap: break-word;
}

.quick-shortcut-item:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sync-option-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.compact-sync-grid {
  gap: 12px;
}

.sync-option-card,
.sync-option-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface-soft);
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
  box-shadow: var(--sync-shadow-soft);
}

.sync-option-card:hover,
.sync-option-row:hover,
.quick-action-card:hover,
.ghost-action:hover {
  transform: translateY(-1px);
  background: var(--sync-surface-hover);
}

.sync-option-card.active,
.sync-option-row.active {
  border-color: var(--sync-border-strong);
  background: var(--sync-option-active-bg);
  box-shadow: var(--sync-option-active-shadow);
}

.sync-checkbox {
  margin-top: 2px;
  width: 18px;
  height: 18px;
  accent-color: #2563eb;
}

.sync-option-copy strong,
.quick-action-copy strong,
.source-row strong,
.history-copy strong,
.history-meta strong {
  display: block;
  font-weight: 600;
}

.sync-option-copy span,
.quick-action-copy span,
.history-copy span,
.history-meta span {
  display: block;
  margin-top: 6px;
  font-size: 0.9rem;
}

.input {
  width: 100%;
  padding: 12px 16px;
  background: var(--sync-surface-strong);
  border: 1px solid var(--sync-border);
  border-radius: 12px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.2s;
  box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04);
}

.input:focus {
  outline: none;
  border-color: #3B82F6;
  background: var(--sync-input-focus-bg);
  box-shadow: var(--sync-input-focus-ring);
}

.btn-primary {
  padding: 12px 24px;
  background: linear-gradient(135deg, #2563eb 0%, #14b8a6 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.source-list,
.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.source-chip-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

.source-row,
.quick-action-card,
.history-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  border-radius: 20px;
  border: 1px solid var(--sync-border);
  background: var(--sync-surface);
  padding: 14px 16px;
  box-shadow: var(--sync-shadow-soft);
}

.source-row-main,
.history-row-main {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.source-row span {
  display: block;
  margin-top: 4px;
  font-size: 0.84rem;
}

.status-pill {
  font-size: 0.78rem;
}

.record-icon {
  width: 40px;
  height: 40px;
  flex: 0 0 auto;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quick-action-card {
  width: 100%;
  text-align: left;
}

.compact-quick-card {
  padding: 12px 14px;
  border-radius: 16px;
}

.toolbar-quick-card {
  padding: 10px 12px;
}

.quick-action-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
}

.quick-action-green {
  background: var(--sync-quick-green-bg);
  color: var(--sync-quick-green-fg);
}

.quick-action-blue {
  background: var(--sync-quick-blue-bg);
  color: var(--sync-quick-blue-fg);
}

.quick-action-violet {
  background: var(--sync-quick-violet-bg);
  color: var(--sync-quick-violet-fg);
}

.history-meta {
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 48px 0;
}

.hero-orb {
  position: absolute;
  border-radius: 9999px;
  filter: blur(80px);
}

.hero-orb-left {
  top: -32px;
  left: -20px;
  width: 220px;
  height: 220px;
  background: rgba(37, 99, 235, 0.18);
}

.hero-orb-right {
  right: -24px;
  top: 20px;
  width: 260px;
  height: 260px;
  background: rgba(16, 185, 129, 0.14);
}

@media (max-width: 1279px) {
  .summary-header,
  .workspace-head,
  .workspace-grid,
  .control-grid {
    grid-template-columns: 1fr;
  }

  .workspace-head-actions,
  .summary-tags {
    justify-content: flex-start;
  }

  .metrics-strip,
  .sync-option-grid,
  .source-selection-grid,
  .quick-shortcut-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .sync-shell {
    padding: 16px 14px 32px;
  }

  .hero-card,
  .panel,
  .card {
    padding: 14px;
    border-radius: 20px;
  }

  .metrics-strip,
  .sync-option-grid,
  .source-selection-grid,
  .quick-shortcut-grid {
    grid-template-columns: 1fr;
  }

  .source-selector-head,
  .quick-shortcut-grid {
    flex-wrap: wrap;
  }

  .workspace-head-actions,
  .work-status-box {
    width: 100%;
  }

  .workspace-progress-track,
  .workspace-run-btn {
    width: 100%;
  }

  .quick-action-card,
  .history-row,
  .section-heading {
    flex-direction: column;
    align-items: flex-start;
  }

  .history-meta {
    text-align: left;
  }
}
</style>
