<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="flex items-center justify-between mb-6">
      <button @click="goBack" class="flex items-center gap-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
        </svg>
        返回
      </button>
      <button @click="downloadArticle" 
              class="px-4 py-2 bg-[#22C55E] hover:bg-[#16A34A] text-white rounded-lg transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        下载
      </button>
    </div>

    <div class="flex gap-6">
      <!-- 文章主体 -->
      <div class="flex-1">
        <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-6">
          <h1 class="text-2xl font-bold mb-4">{{ article.title }}</h1>
          
          <div class="flex items-center gap-4 mb-6 text-sm text-[var(--text-secondary)]">
            <span :class="getCategoryClass(article.categoryType)" class="px-2 py-0.5 rounded">
              {{ article.category }}
            </span>
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
            <span>更新于 {{ article.updateTime }}</span>
          </div>

          <div class="prose prose-invert max-w-none" v-html="article.content"></div>
        </div>

        <!-- 上下篇导航 -->
        <div class="flex justify-between mt-6">
          <button v-if="prevArticle" @click="navigateToArticle(prevArticle.id)"
                  class="flex items-center gap-2 px-4 py-2 bg-[var(--bg-secondary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            {{ prevArticle.title }}
          </button>
          <div v-else></div>
          <button v-if="nextArticle" @click="navigateToArticle(nextArticle.id)"
                  class="flex items-center gap-2 px-4 py-2 bg-[var(--bg-secondary)] hover:bg-[var(--bg-hover)] rounded-lg transition-colors">
            {{ nextArticle.title }}
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 侧边栏目录 -->
      <div class="w-64 shrink-0">
        <div class="bg-[var(--bg-secondary)] rounded-xl border border-[var(--border-color)] p-4 sticky top-6">
          <h3 class="font-semibold mb-3">目录</h3>
          <ul class="space-y-1 text-sm">
            <li v-for="heading in tableOfContents" :key="heading.id"
                :class="['cursor-pointer hover:text-[#22C55E] transition-colors py-1', 
                         heading.level === 2 ? 'pl-0' : heading.level === 3 ? 'pl-3' : 'pl-6']"
                @click="scrollToHeading(heading.id)">
              {{ heading.text }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const articleId = computed(() => route.params.id as string)

const article = ref({
  title: '',
  category: '',
  categoryType: '',
  readTime: '',
  views: 0,
  updateTime: '',
  content: ''
})

const prevArticle = ref<any>(null)
const nextArticle = ref<any>(null)
const tableOfContents = ref<any[]>([])

const getCategoryClass = (type: string): string => {
  const classMap: Record<string, string> = {
    'primary': 'bg-[#3B82F6]/20 text-[#3B82F6]',
    'success': 'bg-[#22C55E]/20 text-[#22C55E]',
    'warning': 'bg-[#F59E0B]/20 text-[#F59E0B]',
    'danger': 'bg-[#EF4444]/20 text-[#EF4444]',
    'info': 'bg-[#8B5CF6]/20 text-[#8B5CF6]'
  }
  return classMap[type] || 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
}

const goBack = () => {
  router.back()
}

const navigateToArticle = (id: string) => {
  router.push(`/learning/article/${id}`)
}

const scrollToHeading = (id: string) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const downloadArticle = () => {
  const blob = new Blob([article.value.content], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${article.value.title}.md`
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('下载成功')
}

const loadArticle = async () => {
  try {
    // 这里应该调用 API 获取文章内容
    // 暂时使用模拟数据
    article.value = {
      title: '文章标题',
      category: 'AI基础',
      categoryType: 'primary',
      readTime: '5分钟',
      views: 1234,
      updateTime: '2024-01-01',
      content: '<p>文章内容...</p>'
    }
  } catch (error) {
    console.error('加载文章失败:', error)
    ElMessage.error('加载文章失败')
  }
}

watch(articleId, loadArticle, { immediate: true })
</script>
