<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        单股分析
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">AI 驱动的智能股票分析，多维度评估投资价值与风险</p>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧：主表单 -->
      <div class="col-span-8">
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold">分析配置</h2>
            <span class="badge-info">必填信息</span>
          </div>

          <!-- 股票信息 -->
          <div class="mb-8">
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-4 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              股票信息
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm text-[var(--text-secondary)] mb-2">股票代码 <span class="text-[#EF4444]">*</span></label>
                <input
                  v-model="form.stockCode"
                  type="text"
                  placeholder="如：000001、AAPL、0700"
                  class="input"
                />
              </div>
              <div>
                <label class="block text-sm text-[var(--text-secondary)] mb-2">市场类型</label>
                <select v-model="form.market" class="input">
                  <option value="A股">🇨🇳 A股市场</option>
                  <option value="美股">🇺🇸 美股市场</option>
                  <option value="港股">🇭🇰 港股市场</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 分析深度 -->
          <div class="mb-8">
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-4 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              分析深度
            </h3>
            <div class="grid grid-cols-5 gap-3">
              <button
                v-for="(depth, index) in depthOptions"
                :key="index"
                @click="form.researchDepth = index + 1"
                class="p-3 rounded-xl border-2 transition-all text-center"
                :class="form.researchDepth === index + 1 
                  ? 'border-[#22C55E] bg-[#22C55E]/10 text-[#22C55E]' 
                  : 'border-white/10 bg-white/5 text-[var(--text-secondary)] hover:border-white/20'"
              >
                <!-- 闪电图标 - 快速 -->
                <svg v-if="depth.icon === 'bolt'" class="w-6 h-6 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <!-- 图表图标 - 基础 -->
                <svg v-else-if="depth.icon === 'chart'" class="w-6 h-6 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <!-- 靶心图标 - 标准 -->
                <svg v-else-if="depth.icon === 'target'" class="w-6 h-6 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                <!-- 搜索图标 - 深度 -->
                <svg v-else-if="depth.icon === 'search'" class="w-6 h-6 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <!-- 星星图标 - 全面 -->
                <svg v-else-if="depth.icon === 'star'" class="w-6 h-6 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                </svg>
                <div class="text-xs font-medium">{{ depth.name }}</div>
                <div class="text-xs opacity-70 mt-1">{{ depth.time }}</div>
              </button>
            </div>
          </div>

          <!-- 分析师团队 -->
          <div class="mb-8">
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-4 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              分析师团队
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="analyst in analysts"
                :key="analyst.id"
                @click="toggleAnalyst(analyst.name)"
                class="flex items-center gap-3 p-3 rounded-xl border-2 transition-all"
                :class="form.selectedAnalysts.includes(analyst.name)
                  ? 'border-[#22C55E] bg-[#22C55E]/10'
                  : 'border-white/10 bg-white/5 hover:border-white/20'"
              >
                <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#22C55E]/20 to-[#8B5CF6]/20 flex items-center justify-center text-[#22C55E]">
                  <!-- 图表图标 - 市场分析师 -->
                  <svg v-if="analyst.icon === 'chart'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <!-- 货币图标 - 基本面分析师 -->
                  <svg v-else-if="analyst.icon === 'currency'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <!-- 新闻图标 - 新闻分析师 -->
                  <svg v-else-if="analyst.icon === 'news'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                  </svg>
                  <!-- 表情图标 - 情绪分析师 -->
                  <svg v-else-if="analyst.icon === 'emoji'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="flex-1 text-left">
                  <div class="text-sm font-medium text-[var(--text-primary)]">{{ analyst.name }}</div>
                  <div class="text-xs text-[var(--text-muted)]">{{ analyst.desc }}</div>
                </div>
                <svg v-if="form.selectedAnalysts.includes(analyst.name)" class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-center">
            <button
              @click="submitAnalysis"
              :disabled="!form.stockCode.trim() || submitting"
              class="btn-primary px-8 py-4 text-lg font-semibold flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="submitting" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {{ submitting ? '提交中...' : '开始智能分析' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧：高级配置 -->
      <div class="col-span-4">
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold">高级配置</h2>
            <span class="badge-warning">可选</span>
          </div>

          <!-- AI 模型配置 -->
          <div class="mb-6">
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-3 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              AI 模型配置
            </h3>
            <div class="space-y-3">
              <div>
                <label class="block text-xs text-[var(--text-muted)] mb-1">快速分析模型</label>
                <select v-model="form.quickModel" class="input text-sm">
                  <option value="qwen-turbo">Qwen Turbo</option>
                  <option value="gpt-4o-mini">GPT-4o Mini</option>
                  <option value="claude-3-haiku">Claude 3 Haiku</option>
                </select>
              </div>
              <div>
                <label class="block text-xs text-[var(--text-muted)] mb-1">深度决策模型</label>
                <select v-model="form.deepModel" class="input text-sm">
                  <option value="qwen-max">Qwen Max</option>
                  <option value="gpt-4o">GPT-4o</option>
                  <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 分析选项 -->
          <div>
            <h3 class="text-sm font-medium text-[var(--text-secondary)] mb-3 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              分析选项
            </h3>
            <div class="space-y-3">
              <label class="flex items-center justify-between p-3 rounded-lg bg-white/5 cursor-pointer hover:bg-white/10">
                <span class="text-sm text-[var(--text-primary)]">情绪分析</span>
                <input type="checkbox" v-model="form.includeSentiment" class="w-4 h-4 accent-[#22C55E]" />
              </label>
              <label class="flex items-center justify-between p-3 rounded-lg bg-white/5 cursor-pointer hover:bg-white/10">
                <span class="text-sm text-[var(--text-primary)]">风险评估</span>
                <input type="checkbox" v-model="form.includeRisk" class="w-4 h-4 accent-[#22C55E]" />
              </label>
            </div>
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
import { analysisApi } from '@/api/analysis'

const router = useRouter()
const submitting = ref(false)

const form = reactive({
  stockCode: '',
  market: 'A股',
  researchDepth: 3,
  selectedAnalysts: ['市场分析师', '基本面分析师'],
  quickModel: 'qwen-turbo',
  deepModel: 'qwen-max',
  includeSentiment: true,
  includeRisk: true,
})

const depthOptions = [
  { name: '快速', time: '2-5分钟', icon: 'bolt' },
  { name: '基础', time: '3-6分钟', icon: 'chart' },
  { name: '标准', time: '4-8分钟', icon: 'target' },
  { name: '深度', time: '6-11分钟', icon: 'search' },
  { name: '全面', time: '8-16分钟', icon: 'star' }
]

const analysts = [
  { id: 1, name: '市场分析师', icon: 'chart', desc: '技术指标分析' },
  { id: 2, name: '基本面分析师', icon: 'currency', desc: '财务数据分析' },
  { id: 3, name: '新闻分析师', icon: 'news', desc: '新闻事件分析' },
  { id: 4, name: '情绪分析师', icon: 'emoji', desc: '市场情绪分析' },
]

const toggleAnalyst = (name: string) => {
  const index = form.selectedAnalysts.indexOf(name)
  if (index > -1) {
    form.selectedAnalysts.splice(index, 1)
  } else {
    form.selectedAnalysts.push(name)
  }
}

const submitAnalysis = async () => {
  if (!form.stockCode.trim()) {
    ElMessage.warning('请输入股票代码')
    return
  }
  if (form.selectedAnalysts.length === 0) {
    ElMessage.warning('请至少选择一个分析师')
    return
  }

  submitting.value = true
  
  try {
    // 调用真正的后端 API
    const response = await analysisApi.startSingleAnalysis({
      symbol: form.stockCode.trim(),
      parameters: {
        market_type: form.market,
        research_depth: String(form.researchDepth),
        selected_analysts: form.selectedAnalysts,
        include_sentiment: form.includeSentiment,
        include_risk: form.includeRisk,
        quick_analysis_model: form.quickModel,
        deep_analysis_model: form.deepModel,
      }
    })
    
    if (response.success) {
      ElMessage.success('分析任务已提交')
      // 跳转到任务中心
      router.push('/tasks')
    } else {
      ElMessage.error(response.message || '提交失败')
    }
  } catch (error: any) {
    console.error('提交分析失败:', error)
    ElMessage.error(error.message || '提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}
</script>
