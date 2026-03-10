<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 mb-6">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-3">
            <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            定时任务管理
          </h1>
          <p class="text-[var(--text-secondary)] mt-1">管理系统中的所有定时任务，支持暂停、恢复和手动触发</p>
        </div>
        <div class="flex gap-2">
          <button @click="loadJobs" :disabled="loading" 
                  class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-2">
            <svg :class="{ 'animate-spin': loading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            刷新
          </button>
          <button @click="showHistoryDialog" 
                  class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
            执行历史
          </button>
        </div>
      </div>
      
      <!-- 统计 -->
      <div v-if="stats" class="flex gap-8 mt-4 pt-4 border-t border-[var(--border-color)]">
        <div class="text-center">
          <div class="text-xl font-bold">{{ stats.total_jobs }}</div>
          <div class="text-xs text-[var(--text-secondary)]">总任务数</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-[#22C55E]">{{ stats.running_jobs }}</div>
          <div class="text-xs text-[var(--text-secondary)]">运行中</div>
        </div>
        <div class="text-center">
          <div class="text-xl font-bold text-[#F59E0B]">{{ stats.paused_jobs }}</div>
          <div class="text-xs text-[var(--text-secondary)]">已暂停</div>
        </div>
      </div>
    </div>

    <!-- 筛选 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-4 mb-6">
      <div class="flex flex-wrap gap-4">
        <input type="text" v-model="searchKeyword" placeholder="搜索任务名称" 
               class="flex-1 min-w-[200px] px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
        <select v-model="filterStatus" class="w-40 px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
          <option value="">全部状态</option>
          <option value="running">运行中</option>
          <option value="paused">已暂停</option>
        </select>
        <button @click="handleReset" class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
          重置
        </button>
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

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">任务名称</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">触发器</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">备注</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">下次执行</th>
              <th class="text-center py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="job in filteredJobs" :key="job.id" class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)]">
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <span :class="job.paused ? 'bg-[#F59E0B]/20 text-[#F59E0B]' : 'bg-[#22C55E]/20 text-[#22C55E]'" 
                        class="px-2 py-0.5 rounded text-xs font-medium">
                    {{ job.paused ? '已暂停' : '运行中' }}
                  </span>
                  <span>{{ job.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatTrigger(job.trigger) }}</td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ job.description || '-' }}</td>
              <td class="py-3 px-4">
                <div v-if="job.next_run_time" class="text-sm">
                  {{ formatDateTime(job.next_run_time) }}
                </div>
                <div v-else class="text-sm text-[#F59E0B]">已暂停</div>
              </td>
              <td class="py-3 px-4">
                <div class="flex items-center justify-center gap-2">
                  <button @click="handlePause(job)" v-if="!job.paused" 
                          class="px-2 py-1 text-sm bg-[#F59E0B] hover:bg-[#D97706] text-white rounded transition-colors">
                    暂停
                  </button>
                  <button @click="handleResume(job)" v-else 
                          class="px-2 py-1 text-sm bg-[#22C55E] hover:bg-[#16A34A] text-white rounded transition-colors">
                    恢复
                  </button>
                  <button @click="handleTrigger(job)" 
                          class="px-2 py-1 text-sm bg-[#3B82F6] hover:bg-[#2563EB] text-white rounded transition-colors">
                    执行
                  </button>
                  <button @click="showJobDetail(job)" 
                          class="px-2 py-1 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded transition-colors">
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
        <div v-if="currentJob" class="space-y-3 text-sm">
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">任务ID</span>
            <span class="font-mono">{{ currentJob.id }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">任务名称</span>
            <span>{{ currentJob.name }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">状态</span>
            <span :class="currentJob.paused ? 'text-[#F59E0B]' : 'text-[#22C55E]'">
              {{ currentJob.paused ? '已暂停' : '运行中' }}
            </span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">触发器</span>
            <span>{{ currentJob.trigger }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">下次执行</span>
            <span>{{ currentJob.next_run_time ? formatDateTime(currentJob.next_run_time) : '已暂停' }}</span>
          </div>
          <div v-if="currentJob.func" class="flex justify-between py-2 border-b border-[var(--border-color)]">
            <span class="text-[var(--text-secondary)]">执行函数</span>
            <span class="font-mono text-xs">{{ currentJob.func }}</span>
          </div>
          <div v-if="currentJob.kwargs" class="py-2">
            <span class="text-[var(--text-secondary)] block mb-2">参数</span>
            <pre class="p-3 bg-[var(--bg-tertiary)] rounded-lg text-xs overflow-x-auto">{{ JSON.stringify(currentJob.kwargs, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { schedulerApi } from '@/api/scheduler'

const loading = ref(false)
const searchKeyword = ref('')
const filterStatus = ref('')
const detailDialogVisible = ref(false)
const currentJob = ref<any>(null)
const historyDialogVisible = ref(false)

const jobs = ref<any[]>([])
const stats = ref<any>(null)

const filteredJobs = computed(() => {
  let result = jobs.value
  if (searchKeyword.value) {
    result = result.filter(j => j.name.toLowerCase().includes(searchKeyword.value.toLowerCase()))
  }
  if (filterStatus.value === 'running') {
    result = result.filter(j => !j.paused)
  } else if (filterStatus.value === 'paused') {
    result = result.filter(j => j.paused)
  }
  return result
})

const formatTrigger = (trigger: string) => {
  if (!trigger) return '-'
  return trigger.replace(/interval\[|\]|cron\[|/g, '').replace(/,/g, ', ')
}

const formatDateTime = (date: string) => new Date(date).toLocaleString('zh-CN')

const loadJobs = async () => {
  loading.value = true
  try {
    const res = await schedulerApi.getJobs()
    jobs.value = res.data?.jobs || []
    stats.value = {
      total_jobs: jobs.value.length,
      running_jobs: jobs.value.filter(j => !j.paused).length,
      paused_jobs: jobs.value.filter(j => j.paused).length
    }
  } catch (error) {
    console.error('加载任务失败:', error)
    ElMessage.error('加载任务失败')
  } finally {
    loading.value = false
  }
}

const handlePause = async (job: any) => {
  try {
    await schedulerApi.pauseJob(job.id)
    ElMessage.success('任务已暂停')
    loadJobs()
  } catch (error) {
    ElMessage.error('暂停任务失败')
  }
}

const handleResume = async (job: any) => {
  try {
    await schedulerApi.resumeJob(job.id)
    ElMessage.success('任务已恢复')
    loadJobs()
  } catch (error) {
    ElMessage.error('恢复任务失败')
  }
}

const handleTrigger = async (job: any) => {
  try {
    await schedulerApi.triggerJob(job.id)
    ElMessage.success('任务已触发执行')
  } catch (error) {
    ElMessage.error('触发任务失败')
  }
}

const showJobDetail = (job: any) => {
  currentJob.value = job
  detailDialogVisible.value = true
}

const showHistoryDialog = () => {
  ElMessage.info('执行历史功能开发中')
}

const handleReset = () => {
  searchKeyword.value = ''
  filterStatus.value = ''
}

onMounted(() => {
  loadJobs()
})
</script>
