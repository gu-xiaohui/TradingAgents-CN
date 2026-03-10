<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" transform="translate(4, 4) scale(0.6)" />
          </svg>
        </div>
        批量分析
      </h1>
      <p class="text-[var(--text-muted)] mt-1 ml-13">AI 驱动的批量股票分析，高效处理多只股票</p>
    </div>

    <!-- 风险提示 -->
    <div class="p-4 rounded-xl bg-[#F59E0B]/10 border border-[#F59E0B]/20 mb-6">
      <div class="flex gap-3">
        <svg class="w-5 h-5 text-[#F59E0B] flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
        </svg>
        <div class="text-sm">
          <p class="font-medium text-[#F59E0B]">⚠️ 重要提示</p>
          <p class="text-[var(--text-secondary)]">本工具为股票分析辅助工具，所有分析结果仅供参考，不构成投资建议。投资有风险，决策需谨慎。</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：股票输入 -->
      <div class="col-span-6">
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold">股票列表</h2>
            <span class="badge-info">{{ stockCodes.length }} 只股票</span>
          </div>

          <textarea
            v-model="stockInput"
            rows="12"
            placeholder="请输入股票代码，每行一个&#10;支持格式：&#10;000001&#10;000002.SZ&#10;600036.SH&#10;AAPL"
            class="input mb-4 font-mono text-sm"
          />

          <div class="flex gap-3">
            <button @click="parseStockCodes" class="btn-secondary text-sm">解析股票代码</button>
            <button @click="clearStocks" class="btn-secondary text-sm">清空</button>
          </div>

          <!-- 股票预览 -->
          <div v-if="stockCodes.length > 0" class="mt-4 pt-4 border-t border-white/10">
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-3">股票预览</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(code, index) in stockCodes.slice(0, 30)"
                :key="code"
                class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white/5 text-sm"
              >
                {{ code }}
                <button @click="removeStock(index)" class="text-[var(--text-muted)] hover:text-[#EF4444]">
                  <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
              <span v-if="stockCodes.length > 30" class="px-2 py-1 text-sm text-[var(--text-muted)]">
                +{{ stockCodes.length - 30 }} 更多...
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：分析配置 -->
      <div class="col-span-6">
        <div class="card">
          <h2 class="text-lg font-semibold mb-6">分析配置</h2>

          <div class="space-y-6">
            <!-- 分析深度 -->
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-3">分析深度</label>
              <div class="grid grid-cols-5 gap-2">
                <button
                  v-for="i in 5"
                  :key="i"
                  @click="config.depth = i"
                  class="p-3 rounded-xl border-2 transition-all text-center"
                  :class="config.depth === i 
                    ? 'border-[#22C55E] bg-[#22C55E]/10 text-[#22C55E]' 
                    : 'border-white/10 bg-white/5 text-[var(--text-secondary)] hover:border-white/20'"
                >
                  <div class="text-sm font-medium">{{ i }}级</div>
                </button>
              </div>
            </div>

            <!-- 市场类型 -->
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">市场类型</label>
              <select v-model="config.market" class="input">
                <option value="A股">🇨🇳 A股市场</option>
                <option value="美股">🇺🇸 美股市场</option>
                <option value="港股">🇭🇰 港股市场</option>
              </select>
            </div>

            <!-- 分析师选择 -->
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-3">分析师团队</label>
              <div class="space-y-2">
                <label
                  v-for="analyst in analysts"
                  :key="analyst.id"
                  class="flex items-center gap-3 p-3 rounded-xl border-2 cursor-pointer transition-colors"
                  :class="config.analysts.includes(analyst.id)
                    ? 'border-[#22C55E] bg-[#22C55E]/10'
                    : 'border-white/10 bg-white/5 hover:border-white/20'"
                >
                  <input
                    type="checkbox"
                    :checked="config.analysts.includes(analyst.id)"
                    @change="toggleAnalyst(analyst.id)"
                    class="hidden"
                  />
                  <div class="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" :d="analyst.icon" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="text-sm font-medium">{{ analyst.name }}</div>
                    <div class="text-xs text-[var(--text-muted)]">{{ analyst.desc }}</div>
                  </div>
                  <svg v-if="config.analysts.includes(analyst.id)" class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </label>
              </div>
            </div>

            <!-- 提交按钮 -->
            <button
              @click="submitBatch"
              :disabled="stockCodes.length === 0 || submitting"
              class="btn-primary w-full py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="submitting" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
              </svg>
              {{ submitting ? '提交中...' : `开始批量分析 (${stockCodes.length}只)` }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { analysisApi } from '@/api/analysis'

const router = useRouter()
const authStore = useAuthStore()

const stockInput = ref('')
const stockCodes = ref<string[]>([])
const submitting = ref(false)

const config = reactive({
  depth: 3,
  market: 'A股',
  analysts: ['market', 'fundamental']
})

const analysts = [
  { id: 'market', name: '市场分析师', desc: '技术指标分析', icon: 'M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z' },
  { id: 'fundamental', name: '基本面分析师', desc: '财务数据分析', icon: 'M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75-.75H5.25A.75.75 0 0 0 4.5 18v.75c0 .414.336.75.75.75h.75m-1.5-1.5h14.5' },
  { id: 'news', name: '新闻分析师', desc: '新闻事件分析', icon: 'M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z' },
  { id: 'sentiment', name: '情绪分析师', desc: '市场情绪分析', icon: 'M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z' },
]

const parseStockCodes = () => {
  const lines = stockInput.value.split('\n')
  stockCodes.value = lines
    .map(line => line.trim())
    .filter(line => line.length > 0)
    .map(code => {
      // 标准化股票代码
      return code.toUpperCase()
    })
}

const clearStocks = () => {
  stockInput.value = ''
  stockCodes.value = []
}

const removeStock = (index: number) => {
  stockCodes.value.splice(index, 1)
}

const toggleAnalyst = (id: string) => {
  const index = config.analysts.indexOf(id)
  if (index > -1) {
    config.analysts.splice(index, 1)
  } else {
    config.analysts.push(id)
  }
}

const submitBatch = async () => {
  if (stockCodes.value.length === 0) {
    ElMessage.warning('请输入至少一只股票代码')
    return
  }

  submitting.value = true

  try {
    // 调用批量分析 API
    const response = await analysisApi.startBatchAnalysis({
      symbols: stockCodes.value,
      parameters: {
        market_type: config.market,
        research_depth: String(config.depth),
        selected_analysts: config.analysts
      }
    })

    if (response.success) {
      ElMessage.success(`已提交 ${stockCodes.value.length} 只股票的批量分析任务`)
      router.push('/tasks')
    } else {
      ElMessage.error(response.message || '提交失败')
    }
  } catch (error: any) {
    console.error('批量分析失败:', error)
    ElMessage.error(error.message || '提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}
</script>
