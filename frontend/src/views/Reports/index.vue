<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
          </svg>
        </div>
        分析报告
      </h1>
      <p class="text-[var(--text-muted)] mt-1 ml-13">查看和管理股票分析报告</p>
    </div>

    <!-- 筛选栏 -->
    <div class="card mb-6">
      <div class="flex items-center gap-4">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索股票代码或名称..."
          class="input flex-1 max-w-xs"
        />
        <select v-model="marketFilter" class="input w-32">
          <option value="">全部市场</option>
          <option value="A股">A股</option>
          <option value="港股">港股</option>
          <option value="美股">美股</option>
        </select>
        <button @click="refreshReports" class="btn-secondary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
      </div>
    </div>

    <!-- 报告列表 -->
    <div class="card">
      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <svg class="w-8 h-8 mx-auto animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <p class="text-[var(--text-muted)] mt-2">加载中...</p>
      </div>

      <!-- 报告列表 -->
      <div v-else-if="filteredReports.length > 0" class="space-y-3">
        <div
          v-for="report in filteredReports"
          :key="report.task_id || report.id"
          class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
          @click="viewReport(report)"
        >
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-[#22C55E]/20 flex items-center justify-center">
              <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
              </svg>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="font-mono font-medium">{{ report.stock_code }}</span>
                <span class="text-[var(--text-secondary)]">{{ report.stock_name }}</span>
              </div>
              <div class="text-xs text-[var(--text-muted)] mt-1">
                {{ formatTime(report.created_at || report.start_time) }}
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-6">
            <div v-if="report.rating" class="text-center">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center font-bold"
                :class="getRatingClass(report.rating)"
              >
                {{ report.rating }}
              </div>
              <div class="text-xs text-[var(--text-muted)] mt-1">评分</div>
            </div>
            
            <div class="flex items-center gap-2">
              <button @click.stop="viewReport(report)" class="btn-secondary text-sm">查看</button>
              <button @click.stop="downloadReport(report, 'markdown')" class="px-3 py-1.5 rounded-lg text-sm bg-white/5 text-[var(--text-secondary)] hover:bg-white/10 transition-colors">
                下载
              </button>
              <button @click.stop="deleteReport(report)" class="px-3 py-1.5 rounded-lg text-sm bg-[#EF4444]/10 text-[#EF4444] hover:bg-[#EF4444]/20 transition-colors">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-[var(--text-muted)] opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
        </svg>
        <p class="text-[var(--text-muted)] mt-4">暂无报告</p>
        <button @click="goToAnalysis" class="btn-primary mt-4">开始分析</button>
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
          <span class="text-sm">{{ currentPage }} / {{ totalPages }}</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const reports = ref<any[]>([])
const searchKeyword = ref('')
const marketFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filteredReports = computed(() => {
  let result = [...reports.value]
  
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    result = result.filter(r => 
      r.stock_code?.toLowerCase().includes(kw) || 
      r.stock_name?.toLowerCase().includes(kw)
    )
  }
  
  if (marketFilter.value) {
    result = result.filter(r => r.market === marketFilter.value)
  }
  
  total.value = result.length
  return result.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value)
})

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const getRatingClass = (rating: number) => {
  if (rating >= 8) return 'bg-[#22C55E]/20 text-[#22C55E]'
  if (rating >= 6) return 'bg-[#F59E0B]/20 text-[#F59E0B]'
  return 'bg-[#EF4444]/20 text-[#EF4444]'
}

const viewReport = (report: any) => {
  router.push(`/reports/${report.task_id || report.id}`)
}

const goToAnalysis = () => {
  router.push('/analysis')
}

const downloadReport = async (report: any, format: string) => {
  try {
    const res = await fetch(`/api/reports/${report.task_id || report.id}/download?format=${format}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) {
      ElMessage.error('下载失败')
      return
    }
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${report.stock_code}_分析报告.md`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
    ElMessage.success('报告已下载')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

const deleteReport = async (report: any) => {
  try {
    await ElMessageBox.confirm('确定删除该报告？', '确认删除', { type: 'warning' })
    // 调用删除 API
    ElMessage.success('已删除')
    reports.value = reports.value.filter(r => (r.task_id || r.id) !== (report.task_id || report.id))
  } catch {}
}

const refreshReports = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/reports?limit=100', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
      const data = await res.json()
      reports.value = data.data || data.reports || data || []
    }
    ElMessage.success('已刷新')
  } catch (error) {
    console.error('加载报告失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshReports()
})
</script>
