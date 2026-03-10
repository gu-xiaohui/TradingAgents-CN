<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
        </svg>
        数据库管理
      </h1>
      <p class="text-[var(--text-secondary)] mt-1">MongoDB + Redis 数据库管理和监控</p>
    </div>

    <!-- 连接状态 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- MongoDB -->
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
          </svg>
          MongoDB 连接状态
        </h3>
        
        <div class="space-y-4">
          <div>
            <span :class="mongoStatus.connected ? 'bg-[#22C55E]/20 text-[#22C55E]' : 'bg-[#EF4444]/20 text-[#EF4444]'" 
                  class="px-3 py-1 rounded-full text-sm font-medium">
              {{ mongoStatus.connected ? '已连接' : '未连接' }}
            </span>
          </div>
          
          <div v-if="mongoStatus.connected" class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">服务器:</span>
              <span class="font-mono">{{ mongoStatus.host }}:{{ mongoStatus.port }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">数据库:</span>
              <span>{{ mongoStatus.database }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">版本:</span>
              <span>{{ mongoStatus.version || 'Unknown' }}</span>
            </div>
            <div v-if="mongoStatus.connected_at" class="flex justify-between">
              <span class="text-[var(--text-secondary)]">连接时间:</span>
              <span>{{ formatDateTime(mongoStatus.connected_at) }}</span>
            </div>
          </div>
          
          <div class="flex gap-2 pt-2">
            <button @click="testConnections" :disabled="testing" 
                    class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors disabled:opacity-50">
              测试连接
            </button>
            <button @click="loadDatabaseStatus" :disabled="loading" 
                    class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-1.5 disabled:opacity-50">
              <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              刷新
            </button>
          </div>
        </div>
      </div>

      <!-- Redis -->
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 14.25h13.5m-13.5 0a3 3 0 01-3-3m3 3a3 3 0 100 6h13.5a3 3 0 100-6m-16.5-3a3 3 0 013-3h13.5a3 3 0 013 3m-19.5 0a4.5 4.5 0 01.9-2.7L5.737 5.1a3.375 3.375 0 012.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 01.9 2.7m0 0a3 3 0 01-3 3m0 3h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008zm-3 6h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008z" />
          </svg>
          Redis 连接状态
        </h3>
        
        <div class="space-y-4">
          <div>
            <span :class="redisStatus.connected ? 'bg-[#22C55E]/20 text-[#22C55E]' : 'bg-[#EF4444]/20 text-[#EF4444]'" 
                  class="px-3 py-1 rounded-full text-sm font-medium">
              {{ redisStatus.connected ? '已连接' : '未连接' }}
            </span>
          </div>
          
          <div v-if="redisStatus.connected" class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">服务器:</span>
              <span class="font-mono">{{ redisStatus.host }}:{{ redisStatus.port }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">数据库:</span>
              <span>{{ redisStatus.database }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-[var(--text-secondary)]">版本:</span>
              <span>{{ redisStatus.version || 'Unknown' }}</span>
            </div>
            <div v-if="redisStatus.memory_used" class="flex justify-between">
              <span class="text-[var(--text-secondary)]">内存使用:</span>
              <span>{{ formatBytes(redisStatus.memory_used) }}</span>
            </div>
          </div>
          
          <div class="flex gap-2 pt-2">
            <button @click="testConnections" :disabled="testing" 
                    class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors disabled:opacity-50">
              测试连接
            </button>
            <button @click="loadDatabaseStatus" :disabled="loading" 
                    class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-1.5 disabled:opacity-50">
              <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              刷新
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据库统计 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#22C55E]">{{ dbStats.totalCollections }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">MongoDB 集合数</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#3B82F6]">{{ dbStats.totalDocuments.toLocaleString() }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">总文档数</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#8B5CF6]">{{ formatBytes(dbStats.totalSize) }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">数据库大小</div>
      </div>
    </div>

    <!-- 数据管理操作 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 mb-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
        </svg>
        数据管理操作
      </h3>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 数据导出 -->
        <div class="space-y-4">
          <h4 class="font-medium flex items-center gap-2">
            <svg class="w-4 h-4 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>
            数据导出
          </h4>
          <p class="text-sm text-[var(--text-secondary)]">导出数据库数据到文件</p>
          
          <div class="space-y-3">
            <div>
              <label class="text-sm text-[var(--text-secondary)] block mb-1.5">导出格式</label>
              <select v-model="exportFormat" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
                <option value="xlsx">Excel</option>
              </select>
            </div>
            
            <div>
              <label class="text-sm text-[var(--text-secondary)] block mb-1.5">数据集合</label>
              <select v-model="exportCollection" class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
                <option value="config_and_reports">配置和报告（用于迁移）</option>
                <option value="config_only">配置数据（已脱敏）</option>
                <option value="analysis_reports">分析报告</option>
                <option value="user_configs">用户配置</option>
                <option value="operation_logs">操作日志</option>
              </select>
            </div>
            
            <button @click="exportData" :disabled="exporting" 
                    class="w-full px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50">
              <svg v-if="exporting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              导出数据
            </button>
          </div>
        </div>

        <!-- 数据导入 -->
        <div class="space-y-4">
          <h4 class="font-medium flex items-center gap-2">
            <svg class="w-4 h-4 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
            数据导入
          </h4>
          <p class="text-sm text-[var(--text-secondary)]">从导出文件导入数据</p>
          
          <div class="space-y-3">
            <div class="border-2 border-dashed border-[var(--border-color)] rounded-lg p-4 text-center hover:border-[#22C55E] transition-colors cursor-pointer"
                 @click="$refs.fileInput.click()">
              <input ref="fileInput" type="file" accept=".json" class="hidden" @change="handleFileChange">
              <svg class="w-8 h-8 mx-auto text-[var(--text-secondary)] mb-2" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
              </svg>
              <p class="text-sm text-[var(--text-secondary)]">
                {{ importFile ? importFile.name : '点击选择或拖拽文件' }}
              </p>
              <p class="text-xs text-[var(--text-secondary)] mt-1">仅支持 JSON 格式</p>
            </div>
            
            <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" v-model="importOverwrite" class="rounded border-[var(--border-color)]">
              <span>覆盖现有数据</span>
              <span class="text-[#F59E0B] text-xs">（将删除现有数据）</span>
            </label>
            
            <button @click="importData" :disabled="!importFile || importing" 
                    class="w-full px-4 py-2 bg-[#3B82F6] hover:bg-[#2563EB] text-white rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50">
              <svg v-if="importing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              导入数据
            </button>
          </div>
        </div>
      </div>
      
      <!-- 备份说明 -->
      <div class="mt-6 p-4 bg-[#3B82F6]/10 border border-[#3B82F6]/20 rounded-lg">
        <h4 class="font-medium text-[#3B82F6] mb-2">数据备份与还原</h4>
        <p class="text-sm text-[var(--text-secondary)] mb-3">建议使用 MongoDB 原生工具进行完整备份：</p>
        <div class="bg-[var(--bg-tertiary)] rounded p-3 text-xs font-mono space-y-2">
          <div><span class="text-[#22C55E]"># 备份</span></div>
          <div class="text-[#3B82F6]">mongodump --uri="mongodb://localhost:27017" --db=tradingagents --out=./backup --gzip</div>
          <div class="mt-2"><span class="text-[#22C55E]"># 还原</span></div>
          <div class="text-[#3B82F6]">mongorestore --uri="mongodb://localhost:27017" --db=tradingagents --gzip ./backup/tradingagents</div>
        </div>
      </div>
    </div>

    <!-- 数据清理 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center gap-2 text-[#EF4444]">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
        数据清理
      </h3>
      
      <div class="p-3 bg-[#EF4444]/10 border border-[#EF4444]/20 rounded-lg mb-4 text-sm text-[#EF4444]">
        以下操作将永久删除数据，请谨慎操作
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-3">
          <h4 class="font-medium">清理过期分析结果</h4>
          <p class="text-sm text-[var(--text-secondary)]">删除指定天数之前的分析结果</p>
          <div class="flex items-center gap-3">
            <input type="number" v-model="cleanupDays" min="1" max="365" 
                   class="w-24 px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <span class="text-sm text-[var(--text-secondary)]">天前</span>
          </div>
          <button @click="cleanupAnalysisResults" :disabled="cleaning" 
                  class="px-4 py-2 bg-[#F59E0B] hover:bg-[#D97706] text-white rounded-lg transition-colors text-sm disabled:opacity-50">
            清理分析结果
          </button>
        </div>
        
        <div class="space-y-3">
          <h4 class="font-medium">清理操作日志</h4>
          <p class="text-sm text-[var(--text-secondary)]">删除指定天数之前的操作日志</p>
          <div class="flex items-center gap-3">
            <input type="number" v-model="logCleanupDays" min="1" max="365" 
                   class="w-24 px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <span class="text-sm text-[var(--text-secondary)]">天前</span>
          </div>
          <button @click="cleanupOperationLogs" :disabled="cleaning" 
                  class="px-4 py-2 bg-[#F59E0B] hover:bg-[#D97706] text-white rounded-lg transition-colors text-sm disabled:opacity-50">
            清理操作日志
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  databaseApi,
  formatBytes,
  formatDateTime,
  type DatabaseStatus,
  type DatabaseStats
} from '@/api/database'

// 响应式数据
const loading = ref(false)
const exporting = ref(false)
const importing = ref(false)
const testing = ref(false)
const cleaning = ref(false)

const exportFormat = ref('json')
const exportCollection = ref('config_and_reports')
const importFile = ref<File | null>(null)
const importOverwrite = ref(false)
const cleanupDays = ref(30)
const logCleanupDays = ref(90)

// 数据状态
const databaseStatus = ref<DatabaseStatus | null>(null)
const databaseStats = ref<DatabaseStats | null>(null)

// 计算属性
const mongoStatus = computed(() => databaseStatus.value?.mongodb || {
  connected: false,
  host: 'localhost',
  port: 27017,
  database: 'tradingagents'
})

const redisStatus = computed(() => databaseStatus.value?.redis || {
  connected: false,
  host: 'localhost',
  port: 6379,
  database: 0
})

const dbStats = computed(() => ({
  totalCollections: databaseStats.value?.total_collections || 0,
  totalDocuments: databaseStats.value?.total_documents || 0,
  totalSize: databaseStats.value?.total_size || 0
}))

// 方法
const loadDatabaseStatus = async () => {
  try {
    loading.value = true
    const status = await databaseApi.getStatus()
    databaseStatus.value = status
  } catch (error) {
    console.error('加载数据库状态失败:', error)
    ElMessage.error('加载数据库状态失败')
  } finally {
    loading.value = false
  }
}

const loadDatabaseStats = async () => {
  try {
    const stats = await databaseApi.getStats()
    databaseStats.value = stats
  } catch (error) {
    console.error('加载数据库统计失败:', error)
    ElMessage.error('加载数据库统计失败')
  }
}

const testConnections = async () => {
  try {
    testing.value = true
    const response = await databaseApi.testConnections()
    const results = response.data
    
    if (results.overall) {
      ElMessage.success('数据库连接测试成功')
    } else {
      ElMessage.warning('部分数据库连接测试失败')
    }
    
    await loadDatabaseStatus()
  } catch (error) {
    console.error('连接测试失败:', error)
    ElMessage.error('连接测试失败')
  } finally {
    testing.value = false
  }
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    importFile.value = target.files[0]
  }
}

const exportData = async () => {
  try {
    exporting.value = true
    const response = await databaseApi.exportData({
      format: exportFormat.value,
      collection: exportCollection.value
    })
    
    // 创建下载链接
    const blob = new Blob([JSON.stringify(response, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `export_${exportCollection.value}_${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
    
    ElMessage.success('数据导出成功')
  } catch (error) {
    console.error('导出数据失败:', error)
    ElMessage.error('导出数据失败')
  } finally {
    exporting.value = false
  }
}

const importData = async () => {
  if (!importFile.value) return
  
  try {
    await ElMessageBox.confirm(
      importOverwrite.value 
        ? '确定要导入数据并覆盖现有数据吗？此操作不可恢复！' 
        : '确定要导入数据吗？',
      '确认导入',
      { type: 'warning' }
    )
    
    importing.value = true
    const formData = new FormData()
    formData.append('file', importFile.value)
    formData.append('overwrite', String(importOverwrite.value))
    
    await databaseApi.importData(formData)
    ElMessage.success('数据导入成功')
    await loadDatabaseStats()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('导入数据失败:', error)
      ElMessage.error('导入数据失败')
    }
  } finally {
    importing.value = false
  }
}

const cleanupAnalysisResults = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要清理 ${cleanupDays.value} 天前的分析结果吗？`,
      '确认清理',
      { type: 'warning' }
    )
    
    cleaning.value = true
    await databaseApi.cleanupAnalysisResults(cleanupDays.value)
    ElMessage.success(`已清理 ${cleanupDays.value} 天前的分析结果`)
    await loadDatabaseStats()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清理分析结果失败:', error)
      ElMessage.error('清理分析结果失败')
    }
  } finally {
    cleaning.value = false
  }
}

const cleanupOperationLogs = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要清理 ${logCleanupDays.value} 天前的操作日志吗？`,
      '确认清理',
      { type: 'warning' }
    )
    
    cleaning.value = true
    await databaseApi.cleanupOperationLogs(logCleanupDays.value)
    ElMessage.success(`已清理 ${logCleanupDays.value} 天前的操作日志`)
    await loadDatabaseStats()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清理操作日志失败:', error)
      ElMessage.error('清理操作日志失败')
    }
  } finally {
    cleaning.value = false
  }
}

// 生命周期
onMounted(() => {
  loadDatabaseStatus()
  loadDatabaseStats()
})
</script>
