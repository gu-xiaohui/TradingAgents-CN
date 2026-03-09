<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-[#22C55E]/20 via-[#8B5CF6]/10 to-[#22C55E]/20" />
      <div class="absolute top-20 left-20 w-72 h-72 bg-[#22C55E]/30 rounded-full blur-3xl" />
      <div class="absolute bottom-20 right-20 w-96 h-96 bg-[#8B5CF6]/20 rounded-full blur-3xl" />
      
      <div class="relative max-w-6xl mx-auto px-6 py-20">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
            <svg class="w-9 h-9 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div>
            <h1 class="text-4xl font-bold flex items-center gap-3">
              TradingAgents-CN
              <span class="text-sm font-normal px-3 py-1 rounded-full bg-white/10 text-[var(--text-secondary)]">v1.0.0-preview</span>
            </h1>
          </div>
        </div>
        
        <p class="text-xl text-[var(--text-secondary)] mb-4">现代化的多智能体股票分析学习平台</p>
        <p class="text-[var(--text-muted)] max-w-2xl mb-6">
          基于先进的 AI 技术，为投资者提供专业、准确、及时的股票分析服务。
          采用多智能体协作模式，从不同角度对股票进行全方位分析，助您做出更明智的投资决策。
        </p>
        
        <div class="flex items-center gap-2 text-sm text-[var(--text-muted)] mb-8">
          <svg class="w-4 h-4 text-[#F59E0B]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
          <span>基于 <a href="https://github.com/TauricResearch/TradingAgents" target="_blank" class="text-[#22C55E] hover:underline">TradingAgents</a> 项目开发，感谢原项目的贡献</span>
        </div>
        
        <div class="flex items-center gap-4">
          <button @click="goToAnalysis" class="btn-primary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            开始分析
          </button>
          <button @click="viewDocumentation" class="btn-secondary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            查看文档
          </button>
        </div>
        
        <!-- Stats -->
        <div class="flex items-center gap-12 mt-12 pt-8 border-t border-white/10">
          <div class="text-center">
            <div class="text-3xl font-bold text-[#22C55E]">12</div>
            <div class="text-sm text-[var(--text-muted)]">智能体</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-[#8B5CF6]">12+</div>
            <div class="text-sm text-[var(--text-muted)]">数据源</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-[#3B82F6]">24/7</div>
            <div class="text-sm text-[var(--text-muted)]">实时监控</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 核心功能 -->
    <div class="max-w-6xl mx-auto px-6 py-16">
      <div class="text-center mb-12">
        <h2 class="text-2xl font-bold mb-2">核心功能</h2>
        <p class="text-[var(--text-muted)]">强大的 AI 驱动分析能力，全方位投资决策支持</p>
      </div>
      
      <div class="grid grid-cols-3 gap-6">
        <div class="card p-6">
          <div class="w-12 h-12 rounded-xl bg-[#22C55E]/20 flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">多智能体分析</h3>
          <p class="text-sm text-[var(--text-muted)] mb-4">基本面、技术面、新闻分析等 12 个智能体协作，提供全方位的股票分析视角</p>
          <div class="flex flex-wrap gap-2">
            <span class="badge-info">基本面分析</span>
            <span class="badge-success">技术分析</span>
            <span class="badge-warning">新闻分析</span>
          </div>
        </div>
        
        <div class="card p-6">
          <div class="w-12 h-12 rounded-xl bg-[#8B5CF6]/20 flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-[#8B5CF6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">多数据源支持</h3>
          <p class="text-sm text-[var(--text-muted)] mb-4">支持 Tushare、AKShare、BaoStock 等多个数据源，确保数据的全面性和准确性</p>
          <div class="flex flex-wrap gap-2">
            <span class="badge-info">Tushare</span>
            <span class="badge-success">AKShare</span>
            <span class="badge-warning">BaoStock</span>
          </div>
        </div>
        
        <div class="card p-6">
          <div class="w-12 h-12 rounded-xl bg-[#3B82F6]/20 flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-[#3B82F6]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">多模型支持</h3>
          <p class="text-sm text-[var(--text-muted)] mb-4">支持 OpenAI、Claude、Qwen 等多种大语言模型，灵活选择最适合的分析引擎</p>
          <div class="flex flex-wrap gap-2">
            <span class="badge-info">GPT-4</span>
            <span class="badge-success">Claude</span>
            <span class="badge-warning">Qwen</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 技术栈 -->
    <div class="max-w-6xl mx-auto px-6 py-16 border-t border-white/10">
      <div class="text-center mb-12">
        <h2 class="text-2xl font-bold mb-2">技术栈</h2>
        <p class="text-[var(--text-muted)]">基于现代化技术构建的可靠系统</p>
      </div>
      
      <div class="grid grid-cols-4 gap-4">
        <div class="card p-4 text-center">
          <div class="text-2xl mb-2">🐍</div>
          <div class="font-medium text-sm">Python 3.10+</div>
          <div class="text-xs text-[var(--text-muted)]">后端语言</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl mb-2">⚡</div>
          <div class="font-medium text-sm">FastAPI</div>
          <div class="text-xs text-[var(--text-muted)]">Web 框架</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl mb-2">💚</div>
          <div class="font-medium text-sm">Vue 3</div>
          <div class="text-xs text-[var(--text-muted)]">前端框架</div>
        </div>
        <div class="card p-4 text-center">
          <div class="text-2xl mb-2">🎨</div>
          <div class="font-medium text-sm">Tailwind CSS</div>
          <div class="text-xs text-[var(--text-muted)]">样式框架</div>
        </div>
      </div>
    </div>

    <!-- 链接 -->
    <div class="max-w-6xl mx-auto px-6 py-16 border-t border-white/10">
      <div class="text-center mb-12">
        <h2 class="text-2xl font-bold mb-2">相关链接</h2>
        <p class="text-[var(--text-muted)]">了解更多或参与项目</p>
      </div>
      
      <div class="flex justify-center gap-4">
        <a href="https://github.com/TauricResearch/TradingAgents" target="_blank" class="card p-4 flex items-center gap-3 hover:border-[#22C55E]/50 transition-colors">
          <svg class="w-6 h-6 text-[var(--text-primary)]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <div>
            <div class="font-medium text-sm text-[var(--text-primary)]">GitHub</div>
            <div class="text-xs text-[var(--text-muted)]">查看源码</div>
          </div>
        </a>
        
        <a href="https://docs.openclaw.ai" target="_blank" class="card p-4 flex items-center gap-3 hover:border-[#22C55E]/50 transition-colors">
          <svg class="w-6 h-6 text-[var(--text-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <div>
            <div class="font-medium text-sm text-[var(--text-primary)]">文档</div>
            <div class="text-xs text-[var(--text-muted)]">使用指南</div>
          </div>
        </a>
        
        <a href="https://discord.com/invite/clawd" target="_blank" class="card p-4 flex items-center gap-3 hover:border-[#22C55E]/50 transition-colors">
          <svg class="w-6 h-6 text-[#5865F2]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/>
          </svg>
          <div>
            <div class="font-medium text-sm text-[var(--text-primary)]">Discord</div>
            <div class="text-xs text-[var(--text-muted)]">加入社区</div>
          </div>
        </a>
      </div>
    </div>

    <!-- Footer -->
    <div class="border-t border-white/10 py-8">
      <div class="max-w-6xl mx-auto px-6 text-center text-sm text-[var(--text-muted)]">
        <p>TradingAgents-CN v1.0.0-preview · Made with AI</p>
        <p class="mt-2">基于 <a href="https://github.com/TauricResearch/TradingAgents" target="_blank" class="text-[#22C55E] hover:underline">TradingAgents</a> 项目开发</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToAnalysis = () => {
  router.push('/new/analysis')
}

const viewDocumentation = () => {
  router.push('/new/learning')
}
</script>
