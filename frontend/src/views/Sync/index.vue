<template>
  <div class="sync-page">
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
              <span>Data Pipeline Console</span>
            </div>
            <div>
              <h1 class="sync-title">数据同步</h1>
              <p class="sync-subtitle">压缩成一个短工作面板，适合快速完成一轮同步。</p>
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
            <strong>{{ stats.latestDate || '-' }}</strong>
          </div>
        </div>
      </section>

      <section class="workspace-section">
        <div class="panel workspace-panel">
          <div class="workspace-head">
            <div>
              <span class="section-kicker">Sync Workbench</span>
              <h2>同步工作台</h2>
              <p>状态、动作和任务范围都在这里完成，不再拆成多块区域。</p>
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
                <div class="control-block">
                  <label class="field-label">数据源</label>
                  <select v-model="syncOptions.dataSource" class="input sync-select">
                    <option value="akshare">AKShare (免费)</option>
                    <option value="baostock">BaoStock (免费)</option>
                    <option value="tushare">Tushare (需Token)</option>
                  </select>
                </div>

                <div class="control-note-card">
                  <span>当前策略</span>
                  <p>优先使用 {{ currentSourceLabel }} 执行同步。若数据源能力不足，优先拆分“股票列表”和“实时行情”。</p>
                </div>
              </div>

              <div class="section-heading compact-heading">
                <div>
                  <h3>同步范围</h3>
                  <p>压成更扁的切换行，减少面板高度。</p>
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

            <div class="workspace-side">
              <div class="workspace-tools-panel">
                <div class="tools-toolbar-head compact-tools-head">
                  <div>
                    <span class="section-kicker">Tools Rail</span>
                    <h3>数据源与快捷同步</h3>
                  </div>
                </div>

                <div class="tools-toolbar-inline">
                  <div class="inline-status-group">
                    <span class="inline-group-label">数据源</span>
                    <div class="source-chip-grid compact-source-grid toolbar-source-grid">
                      <div v-for="source in dataSources" :key="source.name" class="source-chip-card compact-source-card toolbar-source-card">
                        <div class="source-chip-top">
                          <div class="status-dot" :class="getStatusClass(source.status)"></div>
                          <strong>{{ formatSourceName(source.name) }}</strong>
                        </div>
                        <span class="status-pill" :class="getStatusTextClass(source.status)">{{ source.statusText }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="inline-action-group">
                    <span class="inline-group-label">快捷动作</span>
                    <div class="quick-action-stack compact-quick-stack toolbar-quick-stack">
                      <button
                        @click="quickSync('realtime')"
                        :disabled="isSyncing"
                        class="quick-action-card compact-quick-card toolbar-quick-card"
                      >
                        <div class="quick-action-icon quick-action-green">
                          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                          </svg>
                        </div>
                        <div class="quick-action-copy">
                          <strong>快速同步行情</strong>
                          <span>仅同步当日实时数据</span>
                        </div>
                      </button>

                      <button
                        @click="quickSync('stocks')"
                        :disabled="isSyncing"
                        class="quick-action-card compact-quick-card toolbar-quick-card"
                      >
                        <div class="quick-action-icon quick-action-blue">
                          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                          </svg>
                        </div>
                        <div class="quick-action-copy">
                          <strong>同步股票列表</strong>
                          <span>更新股票基础信息</span>
                        </div>
                      </button>

                      <button
                        @click="quickSync('full')"
                        :disabled="isSyncing"
                        class="quick-action-card compact-quick-card toolbar-quick-card"
                      >
                        <div class="quick-action-icon quick-action-violet">
                          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                        </div>
                        <div class="quick-action-copy">
                          <strong>全量同步</strong>
                          <span>同步所有数据</span>
                        </div>
                      </button>
                    </div>
                  </div>
                </div>
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

const currentSourceLabel = computed(() => {
  const sourceMap: Record<string, string> = {
    akshare: 'AKShare',
    baostock: 'BaoStock',
    tushare: 'Tushare'
  }

  return sourceMap[syncOptions.value.dataSource] || syncOptions.value.dataSource
})

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
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(59, 130, 246, 0.12), transparent 24%),
    radial-gradient(circle at right top, rgba(16, 185, 129, 0.1), transparent 22%),
    var(--bg-primary);
  color: var(--text-primary);
}

.sync-shell {
  max-width: 1380px;
  margin: 0 auto;
  padding: 24px 20px 40px;
}

.card,
.panel,
.hero-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.12);
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
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.05);
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
  background: rgba(59, 130, 246, 0.18);
  color: #93c5fd;
}

.status-idle {
  background: rgba(16, 185, 129, 0.16);
  color: #6ee7b7;
}

.hero-progress-track {
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.08);
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
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.05);
  padding: 10px 12px;
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
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
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
  background: rgba(255, 255, 255, 0.08);
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
  grid-template-columns: minmax(0, 1.35fr) 320px;
  gap: 18px;
  align-items: start;
}

.workspace-main,
.workspace-side {
  min-width: 0;
}

.workspace-side {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.workspace-tools-panel {
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.035);
  padding: 12px;
}

.tools-toolbar-head {
  margin-bottom: 12px;
}

.tools-toolbar-head h3 {
  margin-top: 6px;
  font-size: 1rem;
  font-weight: 600;
}

.compact-tools-head {
  margin-bottom: 10px;
}

.tools-toolbar-inline {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.inline-status-group,
.inline-action-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.inline-group-label {
  color: var(--text-secondary);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.tools-toolbar-block + .tools-toolbar-block {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.workspace-mini-section {
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.035);
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
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.04);
  padding: 16px;
}

.control-note-card span {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #93c5fd;
}

.control-note-card p {
  margin-top: 10px;
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
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.04);
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.sync-option-card:hover,
.sync-option-row:hover,
.quick-action-card:hover,
.ghost-action:hover {
  transform: translateY(-1px);
  background: rgba(255, 255, 255, 0.07);
}

.sync-option-card.active,
.sync-option-row.active {
  border-color: rgba(59, 130, 246, 0.42);
  background: rgba(37, 99, 235, 0.1);
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
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
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
.quick-action-list,
.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.source-chip-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.compact-source-grid {
  grid-template-columns: 1fr;
  gap: 8px;
}

.toolbar-source-grid {
  gap: 6px;
}

.source-chip-card {
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.04);
  padding: 12px;
}

.compact-source-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
}

.toolbar-source-card {
  padding: 8px 10px;
}

.source-chip-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quick-action-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.compact-quick-stack {
  gap: 8px;
}

.toolbar-quick-stack {
  gap: 6px;
}

.source-row,
.quick-action-card,
.history-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.04);
  padding: 14px 16px;
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
  background: rgba(16, 185, 129, 0.18);
  color: #6ee7b7;
}

.quick-action-blue {
  background: rgba(37, 99, 235, 0.18);
  color: #93c5fd;
}

.quick-action-violet {
  background: rgba(139, 92, 246, 0.18);
  color: #c4b5fd;
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
  .source-chip-grid {
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
  .source-chip-grid {
    grid-template-columns: 1fr;
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
