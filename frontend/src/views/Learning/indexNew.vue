<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        学习中心
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">了解 AI、大模型和智能股票分析</p>
    </div>

    <!-- 分类卡片 -->
    <div class="grid grid-cols-4 gap-4">
      <div
        v-for="category in categories"
        :key="category.id"
        @click="navigateTo(category.id)"
        class="card p-6 cursor-pointer hover:border-[#22C55E]/50 transition-all group"
      >
        <div 
          class="w-14 h-14 rounded-xl mb-4 flex items-center justify-center"
          :class="category.bgColor"
        >
          <component :is="category.icon" class="w-7 h-7" :class="category.iconColor" />
        </div>
        <h3 class="text-lg font-semibold text-[var(--text-primary)] mb-2 group-hover:text-[#22C55E] transition-colors">
          {{ category.title }}
        </h3>
        <p class="text-sm text-[var(--text-muted)] mb-4 line-clamp-2">
          {{ category.description }}
        </p>
        <div class="flex items-center justify-between">
          <span 
            class="text-xs px-2 py-1 rounded-full"
            :class="category.tagBg"
          >
            {{ category.count }}篇文章
          </span>
          <svg class="w-5 h-5 text-[var(--text-muted)] group-hover:text-[#22C55E] group-hover:translate-x-1 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 推荐阅读 -->
    <div class="mt-8">
      <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
        推荐阅读
      </h2>
      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="article in recommendedArticles"
          :key="article.id"
          @click="viewArticle(article.id)"
          class="card p-4 cursor-pointer hover:border-[#22C55E]/50 transition-colors"
        >
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-lg bg-[#22C55E]/20 flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-[#22C55E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium text-[var(--text-primary)] truncate">{{ article.title }}</h4>
              <p class="text-xs text-[var(--text-muted)] mt-1 line-clamp-2">{{ article.excerpt }}</p>
              <div class="flex items-center gap-2 mt-2">
                <span class="text-xs text-[var(--text-muted)]">{{ article.readTime }}</span>
                <span class="text-xs text-[var(--text-muted)]">·</span>
                <span class="text-xs text-[var(--text-muted)]">{{ article.category }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// SVG 图标组件
const IconRobot = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
])

const IconPencil = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z' })
])

const IconTarget = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
])

const IconChart = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])

const IconWarning = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' })
])

const IconBook = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const IconAcademic = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 14l9-5-9-5-9 5 9 5z' }),
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z' })
])

const IconQuestion = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-7 h-7' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
])

const categories = [
  {
    id: 'ai-basics',
    title: 'AI 基础知识',
    description: '什么是 AI？什么是大模型？了解人工智能的基本概念',
    icon: IconRobot,
    bgColor: 'bg-[#3B82F6]/20',
    iconColor: 'text-[#3B82F6]',
    tagBg: 'bg-[#3B82F6]/20 text-[#3B82F6]',
    count: 1
  },
  {
    id: 'prompt-engineering',
    title: '提示词工程',
    description: '学习如何编写有效的提示词，让 AI 更好地理解你的需求',
    icon: IconPencil,
    bgColor: 'bg-[#22C55E]/20',
    iconColor: 'text-[#22C55E]',
    tagBg: 'bg-[#22C55E]/20 text-[#22C55E]',
    count: 2
  },
  {
    id: 'model-selection',
    title: '模型选择指南',
    description: '了解不同大模型的特点，选择最适合你的模型',
    icon: IconTarget,
    bgColor: 'bg-[#F59E0B]/20',
    iconColor: 'text-[#F59E0B]',
    tagBg: 'bg-[#F59E0B]/20 text-[#F59E0B]',
    count: 1
  },
  {
    id: 'analysis-principles',
    title: 'AI 分析股票原理',
    description: '深入了解多智能体如何协作分析股票',
    icon: IconChart,
    bgColor: 'bg-[#8B5CF6]/20',
    iconColor: 'text-[#8B5CF6]',
    tagBg: 'bg-[#8B5CF6]/20 text-[#8B5CF6]',
    count: 1
  },
  {
    id: 'risks-limitations',
    title: '风险与局限性',
    description: '了解 AI 的潜在问题和正确使用方式',
    icon: IconWarning,
    bgColor: 'bg-[#EF4444]/20',
    iconColor: 'text-[#EF4444]',
    tagBg: 'bg-[#EF4444]/20 text-[#EF4444]',
    count: 1
  },
  {
    id: 'resources',
    title: '源项目与论文',
    description: 'TradingAgents 项目介绍和学术论文资源',
    icon: IconBook,
    bgColor: 'bg-[#06B6D4]/20',
    iconColor: 'text-[#06B6D4]',
    tagBg: 'bg-[#06B6D4]/20 text-[#06B6D4]',
    count: 2
  },
  {
    id: 'tutorials',
    title: '实战教程',
    description: '通过实际案例学习如何使用本工具',
    icon: IconAcademic,
    bgColor: 'bg-[#EC4899]/20',
    iconColor: 'text-[#EC4899]',
    tagBg: 'bg-[#EC4899]/20 text-[#EC4899]',
    count: 2
  },
  {
    id: 'faq',
    title: '常见问题',
    description: '解答使用过程中的常见疑问',
    icon: IconQuestion,
    bgColor: 'bg-[#64748B]/20',
    iconColor: 'text-[var(--text-muted)]',
    tagBg: 'bg-[#64748B]/20 text-[var(--text-muted)]',
    count: 5
  }
]

const recommendedArticles = [
  { id: 'what-is-ai', title: '什么是人工智能？', excerpt: '了解 AI 的基本概念、发展历史和应用领域...', readTime: '5分钟', category: 'AI基础知识' },
  { id: 'prompt-guide', title: '提示词编写指南', excerpt: '如何写出高质量的提示词，让 AI 更准确地理解你的需求...', readTime: '8分钟', category: '提示词工程' },
  { id: 'multi-agent', title: '多智能体分析原理', excerpt: '深入了解 TradingAgents 如何通过多个 AI 智能体协作进行股票分析...', readTime: '10分钟', category: '分析原理' },
]

const navigateTo = (categoryId: string) => {
  router.push(`/learning/category/${categoryId}`)
}

const viewArticle = (articleId: string) => {
  router.push(`/learning/article/${articleId}`)
}
</script>
