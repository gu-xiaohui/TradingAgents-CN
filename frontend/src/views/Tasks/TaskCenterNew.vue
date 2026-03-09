<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
        </div>
        任务中心
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">统一查看并管理分析任务：进行中 / 已完成 / 失败</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="card p-4 flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-[#3B82F6]/20 flex items-center justify-center">
          <svg class="w-6 h-6 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-[var(--text-primary)]">{{ stats.total }}</div>
          <div class="text-sm text-[var(--text-muted)]">总任务</div>
        </div>
      </div>
      <div class="card p-4 flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-[#22C55E]/20 flex items-center justify-center">
          <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-[#22C55E]">{{ stats.completed }}</div>
          <div class="text-sm text-[var(--text-muted)]">已完成</div>
        </div>
      </div>
      <div class="card p-4 flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-[#EF4444]/20 flex items-center justify-center">
          <svg class="w-6 h-6 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-[#EF4444]">{{ stats.failed }}</div>
          <div class="text-sm text-[var(--text-muted)]">失败</div>
        </div>
      </div>
      <div class="card p-4 flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-[#8B5CF6]/20 flex items-center justify-center">
          <svg class="w-6 h-6 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-[#8B5CF6]">{{ stats.uniqueStocks }}</div>
          <div class="text-sm text-[var(--text-muted)]">股票数</div>
        </div>
      </div>
    </div>

    <!-- 筛选和标签页 -->
    <div class="card">
      <!-- 标签页 -->
      <div class="flex items-center gap-1 mb-6 border-b border-white/10 pb-4">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="activeTab === tab.value 
            ? 'bg-[#22C55E]/10 text-[#22C55E]' 
            : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'"
        >
          {{ tab.label }}
          <span class="ml-2 px-2 py-0.5 rounded-full text-xs" :class="activeTab === tab.value ? 'bg-[#22C55E]/20' : 'bg-white/10'">
            {{ tab.count }}
          </span>
        </button>
      </div>

      <!-- 筛选表单 -->
      <div class="flex items-center gap-4 mb-6">
        <input
          v-model="keyword"
          type="text"
          placeholder="搜索股票代码/名称..."
          class="input flex-1 max-w-xs"
        />
        <select v-model="filters.market" class="input w-32">
          <option value="">全部市场</option>
          <option value="A股">A股</option>
          <option value="美股">美股</option>
          <option value="港股">港股</option>
        </select>
        <button @click="refreshList" class="btn-secondary flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          刷新
        </button>
      </div>

      <!-- 任务列表 -->
      <div class="space-y-3">
        <div
          v-for="task in filteredTasks"
          :key="task.task_id"
          class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
        >
          <div class="flex items-center gap-4">
            <!-- 状态图标 -->
            <div 
              class="w-10 h-10 rounded-lg flex items-center justify-center"
              :class="{
                'bg-[#F59E0B]/20': task.status === 'running' || task.status === 'processing',
                'bg-[#22C55E]/20': task.status === 'completed',
                'bg-[#EF4444]/20': task.status === 'failed',
                'bg-[#64748B]/20': task.status === 'pending'
              }"
            >
              <svg v-if="task.status === 'running' || task.status === 'processing'" class="w-5 h-5 text-[#F59E0B] animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else-if="task.status === 'completed'" class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="task.status === 'failed'" class="w-5 h-5 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else class="w-5 h-5 text-[var(--text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <div>
              <div class="flex items-center gap-2">
                <span class="font-mono font-medium text-[var(--text-primary)]">{{ task.stock_code }}</span>
                <span class="text-sm text-[var(--text-secondary)]">{{ task.stock_name }}</span>
                <span 
                  class="text-xs px-2 py-0.5 rounded-full"
                  :class="{
                    'bg-[#F59E0B]/20 text-[#F59E0B]': task.status === 'running' || task.status === 'processing',
                    'bg-[#22C55E]/20 text-[#22C55E]': task.status === 'completed',
                    'bg-[#EF4444]/20 text-[#EF4444]': task.status === 'failed',
                    'bg-[#64748B]/20 text-[var(--text-muted)]': task.status === 'pending'
                  }"
                >
                  {{ getStatusText(task.status) }}
                </span>
              </div>
              <div class="text-xs text-[var(--text-muted)] mt-1">
                {{ formatTime(task.start_time || task.created_at) }}
              </div>
            </div>
          </div>

          <!-- 进度条 -->
          <div v-if="task.status === 'running' || task.status === 'processing'" class="w-32">
            <div class="h-2 bg-white/10 rounded-full overflow-hidden">
              <div 
                class="h-full bg-gradient-to-r from-[#22C55E] to-[#8B5CF6] transition-all"
                :style="{ width: `${task.progress || 0}%` }"
              ></div>
            </div>
            <div class="text-xs text-[var(--text-muted)] text-center mt-1">{{ task.progress || 0 }}%</div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex items-center gap-2">
            <button
              v-if="task.status === 'completed'"
              @click="viewReport(task)"
              class="px-3 py-1.5 rounded-lg text-sm bg-[#22C55E]/10 text-[#22C55E] hover:bg-[#22C55E]/20 transition-colors"
            >
              查看报告
            </button>
            <button
              v-if="task.status === 'failed'"
              @click="retryTask(task)"
              class="px-3 py-1.5 rounded-lg text-sm bg-[#F59E0B]/10 text-[#F59E0B] hover:bg-[#F59E0B]/20 transition-colors"
            >
              重试
            </button>
            <button
              @click="deleteTask(task)"
              class="px-3 py-1.5 rounded-lg text-sm bg-[#EF4444]/10 text-[#EF4444] hover:bg-[#EF4444]/20 transition-colors"
            >
              删除
            </button>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="filteredTasks.length === 0" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto mb-4 text-[var(--text-muted)] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="text-[var(--text-muted)]">暂无任务</p>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="total > pageSize" class="flex items-center justify-between mt-6 pt-4 border-t border-white/10">
        <div class="text-sm text-[var(--text-muted)]">共 {{ total }} 条记录</div>
        <div class="flex items-center gap-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-1.5 rounded-lg text-sm bg-white/5 text-[var(--text-secondary)] hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            上一页
          </button>
          <span class="text-sm text-[var(--text-primary)]">{{ currentPage }} / {{ totalPages }}</span>
          <button
            @click="currentPage++"
            :disabled="currentPage >= totalPages"
            class="px-3 py-1.5 rounded-lg text-sm bg-white/5 text-[var(--text-secondary)] hover:bg-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            下一页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const activeTab = ref('all')
const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filters = reactive({
  market: '',
  dateRange: null as [string, string] | null
})

const stats = reactive({
  total: 156,
  completed: 142,
  failed: 8,
  uniqueStocks: 45
})

const tabs = computed(() => [
  { label: '全部', value: 'all', count: stats.total },
  { label: '进行中', value: 'running', count: 6 },
  { label: '已完成', value: 'completed', count: stats.completed },
  { label: '失败', value: 'failed', count: stats.failed },
])

// 模拟任务数据
const tasks = ref([
  { task_id: 'task-001', stock_code: '002594', stock_name: '比亚迪', status: 'completed', progress: 100, start_time: '2026-03-09 22:43:01' },
  { task_id: 'task-002', stock_code: '688981', stock_name: '中芯国际', status: 'completed', progress: 100, start_time: '2026-03-09 08:02:30' },
  { task_id: 'task-003', stock_code: '600519', stock_name: '贵州茅台', status: 'running', progress: 65, start_time: '2026-03-10 07:00:00' },
  { task_id: 'task-004', stock_code: '000001', stock_name: '平安银行', status: 'failed', progress: 0, start_time: '2026-03-09 13:53:10' },
  { task_id: 'task-005', stock_code: '300750', stock_name: '宁德时代', status: 'pending', progress: 0, start_time: '2026-03-10 06:30:00' },
])

const filteredTasks = computed(() => {
  let result = [...tasks.value]
  
  if (activeTab.value !== 'all') {
    result = result.filter(t => t.status === activeTab.value)
  }
  
  if (keyword.value) {
    const kw = keyword.value.toLowerCase()
    result = result.filter(t => 
      t.stock_code.toLowerCase().includes(kw) || 
      t.stock_name.toLowerCase().includes(kw)
    )
  }
  
  if (filters.market) {
    // 实际项目中需要根据市场筛选
  }
  
  total.value = result.length
  return result
})

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '等待中',
    running: '进行中',
    processing: '进行中',
    completed: '已完成',
    failed: '失败'
  }
  return map[status] || status
}

const formatTime = (time: string) => {
  return time || '-'
}

const refreshList = () => {
  ElMessage.success('已刷新')
}

const viewReport = (task: any) => {
  router.push(`/reports/${task.task_id}`)
}

const retryTask = (task: any) => {
  ElMessage.success(`已重试任务: ${task.stock_code}`)
}

const deleteTask = async (task: any) => {
  try {
    await ElMessageBox.confirm('确定删除该任务？', '确认删除', { type: 'warning' })
    const index = tasks.value.findIndex(t => t.task_id === task.task_id)
    if (index > -1) {
      tasks.value.splice(index, 1)
      ElMessage.success('已删除')
    }
  } catch {}
}

onMounted(() => {
  // 加载任务列表
})
</script>
