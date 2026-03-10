<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        分析历史
      </h1>
      <p class="text-[var(--text-secondary)] mt-1">查看历史分析记录和结果</p>
    </div>

    <!-- 筛选条件 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-4 mb-6">
      <div class="flex flex-wrap items-end gap-4">
        <div>
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">时间范围</label>
          <input type="date" v-model="filterForm.startDate" class="px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
        </div>
        <div>
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">至</label>
          <input type="date" v-model="filterForm.endDate" class="px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
        </div>
        <div>
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">市场类型</label>
          <select v-model="filterForm.marketType" class="px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option value="">全部市场</option>
            <option value="美股">美股</option>
            <option value="A股">A股</option>
            <option value="港股">港股</option>
          </select>
        </div>
        <div>
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">分析类型</label>
          <select v-model="filterForm.analysisType" class="px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
            <option value="">全部类型</option>
            <option value="basic">基础分析</option>
            <option value="deep">深度分析</option>
            <option value="technical">技术分析</option>
            <option value="comprehensive">综合分析</option>
          </select>
        </div>
        <div class="flex-1 min-w-[150px]">
          <label class="text-sm text-[var(--text-secondary)] block mb-1.5">股票代码</label>
          <input type="text" v-model="filterForm.stockSymbol" placeholder="输入股票代码" 
                 class="w-full px-3 py-2 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm"
                 @keyup.enter="loadAnalysisHistory">
        </div>
        <div class="flex gap-2">
          <button @click="loadAnalysisHistory" :disabled="loading" 
                  class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            查询
          </button>
          <button @click="resetFilter" 
                  class="px-4 py-2 bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
            重置
          </button>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#22C55E]">{{ stats.totalAnalyses }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">总分析数</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#F59E0B]">{{ stats.favoriteCount }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">收藏数量</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#3B82F6]">{{ stats.todayCount }}</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">今日分析</div>
      </div>
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 text-center">
        <div class="text-2xl font-bold text-[#8B5CF6]">{{ stats.successRate }}%</div>
        <div class="text-sm text-[var(--text-secondary)] mt-1">成功率</div>
      </div>
    </div>

    <!-- 分析列表 -->
    <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5">
      <div v-if="loading" class="flex items-center justify-center py-8">
        <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>

      <div v-else-if="analysisList.length === 0" class="text-center py-12 text-[var(--text-secondary)]">
        暂无分析记录
      </div>

      <div v-else class="space-y-4">
        <div v-for="item in analysisList" :key="item.id" 
             class="p-4 bg-[var(--bg-tertiary)] rounded-lg hover:bg-[var(--bg-hover)] transition-colors cursor-pointer"
             @click="viewDetail(item)">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <span class="font-bold text-lg">{{ item.stock_symbol }}</span>
                <span class="text-[var(--text-secondary)]">{{ item.stock_name }}</span>
                <span :class="getMarketClass(item.market)" class="px-2 py-0.5 rounded text-xs">
                  {{ item.market }}
                </span>
                <span :class="getAnalysisTypeClass(item.analysis_type)" class="px-2 py-0.5 rounded text-xs">
                  {{ getAnalysisTypeName(item.analysis_type) }}
                </span>
              </div>
              <p class="text-sm text-[var(--text-secondary)] line-clamp-2">{{ item.summary }}</p>
              <div class="flex items-center gap-4 mt-2 text-xs text-[var(--text-secondary)]">
                <span>{{ formatDateTime(item.created_at) }}</span>
                <span v-if="item.tags?.length">
                  <span v-for="tag in item.tags.slice(0, 3)" :key="tag" class="mr-1">#{{ tag }}</span>
                </span>
              </div>
            </div>
            <div class="flex items-center gap-2 ml-4">
              <button @click.stop="toggleFavorite(item)" class="p-2 hover:bg-[var(--bg-secondary)] rounded transition-colors">
                <svg :class="item.is_favorite ? 'text-[#F59E0B] fill-current' : ''" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                </svg>
              </button>
              <button @click.stop="deleteAnalysis(item)" class="p-2 hover:bg-[var(--bg-secondary)] rounded transition-colors text-[#EF4444]">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="analysisList.length > 0" class="flex items-center justify-between mt-4 pt-4 border-t border-[var(--border-color)]">
        <div class="text-sm text-[var(--text-secondary)]">共 {{ totalItems }} 条记录</div>
        <div class="flex items-center gap-2">
          <button v-for="p in Math.min(5, Math.ceil(totalItems / pageSize))" :key="p"
                  @click="currentPage = p; loadAnalysisHistory()"
                  :class="currentPage === p ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)]'"
                  class="w-8 h-8 rounded-lg text-sm transition-colors">
            {{ p }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { analysisApi } from '@/api/analysis'

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const totalItems = ref(0)

const filterForm = reactive({
  startDate: '',
  endDate: '',
  marketType: '',
  analysisType: '',
  stockSymbol: ''
})

const stats = reactive({
  totalAnalyses: 0,
  favoriteCount: 0,
  todayCount: 0,
  successRate: 0
})

const analysisList = ref<any[]>([])

const formatDateTime = (date: string) => new Date(date).toLocaleString('zh-CN')

const getMarketClass = (market: string): string => {
  const classMap: Record<string, string> = {
    '美股': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'A股': 'bg-[#EF4444]/20 text-[#EF4444]',
    '港股': 'bg-[#F59E0B]/20 text-[#F59E0B]'
  }
  return classMap[market] || 'bg-[var(--bg-secondary)] text-[var(--text-secondary)]'
}

const getAnalysisTypeClass = (type: string): string => {
  const classMap: Record<string, string> = {
    'basic': 'bg-[#22C55E]/20 text-[#22C55E]',
    'deep': 'bg-[#8B5CF6]/20 text-[#8B5CF6]',
    'technical': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'comprehensive': 'bg-[#F59E0B]/20 text-[#F59E0B]'
  }
  return classMap[type] || 'bg-[var(--bg-secondary)] text-[var(--text-secondary)]'
}

const getAnalysisTypeName = (type: string): string => {
  const nameMap: Record<string, string> = {
    'basic': '基础分析',
    'deep': '深度分析',
    'technical': '技术分析',
    'comprehensive': '综合分析'
  }
  return nameMap[type] || type
}

const loadAnalysisHistory = async () => {
  loading.value = true
  try {
    const res = await analysisApi.getHistory({
      page: currentPage.value,
      page_size: pageSize.value,
      ...filterForm
    })
    analysisList.value = res.data?.items || []
    totalItems.value = res.data?.total || 0
  } catch (error) {
    console.error('加载分析历史失败:', error)
    ElMessage.error('加载分析历史失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const res = await analysisApi.getStats()
    Object.assign(stats, res.data || {})
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const resetFilter = () => {
  Object.assign(filterForm, { startDate: '', endDate: '', marketType: '', analysisType: '', stockSymbol: '' })
  loadAnalysisHistory()
}

const viewDetail = (item: any) => {
  // 跳转到详情页
  window.location.href = `/reports/${item.id}`
}

const toggleFavorite = async (item: any) => {
  try {
    await analysisApi.toggleFavorite(item.id)
    item.is_favorite = !item.is_favorite
    ElMessage.success(item.is_favorite ? '已收藏' : '已取消收藏')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteAnalysis = async (item: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除 ${item.stock_symbol} 的分析记录吗？`, '确认删除', { type: 'warning' })
    await analysisApi.delete(item.id)
    ElMessage.success('已删除')
    loadAnalysisHistory()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadAnalysisHistory()
  loadStats()
})
</script>
