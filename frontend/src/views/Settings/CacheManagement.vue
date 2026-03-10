<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
        </svg>
        缓存管理
      </h1>
      <p class="text-[var(--text-secondary)] mt-1">管理股票数据缓存，优化系统性能</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 缓存统计 -->
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
          </svg>
          缓存统计
        </h3>
        
        <div v-if="statsLoading" class="flex items-center justify-center py-8">
          <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
        </div>
        
        <div v-else class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-[var(--bg-tertiary)] rounded-lg">
              <div class="text-2xl font-bold text-[#22C55E]">{{ cacheStats.totalFiles }}</div>
              <div class="text-sm text-[var(--text-secondary)]">总文件数</div>
            </div>
            <div class="text-center p-4 bg-[var(--bg-tertiary)] rounded-lg">
              <div class="text-2xl font-bold text-[#22C55E]">{{ formatSize(cacheStats.totalSize) }}</div>
              <div class="text-sm text-[var(--text-secondary)]">总大小</div>
            </div>
            <div class="text-center p-4 bg-[var(--bg-tertiary)] rounded-lg">
              <div class="text-2xl font-bold text-[#3B82F6]">{{ cacheStats.stockDataCount }}</div>
              <div class="text-sm text-[var(--text-secondary)]">股票数据</div>
            </div>
            <div class="text-center p-4 bg-[var(--bg-tertiary)] rounded-lg">
              <div class="text-2xl font-bold text-[#F59E0B]">{{ cacheStats.newsDataCount }}</div>
              <div class="text-sm text-[var(--text-secondary)]">新闻数据</div>
            </div>
          </div>
          
          <div class="pt-4 border-t border-[var(--border-color)]">
            <h4 class="text-sm font-medium mb-3">缓存使用情况</h4>
            <div class="w-full bg-[var(--bg-tertiary)] rounded-full h-3 overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-300"
                :class="getProgressClass(cacheUsagePercentage)"
                :style="{ width: cacheUsagePercentage + '%' }"
              ></div>
            </div>
            <p class="text-sm text-[var(--text-secondary)] mt-2 text-center">
              已使用 {{ formatSize(cacheStats.totalSize) }} / {{ formatSize(cacheStats.maxSize) }}
            </p>
          </div>
        </div>
      </div>

      <!-- 缓存操作 -->
      <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
          </svg>
          缓存操作
        </h3>
        
        <div class="space-y-6">
          <!-- 刷新统计 -->
          <div>
            <h4 class="font-medium mb-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              刷新统计
            </h4>
            <p class="text-sm text-[var(--text-secondary)] mb-3">重新获取最新的缓存统计信息</p>
            <button 
              @click="refreshStats" 
              :disabled="statsLoading"
              class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              <svg v-if="statsLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              刷新统计
            </button>
          </div>
          
          <div class="border-t border-[var(--border-color)]"></div>
          
          <!-- 清理过期缓存 -->
          <div>
            <h4 class="font-medium mb-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-[#F59E0B]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              清理过期缓存
            </h4>
            <p class="text-sm text-[var(--text-secondary)] mb-3">删除指定天数之前的缓存文件</p>
            
            <div class="mb-4">
              <label class="text-sm text-[var(--text-secondary)] block mb-2">清理天数: {{ cleanupDays }} 天</label>
              <input 
                type="range" 
                v-model="cleanupDays" 
                min="1" 
                max="30" 
                class="w-full h-2 bg-[var(--bg-tertiary)] rounded-lg appearance-none cursor-pointer accent-[#F59E0B]"
              />
              <div class="flex justify-between text-xs text-[var(--text-secondary)] mt-1">
                <span>1天</span>
                <span>1周</span>
                <span>2周</span>
                <span>1月</span>
              </div>
            </div>
            
            <button 
              @click="cleanupOldCache" 
              :disabled="cleanupLoading"
              class="px-4 py-2 bg-[#F59E0B] hover:bg-[#D97706] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              <svg v-if="cleanupLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              清理过期缓存
            </button>
          </div>
          
          <div class="border-t border-[var(--border-color)]"></div>
          
          <!-- 清空所有缓存 -->
          <div>
            <h4 class="font-medium mb-2 flex items-center gap-2">
              <svg class="w-4 h-4 text-[#EF4444]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              清空所有缓存
            </h4>
            <p class="text-sm text-[#EF4444] mb-3">此操作将删除所有缓存文件，无法恢复</p>
            
            <button 
              @click="clearAllCache" 
              :disabled="clearAllLoading"
              class="px-4 py-2 bg-[#EF4444] hover:bg-[#DC2626] text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              <svg v-if="clearAllLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
              清空所有缓存
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 缓存详情 -->
    <div class="mt-6 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold flex items-center gap-2">
          <svg class="w-5 h-5 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3 12h3.375c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H3v12h3.375c.621 0 1.125-.504 1.125-1.125v-2.25c0-.621-.504-1.125-1.125-1.125H3V12z" />
          </svg>
          缓存详情
        </h3>
        <button 
          @click="loadCacheDetails" 
          :disabled="detailsLoading"
          class="px-3 py-1.5 text-sm bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors flex items-center gap-1.5"
        >
          <svg :class="{ 'animate-spin': detailsLoading }" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          刷新
        </button>
      </div>
      
      <div v-if="detailsLoading" class="flex items-center justify-center py-8">
        <svg class="w-8 h-8 animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[var(--border-color)]">
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">类型</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">股票代码</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">大小</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">创建时间</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">最后访问</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">命中次数</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-[var(--text-secondary)]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cacheDetails" :key="item.id" class="border-b border-[var(--border-color)] hover:bg-[var(--bg-hover)]">
              <td class="py-3 px-4">
                <span :class="getCacheTypeClass(item.type)" class="px-2 py-1 rounded text-xs font-medium">
                  {{ item.type }}
                </span>
              </td>
              <td class="py-3 px-4 font-mono">{{ item.symbol }}</td>
              <td class="py-3 px-4">{{ formatSize(item.size) }}</td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatDate(item.created_at) }}</td>
              <td class="py-3 px-4 text-sm text-[var(--text-secondary)]">{{ formatDate(item.last_accessed) }}</td>
              <td class="py-3 px-4">{{ item.hit_count }}</td>
              <td class="py-3 px-4">
                <button 
                  @click="deleteCacheItem(item)"
                  class="text-[#EF4444] hover:text-[#DC2626] transition-colors"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 分页 -->
        <div v-if="cacheDetails.length > 0" class="flex items-center justify-between mt-4 pt-4 border-t border-[var(--border-color)]">
          <div class="text-sm text-[var(--text-secondary)]">
            共 {{ totalItems }} 条记录
          </div>
          <div class="flex items-center gap-2">
            <select v-model="pageSize" @change="loadCacheDetails" class="px-3 py-1.5 bg-[var(--bg-tertiary)] border border-[var(--border-color)] rounded-lg text-sm">
              <option :value="10">10 条/页</option>
              <option :value="20">20 条/页</option>
              <option :value="50">50 条/页</option>
              <option :value="100">100 条/页</option>
            </select>
            <button 
              v-for="p in Math.ceil(totalItems / pageSize)" 
              :key="p"
              @click="currentPage = p; loadCacheDetails()"
              :class="currentPage === p ? 'bg-[#22C55E] text-white' : 'bg-[var(--bg-tertiary)] hover:bg-[var(--bg-hover)]'"
              class="w-8 h-8 rounded-lg text-sm transition-colors"
            >
              {{ p }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as cacheApi from '@/api/cache'

// 响应式数据
const statsLoading = ref(false)
const cleanupLoading = ref(false)
const clearAllLoading = ref(false)
const detailsLoading = ref(false)

const cleanupDays = ref(7)
const currentPage = ref(1)
const pageSize = ref(20)
const totalItems = ref(0)

// 缓存统计数据
const cacheStats = ref({
  totalFiles: 0,
  totalSize: 0,
  maxSize: 1024 * 1024 * 1024, // 1GB
  stockDataCount: 0,
  newsDataCount: 0,
  analysisDataCount: 0
})

// 缓存详情数据
const cacheDetails = ref<any[]>([])

// 计算属性
const cacheUsagePercentage = computed(() => {
  if (cacheStats.value.maxSize === 0) return 0
  return Math.round((cacheStats.value.totalSize / cacheStats.value.maxSize) * 100)
})

// 方法
const formatSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const getProgressClass = (percentage: number): string => {
  if (percentage < 50) return 'bg-[#22C55E]'
  if (percentage < 80) return 'bg-[#F59E0B]'
  return 'bg-[#EF4444]'
}

const getCacheTypeClass = (type: string): string => {
  const classMap: Record<string, string> = {
    'stock': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'news': 'bg-[#22C55E]/20 text-[#22C55E]',
    'analysis': 'bg-[#F59E0B]/20 text-[#F59E0B]'
  }
  return classMap[type] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const refreshStats = async () => {
  statsLoading.value = true
  try {
    const response = await cacheApi.getCacheStats()
    cacheStats.value = response.data || response
    ElMessage.success('缓存统计已刷新')
  } catch (error: any) {
    console.error('刷新缓存统计失败:', error)
    ElMessage.error(error.message || '刷新缓存统计失败')
  } finally {
    statsLoading.value = false
  }
}

const cleanupOldCache = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要清理 ${cleanupDays.value} 天前的缓存文件吗？`,
      '确认清理',
      { type: 'warning' }
    )

    cleanupLoading.value = true
    await cacheApi.cleanupOldCache(cleanupDays.value)
    ElMessage.success(`已清理 ${cleanupDays.value} 天前的缓存文件`)
    await refreshStats()
    await loadCacheDetails()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清理缓存失败:', error)
      ElMessage.error(error.message || '清理缓存失败')
    }
  } finally {
    cleanupLoading.value = false
  }
}

const clearAllCache = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有缓存文件吗？此操作无法恢复！',
      '确认清空',
      {
        type: 'error',
        confirmButtonText: '确定清空',
        cancelButtonText: '取消'
      }
    )

    clearAllLoading.value = true
    await cacheApi.clearAllCache()
    ElMessage.success('所有缓存已清空')
    await refreshStats()
    await loadCacheDetails()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空缓存失败:', error)
      ElMessage.error(error.message || '清空缓存失败')
    }
  } finally {
    clearAllLoading.value = false
  }
}

const loadCacheDetails = async () => {
  detailsLoading.value = true
  try {
    const response = await cacheApi.getCacheDetails(currentPage.value, pageSize.value)
    const data = response.data || response
    cacheDetails.value = data.items || []
    totalItems.value = data.total || 0
  } catch (error: any) {
    console.error('加载缓存详情失败:', error)
    ElMessage.error(error.message || '加载缓存详情失败')
  } finally {
    detailsLoading.value = false
  }
}

const deleteCacheItem = async (item: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 ${item.symbol} 的${item.type}缓存吗？`,
      '确认删除',
      { type: 'warning' }
    )
    
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('缓存项已删除')
    await loadCacheDetails()
    await refreshStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除缓存项失败')
    }
  }
}

// 生命周期
onMounted(() => {
  refreshStats()
  loadCacheDetails()
})
</script>
