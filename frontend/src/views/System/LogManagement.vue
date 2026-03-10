<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        日志管理
      </h1>
      <div class="flex gap-2">
        <button @click="loadLogFiles" :disabled="loading" 
                class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2">
          <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
        <button @click="showExportDialog" 
                class="px-4 py-2 bg-[#3B82F6] hover:bg-[#2563EB] text-white rounded-lg transition-colors flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
          导出日志
        </button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#22C55E]">{{ statistics.total_files }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">日志文件数</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#3B82F6]">{{ statistics.total_size_mb.toFixed(2) }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">总大小 (MB)</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#EF4444]">{{ statistics.error_files }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">错误日志文件</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 flex items-center justify-center">
        <button @click="loadStatistics" class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
          刷新统计
        </button>
      </div>
    </div>

    <!-- 日志文件列表 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">日志文件列表</h3>
        <input type="text" v-model="searchKeyword" placeholder="搜索文件名" 
               class="px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm w-64">
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
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">文件名</th>
              <th class="text-right py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">大小 (MB)</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">修改时间</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="file in filteredLogFiles" :key="file.name" class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)]">
              <td class="py-3 px-4">
                <span :class="getLogTypeClass(file.type)" class="px-2 py-1 rounded text-xs font-medium mr-2">
                  {{ file.type }}
                </span>
                {{ file.name }}
              </td>
              <td class="py-3 px-4 text-right">{{ file.size_mb.toFixed(2) }}</td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatDate(file.modified_at) }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center justify-center gap-2">
                  <button @click="viewLog(file)" class="px-2 py-1 text-sm text-[#3B82F6] hover:text-[#2563EB]">查看</button>
                  <button @click="downloadLog(file)" class="px-2 py-1 text-sm text-[#22C55E] hover:text-[#16A34A]">下载</button>
                  <button @click="deleteLog(file)" class="px-2 py-1 text-sm text-[#EF4444] hover:text-[#DC2626]">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 查看日志弹窗 -->
    <div v-if="viewDialogVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="viewDialogVisible = false">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 w-full max-w-4xl mx-4 max-h-[80vh] overflow-hidden flex flex-col" @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">{{ currentLog?.name }}</h3>
          <button @click="viewDialogVisible = false" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex gap-2 mb-4">
          <button @click="tailLines = 100" :class="tailLines === 100 ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)]'" class="px-3 py-1 rounded text-sm">最近100行</button>
          <button @click="tailLines = 500" :class="tailLines === 500 ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)]'" class="px-3 py-1 rounded text-sm">最近500行</button>
          <button @click="tailLines = 1000" :class="tailLines === 1000 ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)]'" class="px-3 py-1 rounded text-sm">最近1000行</button>
          <button @click="tailLines = 0" :class="tailLines === 0 ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)]'" class="px-3 py-1 rounded text-sm">全部</button>
        </div>
        <pre class="flex-1 overflow-auto bg-[var(--bg-tertiary)] p-4 rounded-lg text-xs font-mono">{{ logContent }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { logsApi } from '@/api/logs'

const loading = ref(false)
const viewDialogVisible = ref(false)
const currentLog = ref<any>(null)
const logContent = ref('')
const tailLines = ref(100)
const searchKeyword = ref('')

const logFiles = ref<any[]>([])
const statistics = ref({
  total_files: 0,
  total_size_mb: 0,
  error_files: 0
})

const filteredLogFiles = computed(() => {
  if (!searchKeyword.value) return logFiles.value
  return logFiles.value.filter(f => f.name.toLowerCase().includes(searchKeyword.value.toLowerCase()))
})

const getLogTypeClass = (type: string): string => {
  const classMap: Record<string, string> = {
    'error': 'bg-[#EF4444]/20 text-[#EF4444]',
    'info': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'warning': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'debug': 'bg-[#8B5CF6]/20 text-[#8B5CF6]'
  }
  return classMap[type] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const formatDate = (date: string) => new Date(date).toLocaleString('zh-CN')

const loadLogFiles = async () => {
  loading.value = true
  try {
    const res = await logsApi.getLogFiles()
    logFiles.value = res.data || []
  } catch (error) {
    console.error('加载日志文件失败:', error)
    ElMessage.error('加载日志文件失败')
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  try {
    const res = await logsApi.getStatistics()
    statistics.value = res.data || statistics.value
    ElMessage.success('统计信息已刷新')
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const viewLog = async (file: any) => {
  currentLog.value = file
  viewDialogVisible.value = true
  try {
    const res = await logsApi.getLogContent(file.name, tailLines.value)
    logContent.value = res.data || ''
  } catch (error) {
    logContent.value = '加载日志内容失败'
  }
}

const downloadLog = async (file: any) => {
  try {
    const res = await logsApi.downloadLog(file.name)
    const url = window.URL.createObjectURL(new Blob([res]))
    const link = document.createElement('a')
    link.href = url
    link.download = file.name
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载日志失败')
  }
}

const deleteLog = async (file: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除日志文件 ${file.name} 吗？`, '确认删除', { type: 'warning' })
    await logsApi.deleteLog(file.name)
    ElMessage.success('日志文件已删除')
    loadLogFiles()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error('删除日志失败')
  }
}

const showExportDialog = () => {
  ElMessage.info('导出功能开发中')
}

onMounted(() => {
  loadLogFiles()
  loadStatistics()
})
</script>
