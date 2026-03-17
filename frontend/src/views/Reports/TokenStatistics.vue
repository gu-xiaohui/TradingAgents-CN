<template>
  <div class="token-statistics">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Coin /></el-icon>
        Token使用统计
      </h1>
      <p class="page-description">
        Token使用情况、成本分析和统计图表
      </p>
    </div>

    <!-- 控制面板 -->
    <el-card class="control-panel" shadow="never">
      <el-row :gutter="24" align="middle">
        <el-col :span="6">
          <el-form-item label="统计时间范围">
            <el-select v-model="timeRange" @change="loadStatistics">
              <el-option label="今天" value="today" />
              <el-option label="最近7天" value="week" />
              <el-option label="最近30天" value="month" />
              <el-option label="最近90天" value="quarter" />
              <el-option label="全部" value="all" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="供应商筛选">
            <el-select v-model="providerFilter" @change="loadStatistics" clearable>
              <el-option label="全部供应商" value="" />
              <el-option label="阿里百炼" value="dashscope" />
              <el-option label="OpenAI" value="openai" />
              <el-option label="Google" value="google" />
              <el-option label="DeepSeek" value="deepseek" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <div class="control-buttons">
            <el-button @click="loadStatistics" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
            <el-button @click="exportData">
              <el-icon><Download /></el-icon>
              导出统计
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 概览指标 -->
    <el-row :gutter="24" style="margin-top: 24px">
      <el-col :span="6">
        <el-card class="metric-card" shadow="never">
          <div class="metric-content">
            <div class="metric-value">{{ formatNumber(overview.totalRequests) }}</div>
            <div class="metric-label">总请求数</div>
            <div class="metric-change" :class="getChangeClass(overview.requestsChange)">
              {{ formatChange(overview.requestsChange) }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="never">
          <div class="metric-content">
            <div class="metric-value">{{ formatNumber(overview.totalTokens) }}</div>
            <div class="metric-label">总Token数</div>
            <div class="metric-change" :class="getChangeClass(overview.tokensChange)">
              {{ formatChange(overview.tokensChange) }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="never">
          <div class="metric-content">
            <div class="metric-value">¥{{ formatNumber(overview.totalCost) }}</div>
            <div class="metric-label">总成本</div>
            <div class="metric-change" :class="getChangeClass(overview.costChange)">
              {{ formatChange(overview.costChange) }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="never">
          <div class="metric-content">
            <div class="metric-value">¥{{ formatNumber(overview.avgCostPerRequest) }}</div>
            <div class="metric-label">平均单次成本</div>
            <div class="metric-change" :class="getChangeClass(overview.avgCostChange)">
              {{ formatChange(overview.avgCostChange) }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="24" style="margin-top: 24px">
      <!-- Token使用趋势 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <h3>📈 Token使用趋势</h3>
          </template>
          <div ref="tokenTrendChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 成本分布 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <h3>💰 成本分布</h3>
          </template>
          <div ref="costDistributionChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px">
      <!-- 供应商统计 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <h3>🏢 供应商统计</h3>
          </template>
          <div ref="providerChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 模型使用排行 -->
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <h3>🏆 模型使用排行</h3>
          </template>
          <div class="model-ranking">
            <div
              v-for="(model, index) in modelRanking"
              :key="model.name"
              class="ranking-item"
            >
              <div class="rank-number">{{ index + 1 }}</div>
              <div class="model-info">
                <div class="model-name">{{ model.name }}</div>
                <div class="model-stats">
                  {{ formatNumber(model.requests) }} 次请求 · 
                  {{ formatNumber(model.tokens) }} Token · 
                  ¥{{ formatNumber(model.cost) }}
                </div>
              </div>
              <div class="usage-bar">
                <el-progress
                  :percentage="(model.requests / modelRanking[0].requests) * 100"
                  :show-text="false"
                  :stroke-width="6"
                />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细记录表 -->
    <el-card class="records-table" shadow="never" style="margin-top: 24px">
      <template #header>
        <div class="table-header">
          <h3>📋 详细记录</h3>
          <el-input
            v-model="searchKeyword"
            placeholder="搜索股票代码或模型名称"
            style="width: 200px"
            @input="filterRecords"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-table
        :data="filteredRecords"
        v-loading="loading"
        style="width: 100%"
        :default-sort="{ prop: 'timestamp', order: 'descending' }"
      >
        <el-table-column prop="timestamp" label="时间" width="180" sortable>
          <template #default="{ row }">
            {{ formatDateTime(row.timestamp) }}
          </template>
        </el-table-column>
        <el-table-column prop="provider" label="供应商" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ getProviderName(row.provider) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="model" label="模型" width="150" />
        <el-table-column prop="stock_symbol" label="股票代码" width="100" />
        <el-table-column prop="prompt_tokens" label="输入Token" width="100" sortable />
        <el-table-column prop="completion_tokens" label="输出Token" width="100" sortable />
        <el-table-column prop="total_tokens" label="总Token" width="100" sortable />
        <el-table-column prop="cost" label="成本(¥)" width="100" sortable>
          <template #default="{ row }">
            ¥{{ formatNumber(row.cost) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="耗时(ms)" width="100" sortable />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetails(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-if="totalRecords > 0"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="totalRecords"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 16px; text-align: right"
        @size-change="loadRecords"
        @current-change="loadRecords"
      />
    </el-card>

    <!-- 空状态 -->
    <el-empty
      v-if="!loading && overview.totalRequests === 0"
      description="暂无Token使用记录"
      :image-size="200"
    >
      <template #description>
        <div class="empty-description">
          <p>暂无Token使用记录</p>
          <div class="empty-tips">
            <h4>💡 如何开始记录Token使用？</h4>
            <ul>
              <li>进行股票分析：使用股票分析功能</li>
              <li>确保API配置：检查API密钥是否正确配置</li>
              <li>启用成本跟踪：在配置管理中启用Token成本跟踪</li>
            </ul>
          </div>
        </div>
      </template>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Coin,
  Refresh,
  Download,
  Search
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import {
  getUsageStatistics,
  getUsageRecords,
  getCostByProvider,
  getCostByModel,
  getDailyCost
} from '@/api/usage'

// 响应式数据
const loading = ref(false)
const timeRange = ref('month')
const providerFilter = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)

// 图表引用
const tokenTrendChart = ref()
const costDistributionChart = ref()
const providerChart = ref()

// 数据
const overview = reactive({
  totalRequests: 0,
  totalTokens: 0,
  totalCost: 0,
  avgCostPerRequest: 0,
  requestsChange: 0,
  tokensChange: 0,
  costChange: 0,
  avgCostChange: 0
})

const records = ref<any[]>([])
const filteredRecords = ref<any[]>([])
const modelRanking = ref<any[]>([])

// 方法
const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toFixed(2)
}

const formatChange = (change: number): string => {
  if (change > 0) return `+${change.toFixed(1)}%`
  if (change < 0) return `${change.toFixed(1)}%`
  return '0%'
}

const getChangeClass = (change: number): string => {
  if (change > 0) return 'positive'
  if (change < 0) return 'negative'
  return 'neutral'
}

const formatDateTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

const getProviderName = (provider: string): string => {
  const names: Record<string, string> = {
    'dashscope': '阿里百炼',
    'openai': 'OpenAI',
    'google': 'Google',
    'deepseek': 'DeepSeek'
  }
  return names[provider] || provider
}

// 时间范围转天数
const getTimeRangeDays = (): number => {
  const map: Record<string, number> = {
    'today': 1,
    'week': 7,
    'month': 30,
    'quarter': 90,
    'all': 365
  }
  return map[timeRange.value] || 30
}

const loadStatistics = async () => {
  loading.value = true
  try {
    const days = getTimeRangeDays()
    const params: { days: number; provider?: string } = { days }
    if (providerFilter.value) {
      params.provider = providerFilter.value
    }

    const res = await getUsageStatistics(params)
    if (res.success && res.data) {
      const data = res.data
      const totalTokens = (data.total_input_tokens || 0) + (data.total_output_tokens || 0)
      const totalRequests = data.total_requests || 0
      const totalCost = data.total_cost || 0

      Object.assign(overview, {
        totalRequests,
        totalTokens,
        totalCost,
        avgCostPerRequest: totalRequests > 0 ? totalCost / totalRequests : 0,
        requestsChange: 0,
        tokensChange: 0,
        costChange: 0,
        avgCostChange: 0
      })

      // 从 by_model 数据构建模型排行
      if (data.by_model) {
        const modelEntries = Object.entries(data.by_model).map(([name, info]: [string, any]) => ({
          name,
          requests: info.requests || info.total_requests || 0,
          tokens: (info.input_tokens || 0) + (info.output_tokens || 0) || info.total_tokens || 0,
          cost: info.cost || info.total_cost || 0,
        }))
        modelEntries.sort((a, b) => b.requests - a.requests)
        modelRanking.value = modelEntries.slice(0, 10)
      }
    }

    // 加载图表数据
    await nextTick()
    await renderCharts()

  } catch {
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const loadRecords = async () => {
  try {
    const params: { provider?: string; limit?: number } = {
      limit: pageSize.value
    }
    if (providerFilter.value) {
      params.provider = providerFilter.value
    }

    const res = await getUsageRecords(params)
    if (res.success && res.data) {
      records.value = (res.data.records || []).map((r: any) => ({
        timestamp: r.timestamp,
        provider: r.provider,
        model: r.model_name || r.model || '',
        stock_symbol: r.stock_symbol || r.session_id || '',
        prompt_tokens: r.input_tokens || r.prompt_tokens || 0,
        completion_tokens: r.output_tokens || r.completion_tokens || 0,
        total_tokens: (r.input_tokens || 0) + (r.output_tokens || 0) || r.total_tokens || 0,
        cost: r.cost || 0,
        duration: r.duration || 0
      }))
      totalRecords.value = res.data.total || records.value.length
      filterRecords()
    }
  } catch {
    // 无数据时保持空列表
  }
}

const filterRecords = () => {
  if (!searchKeyword.value) {
    filteredRecords.value = records.value
  } else {
    const keyword = searchKeyword.value.toLowerCase()
    filteredRecords.value = records.value.filter((record: any) =>
      (record.stock_symbol || '').toLowerCase().includes(keyword) ||
      (record.model || '').toLowerCase().includes(keyword)
    )
  }
}

const renderCharts = async () => {
  const days = getTimeRangeDays()

  // Token使用趋势图（每日成本趋势）
  if (tokenTrendChart.value) {
    try {
      const res = await getDailyCost(days)
      const chartData = res?.data?.data || res?.data || []
      const chart1 = echarts.init(tokenTrendChart.value)
      if (Array.isArray(chartData) && chartData.length > 0) {
        chart1.setOption({
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: chartData.map((d: any) => d.date || d.day || '') },
          yAxis: { type: 'value' },
          series: [{
            data: chartData.map((d: any) => d.total_tokens || d.tokens || d.cost || 0),
            type: 'line',
            smooth: true
          }]
        })
      } else {
        chart1.setOption({
          title: { text: '暂无数据', left: 'center', top: 'center', textStyle: { color: '#999', fontSize: 14 } },
          xAxis: { type: 'category', data: [] },
          yAxis: { type: 'value' },
          series: []
        })
      }
    } catch {
      // 图表加载失败保持空
    }
  }

  // 成本分布图（按供应商）
  if (costDistributionChart.value) {
    try {
      const res = await getCostByProvider(days)
      const providerData = res?.data?.data || res?.data || []
      const chart2 = echarts.init(costDistributionChart.value)
      if (Array.isArray(providerData) && providerData.length > 0) {
        chart2.setOption({
          tooltip: { trigger: 'item' },
          series: [{
            type: 'pie',
            data: providerData.map((p: any) => ({
              value: p.cost || p.total_cost || 0,
              name: getProviderName(p.provider || p.name || '')
            }))
          }]
        })
      } else {
        chart2.setOption({
          title: { text: '暂无数据', left: 'center', top: 'center', textStyle: { color: '#999', fontSize: 14 } },
          series: []
        })
      }
    } catch {
      // 图表加载失败保持空
    }
  }

  // 供应商统计图（按模型）
  if (providerChart.value) {
    try {
      const res = await getCostByModel(days)
      const modelData = res?.data?.data || res?.data || []
      const chart3 = echarts.init(providerChart.value)
      if (Array.isArray(modelData) && modelData.length > 0) {
        chart3.setOption({
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: modelData.map((m: any) => m.model_name || m.model || m.name || '') },
          yAxis: { type: 'value' },
          series: [{
            data: modelData.map((m: any) => m.cost || m.total_cost || 0),
            type: 'bar'
          }]
        })
      } else {
        chart3.setOption({
          title: { text: '暂无数据', left: 'center', top: 'center', textStyle: { color: '#999', fontSize: 14 } },
          xAxis: { type: 'category', data: [] },
          yAxis: { type: 'value' },
          series: []
        })
      }
    } catch {
      // 图表加载失败保持空
    }
  }
}

const exportData = () => {
  ElMessage.info('导出功能开发中...')
}

const viewDetails = (row: any) => {
  ElMessage.info('详情功能开发中...')
}

// 生命周期
onMounted(() => {
  loadStatistics()
  loadRecords()
})
</script>

<style lang="scss" scoped>
.token-statistics {
  .page-header {
    margin-bottom: 24px;

    .page-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 24px;
      font-weight: 600;
      color: var(--el-text-color-primary);
      margin: 0 0 8px 0;
    }

    .page-description {
      color: var(--el-text-color-regular);
      margin: 0;
    }
  }

  .control-panel {
    .control-buttons {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }
  }

  .metric-card {
    .metric-content {
      text-align: center;
      
      .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: var(--el-color-primary);
        margin-bottom: 8px;
      }
      
      .metric-label {
        font-size: 14px;
        color: var(--el-text-color-regular);
        margin-bottom: 4px;
      }
      
      .metric-change {
        font-size: 12px;
        
        &.positive {
          color: var(--el-color-success);
        }
        
        &.negative {
          color: var(--el-color-danger);
        }
        
        &.neutral {
          color: var(--el-text-color-placeholder);
        }
      }
    }
  }

  .chart-card {
    .chart-container {
      height: 300px;
    }
    
    .model-ranking {
      .ranking-item {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid var(--el-border-color-lighter);
        
        &:last-child {
          border-bottom: none;
        }
        
        .rank-number {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: var(--el-color-primary);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          margin-right: 12px;
        }
        
        .model-info {
          flex: 1;
          
          .model-name {
            font-weight: 600;
            margin-bottom: 4px;
          }
          
          .model-stats {
            font-size: 12px;
            color: var(--el-text-color-regular);
          }
        }
        
        .usage-bar {
          width: 100px;
        }
      }
    }
  }

  .records-table {
    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      h3 {
        margin: 0;
      }
    }
  }

  .empty-description {
    .empty-tips {
      margin-top: 16px;
      text-align: left;
      
      h4 {
        margin: 0 0 8px 0;
        color: var(--el-text-color-primary);
      }
      
      ul {
        margin: 0;
        padding-left: 20px;
        
        li {
          margin-bottom: 4px;
          color: var(--el-text-color-regular);
        }
      }
    }
  }
}
</style>
