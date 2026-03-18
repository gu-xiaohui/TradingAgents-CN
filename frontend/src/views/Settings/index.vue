<template>
  <div class="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] p-6">
    <!-- 页面头部 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#22C55E] to-[#8B5CF6] flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        设置
      </h1>
      <p class="text-[var(--text-secondary)] mt-2 ml-13">管理您的账户和应用偏好设置</p>
    </div>

    <div class="grid grid-cols-12 gap-6">
      <!-- 左侧菜单 -->
      <div class="col-span-3">
        <div class="card p-2 sticky top-6">
          <nav class="space-y-1">
            <button
              v-for="item in menuItems"
              :key="item.id"
              @click="activeTab = item.id"
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors"
              :class="activeTab === item.id 
                ? 'bg-[#22C55E]/10 text-[#22C55E]' 
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'"
            >
              <component :is="item.icon" class="w-5 h-5" />
              <span class="text-sm font-medium">{{ item.label }}</span>
            </button>
          </nav>
        </div>
      </div>

      <!-- 右侧内容 -->
      <div class="col-span-9">
        <!-- 通用设置 -->
        <div v-show="activeTab === 'general'" class="card">
          <h2 class="text-lg font-semibold mb-6">通用设置</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">用户名</label>
              <input type="text" v-model="settings.username" disabled class="input opacity-60" />
            </div>
            
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">邮箱</label>
              <input type="email" v-model="settings.email" class="input" />
            </div>
            
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">语言</label>
              <select v-model="settings.language" class="input">
                <option value="zh-CN">简体中文</option>
                <option value="en-US">English</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">时区</label>
              <select v-model="settings.timezone" class="input">
                <option value="Asia/Shanghai">Asia/Shanghai (GMT+8)</option>
                <option value="America/New_York">America/New_York (GMT-5)</option>
                <option value="Europe/London">Europe/London (GMT+0)</option>
              </select>
            </div>
          </div>
          
          <div class="mt-6 pt-6 border-t border-white/10">
            <button @click="saveSettings" class="btn-primary">保存更改</button>
          </div>
        </div>

        <!-- 分析偏好 -->
        <div v-show="activeTab === 'analysis'" class="card">
          <h2 class="text-lg font-semibold mb-6">分析偏好</h2>
          
          <div class="space-y-6">
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">默认市场</label>
              <select v-model="settings.defaultMarket" class="input">
                <option value="A股">A股市场</option>
                <option value="美股">美股市场</option>
                <option value="港股">港股市场</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-2">默认分析深度</label>
              <div class="grid grid-cols-5 gap-3">
                <button
                  v-for="i in 5"
                  :key="i"
                  @click="settings.defaultDepth = i"
                  class="p-3 rounded-xl border-2 transition-all text-center"
                  :class="settings.defaultDepth === i 
                    ? 'border-[#22C55E] bg-[#22C55E]/10 text-[#22C55E]' 
                    : 'border-white/10 bg-white/5 text-[var(--text-secondary)] hover:border-white/20'"
                >
                  <div class="text-sm font-medium">{{ i }}级</div>
                </button>
              </div>
            </div>
            
            <div>
              <label class="block text-sm text-[var(--text-secondary)] mb-3">默认分析师</label>
              <div class="grid grid-cols-2 gap-3">
                <label
                  v-for="analyst in analysts"
                  :key="analyst.id"
                  class="flex items-center gap-3 p-3 rounded-xl border-2 cursor-pointer transition-colors"
                  :class="settings.defaultAnalysts.includes(analyst.id)
                    ? 'border-[#22C55E] bg-[#22C55E]/10'
                    : 'border-white/10 bg-white/5 hover:border-white/20'"
                >
                  <input 
                    type="checkbox" 
                    :checked="settings.defaultAnalysts.includes(analyst.id)"
                    @change="toggleAnalyst(analyst.id)"
                    class="hidden"
                  />
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#22C55E]/20 to-[#8B5CF6]/20 flex items-center justify-center">
                    <component :is="analyst.icon" class="w-4 h-4 text-[#22C55E]" />
                  </div>
                  <span class="text-sm text-[var(--text-primary)]">{{ analyst.name }}</span>
                  <svg v-if="settings.defaultAnalysts.includes(analyst.id)" class="w-4 h-4 text-[#22C55E] ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </label>
              </div>
            </div>
          </div>
          
          <div class="mt-6 pt-6 border-t border-white/10">
            <button @click="saveSettings" class="btn-primary">保存更改</button>
          </div>
        </div>

        <!-- 通知设置 -->
        <div v-show="activeTab === 'notifications'" class="card">
          <h2 class="text-lg font-semibold mb-6">通知设置</h2>
          
          <div class="space-y-4">
            <label class="flex items-center justify-between p-4 rounded-xl bg-white/5 cursor-pointer hover:bg-white/10">
              <div>
                <div class="text-sm font-medium text-[var(--text-primary)]">分析完成通知</div>
                <div class="text-xs text-[var(--text-muted)] mt-1">当分析任务完成时发送通知</div>
              </div>
              <input type="checkbox" v-model="settings.notifyOnComplete" class="w-5 h-5 accent-[#22C55E]" />
            </label>
            
            <label class="flex items-center justify-between p-4 rounded-xl bg-white/5 cursor-pointer hover:bg-white/10">
              <div>
                <div class="text-sm font-medium text-[var(--text-primary)]">分析失败通知</div>
                <div class="text-xs text-[var(--text-muted)] mt-1">当分析任务失败时发送通知</div>
              </div>
              <input type="checkbox" v-model="settings.notifyOnFail" class="w-5 h-5 accent-[#22C55E]" />
            </label>
            
            <label class="flex items-center justify-between p-4 rounded-xl bg-white/5 cursor-pointer hover:bg-white/10">
              <div>
                <div class="text-sm font-medium text-[var(--text-primary)]">市场快讯推送</div>
                <div class="text-xs text-[var(--text-muted)] mt-1">每日推送市场重要快讯</div>
              </div>
              <input type="checkbox" v-model="settings.notifyNews" class="w-5 h-5 accent-[#22C55E]" />
            </label>
            
            <label class="flex items-center justify-between p-4 rounded-xl bg-white/5 cursor-pointer hover:bg-white/10">
              <div>
                <div class="text-sm font-medium text-[var(--text-primary)]">邮件订阅</div>
                <div class="text-xs text-[var(--text-muted)] mt-1">接收每周投资分析报告邮件</div>
              </div>
              <input type="checkbox" v-model="settings.emailSubscription" class="w-5 h-5 accent-[#22C55E]" />
            </label>
          </div>
          
          <div class="mt-6 pt-6 border-t border-white/10">
            <button @click="saveSettings" class="btn-primary">保存更改</button>
          </div>
        </div>

        <!-- 配置管理 -->
        <div v-show="activeTab === 'config'" class="space-y-6">
          <!-- 配置子标签 -->
          <div class="flex gap-2 flex-wrap">
            <button
              v-for="tab in configTabs"
              :key="tab.id"
              @click="configSubTab = tab.id"
              class="px-3 py-1.5 rounded-lg text-sm transition-colors"
              :class="configSubTab === tab.id
                ? 'bg-[#22C55E]/10 text-[#22C55E]'
                : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- 配置验证 -->
          <div v-show="configSubTab === 'validation'">
            <ConfigValidation />
          </div>

          <!-- 大模型配置 -->
          <div v-show="configSubTab === 'llm'" class="card">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-lg font-semibold">大模型配置</h2>
              <button @click="refreshModels" class="btn-secondary text-sm" :disabled="configLoading">
                <svg class="w-4 h-4" :class="{ 'animate-spin': configLoading }" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                </svg>
                刷新
              </button>
            </div>
            <div v-if="configLoading" class="text-center py-12">
              <svg class="w-8 h-8 mx-auto animate-spin text-[#22C55E]" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <p class="text-[var(--text-muted)] mt-2">加载中...</p>
            </div>
            <div v-else class="space-y-3">
              <div
                v-for="model in models"
                :key="model.model_name"
                class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                    :class="model.enabled ? 'bg-[#22C55E]/20' : 'bg-white/10'">
                    <svg class="w-5 h-5" :class="model.enabled ? 'text-[#22C55E]' : 'text-[var(--text-muted)]'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                    </svg>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-medium">{{ model.model_name }}</span>
                      <span v-if="model.enabled" class="badge-success">已启用</span>
                      <span v-else class="badge-info">已禁用</span>
                    </div>
                    <div class="text-sm text-[var(--text-muted)]">{{ model.provider }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <span class="text-sm text-[var(--text-muted)]">优先级: {{ model.priority }}</span>
                  <button
                    @click="toggleModel(model)"
                    class="px-3 py-1.5 rounded-lg text-sm transition-colors"
                    :class="model.enabled
                      ? 'bg-[#EF4444]/10 text-[#EF4444] hover:bg-[#EF4444]/20'
                      : 'bg-[#22C55E]/10 text-[#22C55E] hover:bg-[#22C55E]/20'"
                  >
                    {{ model.enabled ? '禁用' : '启用' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 数据源配置 -->
          <div v-show="configSubTab === 'datasource'" class="card">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-lg font-semibold">数据源配置</h2>
              <button @click="refreshDataSources" class="btn-secondary text-sm">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                </svg>
                刷新
              </button>
            </div>
            <div class="space-y-3">
              <div
                v-for="ds in dataSources"
                :key="ds.name"
                class="flex items-center justify-between p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                    :class="ds.enabled ? 'bg-[#22C55E]/20' : 'bg-white/10'">
                    <svg class="w-5 h-5" :class="ds.enabled ? 'text-[#22C55E]' : 'text-[var(--text-muted)]'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                    </svg>
                  </div>
                  <div>
                    <div class="font-medium">{{ ds.display_name || ds.name }}</div>
                    <div class="text-sm text-[var(--text-muted)]">{{ ds.type || '数据源' }}</div>
                  </div>
                </div>
                <span :class="ds.enabled ? 'badge-success' : 'badge-info'">
                  {{ ds.enabled ? '已启用' : '已禁用' }}
                </span>
              </div>
            </div>
          </div>

          <!-- 导入导出 -->
          <div v-show="configSubTab === 'import-export'" class="card">
            <h2 class="text-lg font-semibold mb-6">配置导入导出</h2>
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 rounded-xl bg-white/5">
                <div>
                  <div class="font-medium">导出配置</div>
                  <div class="text-sm text-[var(--text-muted)]">导出当前系统配置为 JSON 文件</div>
                </div>
                <button @click="exportConfig" class="btn-primary text-sm">导出</button>
              </div>
              <div class="flex items-center justify-between p-4 rounded-xl bg-white/5">
                <div>
                  <div class="font-medium">导入配置</div>
                  <div class="text-sm text-[var(--text-muted)]">从 JSON 文件导入系统配置</div>
                </div>
                <button @click="importConfig" class="btn-secondary text-sm">导入</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 缓存管理 -->
        <div v-show="activeTab === 'cache'" class="card">
          <h2 class="text-lg font-semibold mb-6">缓存管理</h2>
          
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-white/5 border border-white/10">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-sm font-medium text-[var(--text-primary)]">清除分析缓存</div>
                  <div class="text-xs text-[var(--text-muted)] mt-1">清除已完成的分析结果缓存</div>
                </div>
                <button @click="clearCache('analysis')" class="btn-secondary text-sm">清除</button>
              </div>
            </div>
            
            <div class="p-4 rounded-xl bg-white/5 border border-white/10">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-sm font-medium text-[var(--text-primary)]">清除图片缓存</div>
                  <div class="text-xs text-[var(--text-muted)] mt-1">清除图表和图片缓存</div>
                </div>
                <button @click="clearCache('images')" class="btn-secondary text-sm">清除</button>
              </div>
            </div>
            
            <div class="p-4 rounded-xl bg-white/5 border border-white/10">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-sm font-medium text-[var(--text-primary)]">清除全部缓存</div>
                  <div class="text-xs text-[var(--text-muted)] mt-1">清除所有本地缓存数据</div>
                </div>
                <button @click="clearCache('all')" class="px-3 py-1.5 rounded-lg text-sm bg-[#EF4444]/10 text-[#EF4444] hover:bg-[#EF4444]/20 transition-colors">清除全部</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import ConfigValidation from './components/ConfigValidation.vue'

const authStore = useAuthStore()
const activeTab = ref('general')
const configSubTab = ref('validation')
const configLoading = ref(false)

const configTabs = [
  { id: 'validation', label: '配置验证' },
  { id: 'llm', label: '大模型配置' },
  { id: 'datasource', label: '数据源配置' },
  { id: 'import-export', label: '导入导出' },
]

// 配置管理数据
const models = ref<any[]>([])
const dataSources = ref<any[]>([])

const getHeaders = () => ({
  'Authorization': `Bearer ${authStore.token}`,
  'Content-Type': 'application/json'
})

const refreshModels = async () => {
  configLoading.value = true
  try {
    const res = await fetch('/api/config/llm', { headers: getHeaders() })
    if (res.ok) {
      models.value = await res.json()
    }
  } catch (error) {
    console.error('加载模型失败:', error)
    ElMessage.error('加载模型失败')
  } finally {
    configLoading.value = false
  }
}

const refreshDataSources = async () => {
  try {
    const res = await fetch('/api/config/datasource', { headers: getHeaders() })
    if (res.ok) {
      dataSources.value = await res.json()
    }
  } catch (error) {
    console.error('加载数据源失败:', error)
  }
}

const toggleModel = async (model: any) => {
  try {
    const res = await fetch(`/api/config/llm/${model.provider}/${model.model_name}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({ enabled: !model.enabled })
    })
    if (res.ok) {
      model.enabled = !model.enabled
      ElMessage.success(model.enabled ? '已启用' : '已禁用')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const exportConfig = async () => {
  try {
    const res = await fetch('/api/config/export', { headers: getHeaders() })
    if (res.ok) {
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `config_${new Date().toISOString().slice(0, 10)}.json`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      ElMessage.success('配置已导出')
    }
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const importConfig = () => {
  ElMessage.info('请选择配置文件')
}

// SVG 图标组件
const IconUser = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
])
const IconChart = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
])
const IconBell = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' })
])
const IconTools = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z' })
])
const IconDatabase = () => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', class: 'w-5 h-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4' })
])

const menuItems = [
  { id: 'general', label: '通用设置', icon: IconUser },
  { id: 'analysis', label: '分析偏好', icon: IconChart },
  { id: 'notifications', label: '通知设置', icon: IconBell },
  { id: 'config', label: '配置管理', icon: IconTools },
  { id: 'cache', label: '缓存管理', icon: IconDatabase },
]

const analysts = [
  { id: 'market', name: '市场分析师', icon: IconChart },
  { id: 'fundamental', name: '基本面分析师', icon: IconChart },
  { id: 'news', name: '新闻分析师', icon: IconBell },
  { id: 'sentiment', name: '情绪分析师', icon: IconUser },
]

const settings = reactive({
  username: 'user',
  email: 'user@example.com',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  defaultMarket: 'A股',
  defaultDepth: 3,
  defaultAnalysts: ['market', 'fundamental'],
  notifyOnComplete: true,
  notifyOnFail: true,
  notifyNews: false,
  emailSubscription: false,
})

const toggleAnalyst = (id: string) => {
  const index = settings.defaultAnalysts.indexOf(id)
  if (index > -1) {
    settings.defaultAnalysts.splice(index, 1)
  } else {
    settings.defaultAnalysts.push(id)
  }
}

const saveSettings = () => {
  ElMessage.success('设置已保存')
}

const clearCache = (type: string) => {
  ElMessage.success(`已清除${type === 'all' ? '全部' : type}缓存`)
}

onMounted(async () => {
  await Promise.all([refreshModels(), refreshDataSources()])
})
</script>
