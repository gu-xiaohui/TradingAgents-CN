<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="flex items-center gap-3 mb-6">
      <button @click="goBack" class="flex items-center gap-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
        </svg>
      </button>
      <div class="flex items-center gap-3">
        <span class="text-2xl">{{ categoryInfo.icon }}</span>
        <h1 class="text-2xl font-bold">{{ categoryInfo.title }}</h1>
      </div>
    </div>

    <p class="text-[var(--text-secondary)] mb-6">{{ categoryInfo.description }}</p>

    <!-- 文章列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="article in articles" :key="article.id"
           @click="openArticle(article.id)"
           class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-5 hover:border-[#22C55E] transition-colors cursor-pointer">
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-semibold">{{ article.title }}</h3>
          <span :class="getDifficultyClass(article.difficulty)" class="px-2 py-0.5 rounded text-xs">
            {{ article.difficultyText }}
          </span>
        </div>
        <p class="text-sm text-[var(--text-secondary)] mb-4 line-clamp-2">{{ article.description }}</p>
        <div class="flex items-center gap-4 text-xs text-[var(--text-secondary)]">
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ article.readTime }}
          </span>
          <span class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ article.views }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const category = computed(() => route.params.category as string)

const categoryMap: Record<string, any> = {
  'ai-basics': { title: 'AI基础知识', icon: '🤖', description: '从零开始了解人工智能和大语言模型的基本概念' },
  'prompt-engineering': { title: '提示词工程', icon: '✍️', description: '学习如何编写高质量的提示词' },
  'model-selection': { title: '模型选择指南', icon: '🎯', description: '了解不同大模型的特点' },
  'analysis-principles': { title: 'AI分析股票原理', icon: '📊', description: '深入了解多智能体协作分析股票' },
  'risks-limitations': { title: '风险与局限性', icon: '⚠️', description: '了解AI的潜在问题和正确使用方式' },
  'resources': { title: '源项目与论文', icon: '📖', description: 'TradingAgents项目介绍和学术论文资源' }
}

const categoryInfo = computed(() => categoryMap[category.value] || { title: '未知分类', icon: '📚', description: '' })

const articles = computed(() => {
  // 模拟数据
  return [
    { id: '1', title: '文章1', description: '文章描述', difficulty: 'success', difficultyText: '入门', readTime: '5分钟', views: 100 },
    { id: '2', title: '文章2', description: '文章描述', difficulty: 'warning', difficultyText: '进阶', readTime: '10分钟', views: 200 },
    { id: '3', title: '文章3', description: '文章描述', difficulty: 'danger', difficultyText: '高级', readTime: '15分钟', views: 150 }
  ]
})

const getDifficultyClass = (difficulty: string): string => {
  const classMap: Record<string, string> = {
    'success': 'bg-[#22C55E]/20 text-[#22C55E]',
    'warning': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'danger': 'bg-[#EF4444]/20 text-[#EF4444]'
  }
  return classMap[difficulty] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const goBack = () => router.back()

const openArticle = (id: string) => router.push(`/learning/article/${id}`)
</script>
