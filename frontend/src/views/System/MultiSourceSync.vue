<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold flex items-center gap-3">
          <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
          </svg>
          多数据源同步
        </h1>
        <p class="text-[var(--text-secondary)] mt-1">管理和监控多个数据源的股票基础信息同步</p>
      </div>
      <button @click="runFullTest" :disabled="testing" 
              class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2">
        <svg v-if="testing" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
        </svg>
        全面测试
      </button>
    </div>

    <!-- 数据源状态 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">数据源状态</h3>
        <div class="space-y-3">
          <div v-for="source in dataSources" :key="source.name" 
               class="flex items-center justify-between p-3 bg-[var(--bg-tertiary)] rounded-lg">
            <div class="flex items-center gap-3">
              <div :class="source.available ? 'bg-[#22C55E]' : 'bg-[#EF4444]'" 
                   class="w-2 h-2 rounded-full"></div>
              <span class="font-medium">{{ source.name }}</span>
            </div>
            <div class="flex items-center gap-4">
              <span class="text-sm text-[var(--text-secondary)]">优先级: {{ source.priority }}</span>
              <span :class="source.available ? 'text-[#22C55E]' : 'text-[#EF4444]'" class="text-sm font-medium">
                {{ source.available ? '可用' : '不可用' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
        <h3 class="text-lg font-semibold mb-4">同步控制</h3>
        <div class="space-y-4">
          <div>
            <label class="text-sm text-[var(--text-secondary)] block mb-1.5">股票代码列表</label>
            <textarea v-model="symbolsInput" rows="3" placeholder="输入股票代码，逗号分隔" 
                      class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm resize-none"></textarea>
          </div>
          <div class="flex gap-2">
            <button @click="startSync" :disabled="syncing" 
                    class="flex-1 px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors disabled:opacity-50">
              {{ syncing ? '同步中...' : '开始同步' }}
            </button>
            <button @click="stopSync" :disabled="!syncing" 
                    class="px-4 py-2 bg-[#EF4444] hover:bg-[#DC2626] text-white rounded-lg transition-colors disabled:opacity-50">
              停止
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 同步历史 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <h3 class="text-lg font-semibold mb-4">同步历史</h3>
      <div v-if="syncHistory.length === 0" class="text-center py-8 text-[var(--text-secondary)]">
        暂无同步记录
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">时间</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">股票数</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">数据源</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in syncHistory" :key="item.id" class="border-b border-[var(--border-color)]">
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatDateTime(item.timestamp) }}</td>
              <td class="py-3 px-4">{{ item.count }}</td>
              <td class="py-3 px-4">{{ item.source }}</td>
              <td class="py-3 px-4 text-center">
                <span :class="item.success ? 'bg-[#22C55E]/20 text-[#22C55E]' : 'bg-[#EF4444]/20 text-[#EF4444]'" 
                      class="px-2 py-1 rounded text-xs font-medium">
                  {{ item.success ? '成功' : '失败' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 测试结果弹窗 -->
    <div v-if="testDialogVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="testDialogVisible = false">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 w-full max-w-2xl mx-4" @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">全面测试结果</h3>
          <button @click="testDialogVisible = false" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-3">
          <div v-for="result in testResults" :key="result.name" 
               class="p-4 rounded-lg border border-[var(--border-color)]">
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium">{{ result.name }}</span>
              <span :class="result.available ? 'text-[#22C55E]' : 'text-[#EF4444]'" class="font-medium">
                {{ result.available ? '可用' : '不可用' }}
              </span>
            </div>
            <p class="text-sm text-[var(--text-secondary)]">{{ result.message }}</p>
            <div class="mt-2 text-xs text-[var(--text-secondary)]">
              响应时间: {{ result.response_time }}ms | 优先级: {{ result.priority }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as syncApi from '@/api/sync'

// 包装 syncApi 以匹配组件中使用的 multiSourceApi
const multiSourceApi = {
  getDataSources: () => syncApi.getDataSourcesStatus(),
  getSyncHistory: () => syncApi.getSyncStatus().then((res: any) => ({ data: res.data?.history || [] })),
  runFullTest: () => syncApi.testDataSources(),
  startSync: (params: any) => syncApi.startSync(params),
  stopSync: () => syncApi.stopSync()
}

const testing = ref(false)
const syncing = ref(false)
const testDialogVisible = ref(false)
const symbolsInput = ref('')

const dataSources = ref<any[]>([])
const testResults = ref<any[]>([])
const syncHistory = ref<any[]>([])

const formatDateTime = (date: string) => new Date(date).toLocaleString('zh-CN')

const loadDataSources = async () => {
  try {
    const res = await multiSourceApi.getDataSources()
    dataSources.value = res.data || []
  } catch (error) {
    console.error('加载数据源失败:', error)
  }
}

const loadSyncHistory = async () => {
  try {
    const res = await multiSourceApi.getSyncHistory()
    syncHistory.value = res.data || []
  } catch (error) {
    console.error('加载同步历史失败:', error)
  }
}

const runFullTest = async () => {
  testing.value = true
  try {
    const res = await multiSourceApi.runFullTest()
    testResults.value = res.data || []
    testDialogVisible.value = true
    // 更新数据源状态
    testResults.value.forEach(result => {
      const source = dataSources.value.find(s => s.name === result.name)
      if (source) source.available = result.available
    })
  } catch (error) {
    ElMessage.error('测试失败')
  } finally {
    testing.value = false
  }
}

const startSync = async () => {
  if (!symbolsInput.value.trim()) {
    ElMessage.warning('请输入股票代码')
    return
  }
  syncing.value = true
  try {
    const symbols = symbolsInput.value.split(',').map(s => s.trim()).filter(Boolean)
    await multiSourceApi.startSync({ symbols })
    ElMessage.success('同步任务已启动')
    loadSyncHistory()
  } catch (error) {
    ElMessage.error('启动同步失败')
  } finally {
    syncing.value = false
  }
}

const stopSync = async () => {
  try {
    await multiSourceApi.stopSync()
    ElMessage.success('同步已停止')
    syncing.value = false
  } catch (error) {
    ElMessage.error('停止同步失败')
  }
}

onMounted(() => {
  loadDataSources()
  loadSyncHistory()
})
</script>
