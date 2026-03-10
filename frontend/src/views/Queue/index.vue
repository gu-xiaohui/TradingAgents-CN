<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold flex items-center gap-3">
          <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3 12h3.375c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H3v12h3.375c.621 0 1.125-.504 1.125-1.125v-2.25c0-.621-.504-1.125-1.125-1.125H3V12z" />
          </svg>
          任务队列
        </h1>
        <p class="text-[var(--text-secondary)] mt-1">实时监控和管理分析任务状态</p>
      </div>
      <div class="flex gap-2">
        <button @click="refreshQueue" :disabled="loading" 
                class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-2">
          <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
        <button @click="clearCompleted" 
                class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
          清理已完成
        </button>
      </div>
    </div>

    <!-- 统计 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#F59E0B]">{{ stats.pending }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">等待中</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#3B82F6]">{{ stats.running }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">执行中</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#22C55E]">{{ stats.completed }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">已完成</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#EF4444]">{{ stats.failed }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">失败</div>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <div v-if="loading" class="flex items-center justify-center py-8">
        <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else-if="queueTasks.length === 0" class="text-center py-12 text-[var(--text-secondary)]">
        暂无任务
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">任务ID</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">股票代码</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">股票名称</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">状态</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">进度</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">优先级</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">创建时间</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in queueTasks" :key="task.task_id" class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)]">
              <td class="py-3 px-4">
                <span @click="viewTaskDetail(task)" class="text-[#3B82F6] hover:text-[#2563EB] cursor-pointer font-mono text-sm">
                  {{ task.task_id.substring(0, 8) }}...
                </span>
              </td>
              <td class="py-3 px-4 font-mono">{{ task.stock_code }}</td>
              <td class="py-3 px-4">{{ task.stock_name }}</td>
              <td class="py-3 px-4 text-center">
                <span :class="getStatusClass(task.status)" class="px-2 py-1 rounded text-xs font-medium">
                  {{ getStatusText(task.status) }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-2 bg-[var(--bg-tertiary)] rounded-full overflow-hidden">
                    <div :class="getProgressClass(task.status)" 
                         class="h-full transition-all duration-300"
                         :style="{ width: task.progress + '%' }"></div>
                  </div>
                  <span class="text-xs text-[var(--text-secondary)] w-10">{{ task.progress }}%</span>
                </div>
              </td>
              <td class="py-3 px-4 text-center">
                <span v-if="task.priority > 0" class="px-2 py-0.5 bg-[#F59E0B]/20 text-[#F59E0B] rounded text-xs">
                  高
                </span>
                <span v-else class="text-[var(--text-secondary)]">普通</span>
              </td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatTime(task.created_at) }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center justify-center gap-2">
                  <button v-if="task.status === 'pending'" @click="cancelTask(task)" 
                          class="px-2 py-1 text-sm text-[#EF4444] hover:text-[#DC2626]">
                    取消
                  </button>
                  <button v-if="task.status === 'failed'" @click="retryTask(task)" 
                          class="px-2 py-1 text-sm text-[#22C55E] hover:text-[#16A34A]">
                    重试
                  </button>
                  <button @click="viewTaskDetail(task)" 
                          class="px-2 py-1 text-sm text-[#3B82F6] hover:text-[#2563EB]">
                    详情
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <div v-if="detailDialogVisible" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click="detailDialogVisible = false">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6 w-full max-w-xl mx-4" @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">任务详情</h3>
          <button @click="detailDialogVisible = false" class="text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div v-if="currentTask" class="space-y-3 text-sm">
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">任务ID</span>
            <span class="font-mono">{{ currentTask.task_id }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">股票</span>
            <span>{{ currentTask.stock_code }} {{ currentTask.stock_name }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">状态</span>
            <span :class="getStatusClass(currentTask.status)">{{ getStatusText(currentTask.status) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">进度</span>
            <span>{{ currentTask.progress }}%</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">创建时间</span>
            <span>{{ formatTime(currentTask.created_at) }}</span>
          </div>
          <div v-if="currentTask.error" class="py-2">
            <span class="text-[var(--text-secondary)] block mb-1">错误信息</span>
            <pre class="p-3 bg-[#EF4444]/10 rounded text-xs text-[#EF4444] overflow-x-auto">{{ currentTask.error }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { queueApi } from '@/api/queue'

const loading = ref(false)
const detailDialogVisible = ref(false)
const currentTask = ref<any>(null)

const stats = reactive({ pending: 0, running: 0, completed: 0, failed: 0 })
const queueTasks = ref<any[]>([])

let refreshInterval: any = null

const formatTime = (date: string) => new Date(date).toLocaleString('zh-CN')

const getStatusClass = (status: string): string => {
  const classMap: Record<string, string> = {
    'pending': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'running': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'completed': 'bg-[#22C55E]/20 text-[#22C55E]',
    'failed': 'bg-[#EF4444]/20 text-[#EF4444]'
  }
  return classMap[status] || ''
}

const getStatusText = (status: string): string => {
  const textMap: Record<string, string> = {
    'pending': '等待中',
    'running': '执行中',
    'completed': '已完成',
    'failed': '失败'
  }
  return textMap[status] || status
}

const getProgressClass = (status: string): string => {
  if (status === 'completed') return 'bg-[#22C55E]'
  if (status === 'failed') return 'bg-[#EF4444]'
  return 'bg-[#3B82F6]'
}

const refreshQueue = async () => {
  loading.value = true
  try {
    const res = await queueApi.getTasks()
    queueTasks.value = res.data?.tasks || []
    stats.pending = queueTasks.value.filter(t => t.status === 'pending').length
    stats.running = queueTasks.value.filter(t => t.status === 'running').length
    stats.completed = queueTasks.value.filter(t => t.status === 'completed').length
    stats.failed = queueTasks.value.filter(t => t.status === 'failed').length
  } catch (error) {
    console.error('刷新队列失败:', error)
  } finally {
    loading.value = false
  }
}

const clearCompleted = async () => {
  try {
    await queueApi.clearCompleted()
    ElMessage.success('已清理完成任务')
    refreshQueue()
  } catch (error) {
    ElMessage.error('清理失败')
  }
}

const viewTaskDetail = (task: any) => {
  currentTask.value = task
  detailDialogVisible.value = true
}

const cancelTask = async (task: any) => {
  try {
    await queueApi.cancelTask(task.task_id)
    ElMessage.success('已取消任务')
    refreshQueue()
  } catch (error) {
    ElMessage.error('取消失败')
  }
}

const retryTask = async (task: any) => {
  try {
    await queueApi.retryTask(task.task_id)
    ElMessage.success('已重新执行')
    refreshQueue()
  } catch (error) {
    ElMessage.error('重试失败')
  }
}

onMounted(() => {
  refreshQueue()
  refreshInterval = setInterval(refreshQueue, 5000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>
