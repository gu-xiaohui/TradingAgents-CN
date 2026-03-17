<template>
  <div class="stock-detail-page relative overflow-hidden text-[var(--text-primary)]" :class="{ 'is-dark': isDarkTheme }">

    <div class="detail-shell relative ">
      <div v-if="pageLoading" class="grid gap-6 lg:grid-cols-[1.45fr_0.95fr]">
        <div class="panel min-h-[320px] animate-pulse"></div>
        <div class="panel min-h-[320px] animate-pulse"></div>
        <div class="panel min-h-[420px] animate-pulse lg:col-span-2"></div>
      </div>

      <div v-else-if="pageError" class="panel flex min-h-[360px] flex-col items-center justify-center gap-4 text-center">
        <div class="status-icon bg-[#EF4444]/15 text-[#F87171]">
          <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 6.75h.008v.008H12v-.008Z" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-semibold">个股详情加载失败</h1>
          <p class="mt-2 max-w-xl text-sm text-[var(--text-secondary)]">{{ pageError }}</p>
        </div>
        <div class="flex flex-wrap items-center justify-center gap-3">
          <button class="action-btn action-btn-primary" @click="loadPageData">
            重新加载
          </button>
          <button class="action-btn" @click="router.push('/dashboard')">
            返回仪表板
          </button>
        </div>
      </div>

      <template v-else>
        <section class="grid gap-4 xl:grid-cols-[minmax(0,1.45fr)_360px]">
          <div class="hero-card">
            <div class="hero-layout">
              <div class="space-y-5 min-w-0">
                <div class="flex flex-wrap items-center gap-3">
                  <button class="ghost-link" @click="router.back()">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                    </svg>
                    返回
                  </button>
                  <span class="market-pill" :class="marketPillClass">{{ marketLabel }}</span>
                  <span v-if="displaySector" class="ghost-pill">{{ displaySector }}</span>
                  <span v-if="displayExchange" class="ghost-pill">{{ displayExchange }}</span>
                  <span v-if="displaySourceTag" class="ghost-pill ghost-pill-subtle">{{ displaySourceTag }}</span>
                </div>

                <div class="space-y-2">
                  <div class="flex flex-wrap items-end gap-x-4 gap-y-2">
                    <h1 class="text-3xl font-semibold tracking-tight md:text-4xl">{{ stockName }}</h1>
                    <span class="text-sm uppercase tracking-[0.28em] text-[var(--text-secondary)]">{{ normalizedCode }}</span>
                  </div>
                  <p class="mt-2 max-w-2xl text-sm leading-6 text-[var(--text-secondary)]">
                    {{ companyNarrative }}
                  </p>
                </div>

                <div class="hero-data-row">
                  <div class="hero-price-block">
                    <div class="price-value" :class="changeTextClass">{{ formatPrice(quote.price) }}</div>
                    <div class="mt-2 flex flex-wrap items-center gap-3 text-sm">
                      <span class="change-chip" :class="changeChipClass">{{ changeSummary }}</span>
                      <span class="text-[var(--text-secondary)]">{{ updatedSummary }}</span>
                    </div>
                  </div>

                  <div class="hero-mini-grid">
                    <div class="hero-mini-cell">
                      <span>总市值</span>
                      <strong>{{ formatLargeNumber(fundamentals.total_mv, true) }}</strong>
                    </div>
                    <div class="hero-mini-cell">
                      <span>PE</span>
                      <strong>{{ formatRatio(fundamentals.pe_ttm ?? fundamentals.pe) }}</strong>
                    </div>
                    <div class="hero-mini-cell">
                      <span>PB</span>
                      <strong>{{ formatRatio(fundamentals.pb_mrq ?? fundamentals.pb) }}</strong>
                    </div>
                    <div class="hero-mini-cell">
                      <span>ROE</span>
                      <strong>{{ formatPercentValue(fundamentals.roe) }}</strong>
                    </div>
                  </div>
                </div>

                <div class="stat-inline-grid">
                  <div v-for="item in headlineFacts" :key="item.label" class="stat-inline-card">
                    <span>{{ item.label }}</span>
                    <strong>{{ item.value }}</strong>
                  </div>
                </div>
              </div>

              <div class="action-stack">
                <button class="action-btn action-btn-primary" @click="goToAnalysis">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75h9A2.25 2.25 0 0 1 18.75 6v12A2.25 2.25 0 0 1 16.5 20.25h-9A2.25 2.25 0 0 1 5.25 18V6A2.25 2.25 0 0 1 7.5 3.75Zm0 4.5h9m-9 4.5h6" />
                  </svg>
                  单股分析
                </button>
                <button class="action-btn" @click="toggleFavorite" :disabled="favoriteLoading">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m11.48 3.499 2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.563.563 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557L3.04 10.384a.563.563 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345l2.125-5.11Z" />
                  </svg>
                  {{ isFavorite ? '移出自选' : '加入自选' }}
                </button>
                <button class="action-btn" @click="goPaperTrading">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M3.75 6h16.5A1.5 1.5 0 0 1 21.75 7.5v9A1.5 1.5 0 0 1 20.25 18H3.75a1.5 1.5 0 0 1-1.5-1.5v-9A1.5 1.5 0 0 1 3.75 6Zm3.75 7.5h3" />
                  </svg>
                  模拟交易
                </button>
                <button class="action-btn" @click="refreshQuoteOnly" :disabled="quoteRefreshing">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.992 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182" />
                  </svg>
                  刷新行情
                </button>
              </div>
            </div>

            <div class="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              <div v-for="item in statCards" :key="item.label" class="metric-card">
                <span class="metric-label">{{ item.label }}</span>
                <strong class="metric-value" :class="item.emphasis">{{ item.value }}</strong>
                <span class="metric-note">{{ item.note }}</span>
              </div>
            </div>
          </div>

          <aside class="panel sidebar-panel">
            <div class="section-heading">
              <div>
                <h2>估值快照</h2>
                <p>用当前可用的基本面数据快速判断位置与风格。</p>
              </div>
            </div>

            <div class="space-y-4">
              <div v-for="item in valuationItems" :key="item.label" class="info-row">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>

            <div class="divider"></div>

            <div class="section-heading">
              <div>
                <h2>交易画像</h2>
                <p>结合量价和换手率，帮助快速判断活跃度。</p>
              </div>
            </div>

            <div class="signal-grid">
              <div class="signal-card">
                <span>换手率</span>
                <strong>{{ formatPercentValue(quote.turnover_rate) }}</strong>
                <p>{{ turnoverHint }}</p>
              </div>
              <div class="signal-card">
                <span>振幅</span>
                <strong>{{ formatPercentValue(quote.amplitude) }}</strong>
                <p>{{ amplitudeHint }}</p>
              </div>
              <div class="signal-card">
                <span>成交额</span>
                <strong>{{ formatLargeNumber(quote.amount) }}</strong>
                <p>反映当日资金参与规模。</p>
              </div>
              <div class="signal-card">
                <span>量比替代</span>
                <strong>{{ formatLargeNumber(quote.volume) }}</strong>
                <p>当前接口以成交量替代展示。</p>
              </div>
            </div>
          </aside>
        </section>

        <section class="grid gap-4 xl:grid-cols-[minmax(0,1.45fr)_340px]">
          <div class="panel min-w-0">
            <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div class="section-heading m-0">
                <div>
                  <h2>K 线走势</h2>
                  <p>支持日线、周线、月线切换，展示价格与成交量。</p>
                </div>
              </div>
              <div class="tab-strip">
                <button
                  v-for="period in periods"
                  :key="period.value"
                  class="tab-chip"
                  :class="{ active: activePeriod === period.value }"
                  @click="changePeriod(period.value)"
                  :disabled="chartLoading"
                >
                  {{ period.label }}
                </button>
              </div>
            </div>

            <div class="chart-stage relative mt-4 h-[440px] overflow-hidden rounded-[24px]">
              <div ref="chartRef" class="h-full w-full"></div>
              <div v-if="chartLoading" class="chart-mask">图表加载中...</div>
              <div v-else-if="!kline.items.length" class="chart-mask">暂无 K 线数据</div>
            </div>
          </div>

          <aside class="panel">
            <div class="section-heading">
              <div>
                <h2>公司信息</h2>
                <p>聚合交易所、行业、板块和基础财务字段。</p>
              </div>
            </div>

            <div class="space-y-4">
              <div v-for="item in companyInfoItems" :key="item.label" class="info-row align-start">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>

            <div class="divider"></div>

            <div class="section-heading">
              <div>
                <h2>数据说明</h2>
                <p>部分字段会随数据源能力回退，空值属于正常情况。</p>
              </div>
            </div>

            <ul class="detail-list">
              <li>行情接口提供实时价格、涨跌幅、成交额、振幅和换手率。</li>
              <li>基本面接口优先返回实时估值，缺失时回退到缓存快照。</li>
              <li>新闻接口优先查库，缺失时会尝试即时同步后再次查询。</li>
            </ul>
          </aside>
        </section>

        <section class="grid gap-4 lg:grid-cols-[minmax(0,1.08fr)_minmax(0,0.92fr)] xl:grid-cols-[minmax(0,1.18fr)_minmax(0,0.82fr)]">
          <div class="panel">
            <div class="section-heading">
              <div>
                <h2>历史分析报告</h2>
                <p>展示这个股票最近完成的分析任务，并支持查看完整报告。</p>
              </div>
              <button v-if="analysisHistory.length" class="ghost-link" @click="goToAnalysis">
                发起新分析
              </button>
            </div>

            <div v-if="analysisLoading" class="empty-block">分析记录加载中...</div>
            <div v-else-if="analysisHistory.length" class="space-y-3">
              <button
                v-for="item in analysisHistory"
                :key="item.task_id"
                class="launch-card"
                @click="openAnalysisReport(item.task_id)"
              >
                <div class="flex flex-wrap items-center justify-between gap-3">
                  <strong>{{ formatAnalysisRecommendation(item.recommendation) }}</strong>
                  <span class="ghost-pill">{{ formatDateTime(item.updated_at || item.completed_at || item.created_at) }}</span>
                </div>
                <span>{{ item.summary || item.message || '点击查看完整分析报告。' }}</span>
              </button>
            </div>
            <div v-else class="empty-block">暂无历史分析报告</div>

            <div v-if="analysisError" class="mt-3 text-sm text-[#fca5a5]">{{ analysisError }}</div>
          </div>

          <div class="panel">
            <div class="section-heading">
              <div>
                <h2>近期资讯</h2>
                <p>展示最新相关新闻与公告，便于快速建立事件上下文。</p>
              </div>
              <span class="ghost-pill">{{ newsSourceLabel }}</span>
            </div>

            <div v-if="news.items.length" class="space-y-3">
              <a
                v-for="item in news.items.slice(0, 8)"
                :key="`${item.time}-${item.title}`"
                class="news-card"
                :href="item.url || '#'
                "
                target="_blank"
                rel="noreferrer"
                @click.prevent="openNews(item.url)"
              >
                <div class="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.22em] text-[var(--text-secondary)]">
                  <span>{{ item.source || '资讯' }}</span>
                  <span>{{ formatDateTime(item.time) }}</span>
                </div>
                <h3>{{ item.title }}</h3>
                <p>{{ item.summary || item.content || '暂无摘要，点击查看原文。' }}</p>
              </a>
            </div>
            <div v-else class="empty-block">暂无新闻数据</div>
          </div>

          <div class="panel">
            <div class="section-heading">
              <div>
                <h2>操作建议入口</h2>
                <p>详情页不替代分析结果，这里保留后续动作入口。</p>
              </div>
            </div>

            <div class="space-y-3">
              <button class="launch-card" @click="goToAnalysis">
                <strong>发起单股分析</strong>
                <span>带着当前股票代码跳转到分析页，直接开始生成报告。</span>
              </button>
              <button class="launch-card" @click="goPaperTrading">
                <strong>进入模拟交易</strong>
                <span>把当前股票带到模拟账户场景，便于练习买卖决策。</span>
              </button>
              <button class="launch-card" @click="toggleFavorite" :disabled="favoriteLoading">
                <strong>{{ isFavorite ? '从自选股移除' : '加入自选股' }}</strong>
                <span>自选股模块会同步展示价格和涨跌幅，便于后续跟踪。</span>
              </button>
            </div>
          </div>
        </section>

        <div v-if="reportDialogVisible" class="report-overlay" @click="closeReportDialog">
          <div class="report-dialog" @click.stop>
            <div class="section-heading mb-0">
              <div>
                <h2>分析报告详情</h2>
                <p>{{ selectedAnalysisResult?.analysis_date || '最近分析结果' }}</p>
              </div>
              <button class="ghost-link" @click="closeReportDialog">关闭</button>
            </div>

            <div v-if="reportLoading" class="empty-block mt-4">报告加载中...</div>
            <div v-else-if="selectedAnalysisResult" class="mt-4 space-y-4">
              <div class="metric-card">
                <span class="metric-label">分析摘要</span>
                <strong class="metric-value">{{ formatAnalysisRecommendation(selectedAnalysisResult.recommendation) }}</strong>
                <span class="metric-note">{{ selectedAnalysisResult.summary || '暂无摘要' }}</span>
              </div>

              <div v-if="reportTabs.length" class="tab-strip">
                <button
                  v-for="tab in reportTabs"
                  :key="tab.key"
                  class="tab-chip"
                  :class="{ active: activeReportTab === tab.key }"
                  @click="activeReportTab = tab.key"
                >
                  {{ tab.label }}
                </button>
              </div>

              <div class="report-content">
                <div class="report-markdown" v-html="activeReportHtml"></div>
              </div>
            </div>
            <div v-else class="empty-block mt-4">暂无报告内容</div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { stocksApi, type FundamentalsResponse, type KlineResponse, type NewsResponse, type QuoteResponse } from '@/api/stocks'
import { favoritesApi } from '@/api/favorites'
import { analysisApi } from '@/api/analysis'
import { useThemeStore } from '@/stores/theme'
import { extractSymbol } from '@/utils/stock'
import { getMarketByStockCode } from '@/utils/market'

type ChartPeriod = KlineResponse['period']

interface AnalysisHistoryItem {
  task_id: string
  stock_code?: string
  symbol?: string
  summary?: string
  recommendation?: string
  message?: string
  created_at?: string
  updated_at?: string
  completed_at?: string
}

interface AnalysisTaskResult {
  analysis_id?: string
  analysis_date?: string
  summary?: string
  recommendation?: string
  reports?: Record<string, string>
}

type NewsEntry = NewsResponse['items'][number] & {
  content?: string
  summary?: string
}

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()

const pageLoading = ref(true)
const pageError = ref('')
const quoteRefreshing = ref(false)
const chartLoading = ref(false)
const favoriteLoading = ref(false)
const analysisLoading = ref(false)
const analysisError = ref('')
const reportDialogVisible = ref(false)
const reportLoading = ref(false)
const activeReportTab = ref('summary')

const quote = ref<QuoteResponse>({ symbol: '', price: 0 })
const fundamentals = ref<FundamentalsResponse>({ symbol: '' })
const kline = ref<KlineResponse>({ symbol: '', period: 'day', limit: 120, adj: 'none', items: [] })
const news = ref<NewsResponse & { items: NewsEntry[] }>({
  symbol: '',
  days: 30,
  limit: 20,
  include_announcements: true,
  items: []
})
const isFavorite = ref(false)
const activePeriod = ref<ChartPeriod>('day')
const chartRef = ref<HTMLDivElement | null>(null)
const analysisHistory = ref<AnalysisHistoryItem[]>([])
const selectedAnalysisResult = ref<AnalysisTaskResult | null>(null)

let chart: ECharts | null = null

const periods: Array<{ label: string; value: ChartPeriod }> = [
  { label: '日线', value: 'day' },
  { label: '周线', value: 'week' },
  { label: '月线', value: 'month' }
]

const routeCode = computed(() => String(route.params.code || '').trim().toUpperCase())
const normalizedCode = computed(() => extractSymbol(routeCode.value))
const isDarkTheme = computed(() => themeStore.getActualTheme() === 'dark')

const inferMarket = (value: string): 'CN' | 'HK' | 'US' => {
  const input = value.trim().toUpperCase()
  const queryMarket = String(route.query.market || '').trim().toUpperCase()

  if (['US', '美股'].includes(queryMarket)) return 'US'
  if (['HK', '港股'].includes(queryMarket)) return 'HK'
  if (['US', '美股'].includes(getMarketByStockCode(value))) return 'US'
  if (['港股'].includes(getMarketByStockCode(value)) || input.endsWith('.HK') || /^\d{4,5}$/.test(input)) return 'HK'
  if (/^[A-Z]+$/.test(input)) return 'US'
  return 'CN'
}

const marketCode = computed(() => inferMarket(normalizedCode.value))
const marketLabel = computed(() => {
  if (marketCode.value === 'HK') return '港股'
  if (marketCode.value === 'US') return '美股'
  return 'A股'
})

const isMeaningfulText = (value?: string | null) => {
  const text = String(value || '').trim()
  if (!text) return false
  return !['未知', 'unknown', 'UNKNOWN', 'null', 'NULL', '--', 'database', 'DATABASE'].includes(text)
}

const displaySector = computed(() => {
  const sector = fundamentals.value.sector
  return isMeaningfulText(sector) ? sector : ''
})

const displayExchange = computed(() => {
  const market = fundamentals.value.market
  return isMeaningfulText(market) && market !== displaySector.value ? market : ''
})

const displaySourceTag = computed(() => {
  const source = String(quote.value.source || news.value.source || '').trim().toLowerCase()
  const map: Record<string, string> = {
    database: '缓存数据',
    mongodb: '缓存数据',
    realtime: '实时数据',
    cache_or_api: '聚合数据'
  }
  if (!source) return ''
  return map[source] || (isMeaningfulText(source) ? source : '')
})

const stockName = computed(() => fundamentals.value.name || quote.value.name || normalizedCode.value)
const companyNarrative = computed(() => {
  const parts = [fundamentals.value.industry, displaySector.value, displayExchange.value].filter(Boolean)
  if (!parts.length) return '当前页面聚合实时行情、估值快照、K 线走势和新闻事件，帮助快速完成个股初步判断。'
  return `${stockName.value} 当前归属于 ${parts.join(' / ')}，页面已聚合价格、估值、量能与资讯，用于快速完成首轮研判。`
})

const marketPillClass = computed(() => {
  if (marketCode.value === 'HK') return 'market-pill-hk'
  if (marketCode.value === 'US') return 'market-pill-us'
  return 'market-pill-cn'
})

const changeAmount = computed(() => {
  const price = quote.value.price ?? 0
  const prevClose = quote.value.prev_close ?? 0
  if (!price || !prevClose) return null
  return price - prevClose
})

const changeTextClass = computed(() => {
  if ((quote.value.change_percent ?? 0) > 0) return 'text-[#F87171]'
  if ((quote.value.change_percent ?? 0) < 0) return 'text-[#34D399]'
  return 'text-[var(--text-primary)]'
})

const changeChipClass = computed(() => {
  if ((quote.value.change_percent ?? 0) > 0) return 'change-chip-up'
  if ((quote.value.change_percent ?? 0) < 0) return 'change-chip-down'
  return 'change-chip-flat'
})

const changeSummary = computed(() => {
  const pct = quote.value.change_percent
  const amount = changeAmount.value
  if (pct == null || amount == null || (!pct && !amount)) return '平盘'
  const amountPrefix = amount > 0 ? '+' : ''
  const pctPrefix = pct > 0 ? '+' : ''
  return `${amountPrefix}${amount.toFixed(2)} / ${pctPrefix}${pct.toFixed(2)}%`
})

const updatedSummary = computed(() => {
  const timestamp = quote.value.updated_at || quote.value.trade_date || fundamentals.value.updated_at
  return timestamp ? `更新于 ${formatDateTime(timestamp)}` : '暂无更新时间'
})

const turnoverHint = computed(() => {
  const value = quote.value.turnover_rate ?? fundamentals.value.turnover_rate ?? 0
  if (value >= 10) return '活跃度较高，短线资金参与明显。'
  if (value >= 3) return '活跃度中等，关注后续放量变化。'
  return '换手偏低，更适合结合基本面观察。'
})

const amplitudeHint = computed(() => {
  const value = quote.value.amplitude ?? 0
  if (value >= 8) return '日内波动较大，适合结合事件驱动观察。'
  if (value >= 3) return '波动正常，可结合量能确认方向。'
  return '日内波动有限，更多依赖中期趋势。'
})

const statCards = computed(() => [
  {
    label: '今开 / 昨收',
    value: `${formatPrice(quote.value.open)} / ${formatPrice(quote.value.prev_close)}`,
    note: '衡量日内跳空与承接。',
    emphasis: ''
  },
  {
    label: '最高 / 最低',
    value: `${formatPrice(quote.value.high)} / ${formatPrice(quote.value.low)}`,
    note: '观察盘中上攻和回撤区间。',
    emphasis: ''
  },
  {
    label: '成交量',
    value: formatLargeNumber(quote.value.volume),
    note: '量价是否同步需要重点确认。',
    emphasis: ''
  },
  {
    label: '成交额',
    value: formatLargeNumber(quote.value.amount),
    note: '资金规模决定走势可持续性。',
    emphasis: ''
  },
  {
    label: '换手率',
    value: formatPercentValue(quote.value.turnover_rate),
    note: '短线资金参与程度。',
    emphasis: ''
  },
  {
    label: '振幅',
    value: formatPercentValue(quote.value.amplitude),
    note: '日内波动水平。',
    emphasis: ''
  },
  {
    label: '流通市值',
    value: formatLargeNumber(fundamentals.value.circ_mv, true),
    note: '决定资金拉动难度。',
    emphasis: ''
  },
  {
    label: '市销率',
    value: formatRatio(fundamentals.value.ps_ttm ?? fundamentals.value.ps),
    note: '适合收入型公司横向比较。',
    emphasis: ''
  }
])

const headlineFacts = computed(() => [
  { label: '行业', value: isMeaningfulText(fundamentals.value.industry) ? fundamentals.value.industry : '待补充' },
  { label: '成交额', value: formatLargeNumber(quote.value.amount) },
  { label: '换手率', value: formatPercentValue(quote.value.turnover_rate) },
  { label: '振幅', value: formatPercentValue(quote.value.amplitude) }
])

const valuationItems = computed(() => [
  { label: '行业', value: fundamentals.value.industry || '--' },
  { label: '板块', value: fundamentals.value.sector || fundamentals.value.market || '--' },
  { label: 'PE(TTM)', value: formatRatio(fundamentals.value.pe_ttm ?? fundamentals.value.pe) },
  { label: 'PB(MRQ)', value: formatRatio(fundamentals.value.pb_mrq ?? fundamentals.value.pb) },
  { label: 'PS(TTM)', value: formatRatio(fundamentals.value.ps_ttm ?? fundamentals.value.ps) },
  { label: 'ROE', value: formatPercentValue(fundamentals.value.roe) },
  { label: '负债率', value: formatPercentValue(fundamentals.value.debt_ratio) },
  { label: '总市值', value: formatLargeNumber(fundamentals.value.total_mv, true) }
])

const companyInfoItems = computed(() => [
  { label: '股票名称', value: stockName.value },
  { label: '股票代码', value: normalizedCode.value },
  { label: '市场类型', value: marketLabel.value },
  { label: '交易板块', value: fundamentals.value.market || '--' },
  { label: '所属行业', value: fundamentals.value.industry || '--' },
  { label: 'PE 数据源', value: fundamentals.value.pe_source || '系统回退' },
  { label: '基础面更新时间', value: formatDateTime(fundamentals.value.updated_at) },
  { label: '实时行情日期', value: formatDateTime(quote.value.trade_date) }
])

const newsSourceLabel = computed(() => news.value.source || '新闻聚合')

const reportTabs = computed(() => {
  const reports = selectedAnalysisResult.value?.reports || {}
  return Object.entries(reports).map(([key]) => ({ key, label: formatReportName(key) }))
})

const activeReportHtml = computed(() => {
  if (!selectedAnalysisResult.value) return '<p>暂无报告内容</p>'

  if (activeReportTab.value === 'summary') {
    const summary = selectedAnalysisResult.value.summary || '暂无摘要'
    const recommendation = selectedAnalysisResult.value.recommendation || '暂无建议'
    return marked.parse(`## 投资建议\n\n${recommendation}\n\n## 分析摘要\n\n${summary}`) as string
  }

  const content = selectedAnalysisResult.value.reports?.[activeReportTab.value]
  return marked.parse(content || '暂无报告内容') as string
})

const formatPrice = (value?: number | null) => {
  if (value == null || Number.isNaN(value)) return '--'
  return Number(value).toFixed(2)
}

const formatRatio = (value?: number | null) => {
  if (value == null || Number.isNaN(value)) return '--'
  return Number(value).toFixed(2)
}

const formatPercentValue = (value?: number | null) => {
  if (value == null || Number.isNaN(value)) return '--'
  return `${Number(value).toFixed(2)}%`
}

const formatLargeNumber = (value?: number | null, isMarketCap = false) => {
  if (value == null || Number.isNaN(value)) return '--'
  const amount = Number(value)

  if (isMarketCap) {
    if (amount >= 10000) return `${(amount / 10000).toFixed(2)}万亿`
    return `${amount.toFixed(2)}亿`
  }

  if (Math.abs(amount) >= 1e8) return `${(amount / 1e8).toFixed(2)}亿`
  if (Math.abs(amount) >= 1e4) return `${(amount / 1e4).toFixed(2)}万`
  return amount.toFixed(0)
}

const formatDateTime = (value?: string | null) => {
  if (!value) return '--'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value
  return parsed.toLocaleString('zh-CN', { hour12: false })
}

const ensureChart = async () => {
  await nextTick()
  if (!chartRef.value) return null
  if (!chart) {
    chart = echarts.init(chartRef.value)
    window.addEventListener('resize', handleResize)
  }
  return chart
}

const getDetailThemeColor = (name: string, fallback: string) => {
  const host = chartRef.value?.closest('.stock-detail-page') as HTMLElement | null
  const styles = getComputedStyle(host || document.documentElement)
  const value = styles.getPropertyValue(name).trim()
  return value || fallback
}

const handleResize = () => {
  chart?.resize()
}

const buildChartOption = (): EChartsOption => {
  const items = kline.value.items || []
  const dates = items.map((item) => item.time)
  const riseColor = getDetailThemeColor('--detail-rise', '#f87171')
  const fallColor = getDetailThemeColor('--detail-fall', '#34d399')
  const axisColor = getDetailThemeColor('--detail-axis', '#94A3B8')
  const axisMutedColor = getDetailThemeColor('--detail-axis-muted', '#64748B')
  const splitColor = getDetailThemeColor('--detail-split-line', 'rgba(148, 163, 184, 0.09)')
  const tooltipBg = getDetailThemeColor('--detail-tooltip-bg', 'rgba(6, 18, 28, 0.92)')
  const tooltipBorder = getDetailThemeColor('--detail-tooltip-border', 'rgba(255,255,255,0.08)')
  const tooltipText = getDetailThemeColor('--detail-tooltip-text', '#E5EEF5')
  const candleData = items.map((item) => [item.open ?? 0, item.close ?? 0, item.low ?? 0, item.high ?? 0])
  const volumes = items.map((item) => ({
    value: item.volume ?? 0,
    itemStyle: {
      color: (item.close ?? 0) >= (item.open ?? 0) ? riseColor : fallColor
    }
  }))

  return {
    animation: false,
    backgroundColor: 'transparent',
    grid: [
      { left: 18, right: 18, top: 18, height: '63%' },
      { left: 18, right: 18, top: '75%', height: '16%' }
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      backgroundColor: tooltipBg,
      borderColor: tooltipBorder,
      textStyle: { color: tooltipText }
    },
    xAxis: [
      {
        type: 'category',
        data: dates,
        scale: true,
        boundaryGap: false,
        axisLine: { lineStyle: { color: axisColor } },
        axisLabel: { color: axisColor },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      },
      {
        type: 'category',
        gridIndex: 1,
        data: dates,
        scale: true,
        boundaryGap: false,
        axisLine: { lineStyle: { color: axisColor } },
        axisLabel: { color: axisMutedColor, showMaxLabel: true },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      }
    ],
    yAxis: [
      {
        scale: true,
        axisLine: { show: false },
        axisLabel: { color: axisColor },
        splitLine: { lineStyle: { color: splitColor } }
      },
      {
        gridIndex: 1,
        scale: true,
        axisLine: { show: false },
        axisLabel: { color: axisMutedColor },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        type: 'candlestick',
        data: candleData,
        itemStyle: {
          color: riseColor,
          color0: fallColor,
          borderColor: riseColor,
          borderColor0: fallColor
        }
      },
      {
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        barWidth: '55%'
      }
    ]
  }
}

const renderChart = async () => {
  const chartInstance = await ensureChart()
  if (!chartInstance) return
  chartInstance.setOption(buildChartOption(), true)
}

const loadChart = async (period: ChartPeriod) => {
  chartLoading.value = true
  try {
    const response = await stocksApi.getKline(normalizedCode.value, period, 120, 'qfq')
    kline.value = response.data
    await renderChart()
  } catch (error) {
    console.error('加载 K 线失败:', error)
    kline.value = { symbol: normalizedCode.value, period, limit: 120, adj: 'qfq', items: [] }
    await renderChart()
  } finally {
    chartLoading.value = false
  }
}

const hasMeaningfulQuote = (data?: QuoteResponse) => Boolean(
  data && (data.price != null || data.name || data.updated_at || data.trade_date || data.amount != null)
)

const hasMeaningfulFundamentals = (data?: FundamentalsResponse) => Boolean(
  data && (data.name || data.industry || data.market || data.pe != null || data.total_mv != null)
)

const loadPageData = async () => {
  pageLoading.value = true
  pageError.value = ''
  analysisLoading.value = true
  analysisError.value = ''

  try {
    const [quoteResult, fundamentalsResult, newsResult, favoriteResult, klineResult, analysisResult] = await Promise.allSettled([
      stocksApi.getQuote(normalizedCode.value),
      stocksApi.getFundamentals(normalizedCode.value),
      stocksApi.getNews(normalizedCode.value, 30, 20, true),
      favoritesApi.check(normalizedCode.value),
      stocksApi.getKline(normalizedCode.value, activePeriod.value, 120, 'qfq'),
      analysisApi.getHistory({ symbol: normalizedCode.value, page: 1, page_size: 5, status: 'completed' })
    ])

    const hasQuote = quoteResult.status === 'fulfilled' && hasMeaningfulQuote(quoteResult.value.data)
    const hasFundamentals = fundamentalsResult.status === 'fulfilled' && hasMeaningfulFundamentals(fundamentalsResult.value.data)
    const hasKline = klineResult.status === 'fulfilled' && Array.isArray(klineResult.value.data.items) && klineResult.value.data.items.length > 0
    const hasNews = newsResult.status === 'fulfilled' && Array.isArray(newsResult.value.data.items) && newsResult.value.data.items.length > 0
    const hasHistory = analysisResult.status === 'fulfilled' && Array.isArray(analysisResult.value.data?.tasks) && analysisResult.value.data.tasks.length > 0

    if (!hasQuote && !hasFundamentals && !hasKline && !hasNews && !hasHistory) {
      throw new Error('未能获取该股票的行情或基本面数据，请确认代码是否正确，或先完成后台数据同步。')
    }

    if (quoteResult.status === 'fulfilled') quote.value = quoteResult.value.data
    if (fundamentalsResult.status === 'fulfilled') fundamentals.value = fundamentalsResult.value.data
    if (newsResult.status === 'fulfilled') news.value = newsResult.value.data as NewsResponse & { items: NewsEntry[] }
    if (favoriteResult.status === 'fulfilled') isFavorite.value = favoriteResult.value.data.is_favorite
    if (klineResult.status === 'fulfilled') kline.value = klineResult.value.data
    if (analysisResult.status === 'fulfilled') {
      analysisHistory.value = analysisResult.value.data?.tasks || []
    } else {
      analysisHistory.value = []
      analysisError.value = '历史分析记录加载失败'
    }

    await renderChart()
  } catch (error) {
    console.error('加载个股详情失败:', error)
    pageError.value = error instanceof Error ? error.message : '未知错误'
  } finally {
    pageLoading.value = false
    analysisLoading.value = false
  }
}

const refreshQuoteOnly = async () => {
  quoteRefreshing.value = true
  try {
    const response = await stocksApi.getQuote(normalizedCode.value)
    quote.value = response.data
    ElMessage.success('行情已刷新')
  } catch (error) {
    console.error('刷新行情失败:', error)
    ElMessage.error('刷新行情失败')
  } finally {
    quoteRefreshing.value = false
  }
}

const toggleFavorite = async () => {
  favoriteLoading.value = true
  try {
    if (isFavorite.value) {
      await favoritesApi.remove(normalizedCode.value)
      isFavorite.value = false
      ElMessage.success('已移出自选股')
      return
    }

    await favoritesApi.add({
      stock_code: normalizedCode.value,
      stock_name: stockName.value,
      market: marketLabel.value
    })
    isFavorite.value = true
    ElMessage.success('已加入自选股')
  } catch (error) {
    console.error('更新自选股失败:', error)
    ElMessage.error('自选股操作失败')
  } finally {
    favoriteLoading.value = false
  }
}

const changePeriod = async (period: ChartPeriod) => {
  if (activePeriod.value === period) return
  activePeriod.value = period
  await loadChart(period)
}

const formatReportName = (key: string) => {
  const nameMap: Record<string, string> = {
    summary: '摘要',
    market_report: '市场分析',
    fundamentals_report: '基本面分析',
    sentiment_report: '情绪分析',
    news_report: '新闻分析',
    investment_plan: '投资计划',
    trader_investment_plan: '交易员计划',
    final_trade_decision: '最终决策',
    research_team_decision: '研究团队决策',
    risk_management_decision: '风险管理决策',
    detailed_analysis: '详细分析'
  }

  return nameMap[key] || key.replace(/_/g, ' ')
}

const formatAnalysisRecommendation = (text?: string) => {
  if (!text) return '最近分析结果'
  return text.length > 44 ? `${text.slice(0, 44)}...` : text
}

const openAnalysisReport = async (taskId: string) => {
  reportDialogVisible.value = true
  reportLoading.value = true
  activeReportTab.value = 'summary'

  try {
    const response = await analysisApi.getTaskResult(taskId)
    selectedAnalysisResult.value = response.data || null

    if (selectedAnalysisResult.value?.reports && Object.keys(selectedAnalysisResult.value.reports).length > 0) {
      activeReportTab.value = Object.keys(selectedAnalysisResult.value.reports)[0]
    }
  } catch (error) {
    console.error('加载分析报告失败:', error)
    selectedAnalysisResult.value = null
    ElMessage.error('加载分析报告失败')
  } finally {
    reportLoading.value = false
  }
}

const closeReportDialog = () => {
  reportDialogVisible.value = false
  selectedAnalysisResult.value = null
  activeReportTab.value = 'summary'
}

const goToAnalysis = () => {
  router.push(`/analysis?stock_code=${normalizedCode.value}`)
}

const goPaperTrading = () => {
  router.push(`/paper?code=${normalizedCode.value}`)
}

const openNews = (url?: string) => {
  if (!url) {
    ElMessage.info('该资讯暂无原文链接')
    return
  }

  window.open(url, '_blank', 'noopener,noreferrer')
}

watch(
  () => route.params.code,
  async () => {
    await loadPageData()
  },
  { immediate: true }
)

onMounted(async () => {
  await ensureChart()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  chart = null
})
</script>

<style scoped>
.stock-detail-page {
  min-height: calc(100vh - 96px);
  --detail-rise: #ef6b6b;
  --detail-fall: #13b981;
  --detail-axis: rgba(71, 85, 105, 0.82);
  --detail-axis-muted: rgba(100, 116, 139, 0.84);
  --detail-split-line: rgba(148, 163, 184, 0.14);
  --detail-tooltip-bg: rgba(255, 255, 255, 0.96);
  --detail-tooltip-border: rgba(15, 23, 42, 0.12);
  --detail-tooltip-text: #0f172a;
  --detail-grid-line: rgba(71, 85, 105, 0.08);
  --detail-glow-left: rgba(14, 165, 164, 0.12);
  --detail-glow-right: rgba(37, 99, 235, 0.11);
  --detail-grid-mask: linear-gradient(to bottom, rgba(255, 255, 255, 0.85), transparent 92%);
  --detail-panel-border: rgba(15, 23, 42, 0.08);
  --detail-panel-bg: linear-gradient(180deg, rgba(255, 255, 255, 0.94) 0%, rgba(248, 250, 252, 0.96) 100%);
  --detail-panel-shadow: 0 24px 80px rgba(15, 23, 42, 0.08);
  --detail-ghost-bg: rgba(15, 23, 42, 0.03);
  --detail-ghost-hover: rgba(15, 23, 42, 0.06);
  --detail-card-bg: rgba(255, 255, 255, 0.54);
  --detail-card-border: rgba(15, 23, 42, 0.06);
  --detail-divider: rgba(148, 163, 184, 0.25);
  --detail-empty-bg: rgba(255, 255, 255, 0.5);
  --detail-empty-border: rgba(148, 163, 184, 0.24);
  --detail-overlay: rgba(15, 23, 42, 0.32);
  --detail-chart-bg: rgba(255, 255, 255, 0.68);
  --detail-mask-bg: rgba(255, 255, 255, 0.72);
  --detail-report-bg: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.98) 100%);
  --detail-report-content: rgba(255, 255, 255, 0.72);
  --detail-code-bg: rgba(226, 232, 240, 0.72);
  --detail-subtle-text: #64748b;
}

.stock-detail-page.is-dark {
  --detail-rise: #f87171;
  --detail-fall: #34d399;
  --detail-axis: #94a3b8;
  --detail-axis-muted: #64748b;
  --detail-split-line: rgba(148, 163, 184, 0.09);
  --detail-tooltip-bg: rgba(6, 18, 28, 0.92);
  --detail-tooltip-border: rgba(255, 255, 255, 0.08);
  --detail-tooltip-text: #e5eef5;
  --detail-grid-line: rgba(148, 163, 184, 0.05);
  --detail-glow-left: rgba(16, 185, 129, 0.12);
  --detail-glow-right: rgba(59, 130, 246, 0.12);
  --detail-grid-mask: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), transparent 92%);
  --detail-panel-border: rgba(255, 255, 255, 0.08);
  --detail-panel-bg: linear-gradient(180deg, rgba(9, 22, 31, 0.9) 0%, rgba(6, 16, 24, 0.82) 100%);
  --detail-panel-shadow: 0 24px 80px rgba(2, 8, 23, 0.28);
  --detail-ghost-bg: rgba(255, 255, 255, 0.04);
  --detail-ghost-hover: rgba(255, 255, 255, 0.07);
  --detail-card-bg: rgba(255, 255, 255, 0.035);
  --detail-card-border: rgba(255, 255, 255, 0.07);
  --detail-divider: rgba(148, 163, 184, 0.25);
  --detail-empty-bg: rgba(255, 255, 255, 0.025);
  --detail-empty-border: rgba(148, 163, 184, 0.2);
  --detail-overlay: rgba(2, 6, 23, 0.72);
  --detail-chart-bg: rgba(5, 16, 24, 0.55);
  --detail-mask-bg: rgba(6, 16, 24, 0.64);
  --detail-report-bg: linear-gradient(180deg, rgba(9, 22, 31, 0.96) 0%, rgba(6, 16, 24, 0.94) 100%);
  --detail-report-content: rgba(255, 255, 255, 0.03);
  --detail-code-bg: rgba(15, 23, 42, 0.86);
  --detail-subtle-text: #9fb2c5;
}

.detail-shell {
  margin: 0 auto;
  width: 100%;
  max-width: 1380px;
}

.hero-glow {
  position: absolute;
  border-radius: 9999px;
  filter: blur(90px);
}

.hero-glow-left {
  left: -10%;
  top: -4%;
  height: 320px;
  width: 320px;
  background: var(--detail-glow-left);
}

.hero-glow-right {
  right: -4%;
  top: 10%;
  height: 380px;
  width: 380px;
  background: var(--detail-glow-right);
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(var(--detail-grid-line) 1px, transparent 1px), linear-gradient(90deg, var(--detail-grid-line) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: var(--detail-grid-mask);
}

.panel,
.hero-card {
  border: 1px solid var(--detail-panel-border);
  background: var(--detail-panel-bg);
  backdrop-filter: blur(18px);
  box-shadow: var(--detail-panel-shadow);
}

.panel {
  border-radius: 28px;
  padding: 20px;
}

.hero-card {
  border-radius: 32px;
  padding: 22px;
  position: relative;
  overflow: hidden;
}

.hero-layout {
  display: grid;
  gap: 24px;
  grid-template-columns: minmax(0, 1fr) 220px;
  align-items: start;
}

.hero-card::after {
  content: '';
  position: absolute;
  inset: auto -8% -28% auto;
  width: 300px;
  height: 300px;
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(34, 197, 94, 0.18), transparent 68%);
}

.section-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.section-heading h2 {
  font-size: 1.1rem;
  font-weight: 600;
}

.section-heading p {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
}

.status-icon,
.market-pill,
.ghost-pill,
.change-chip,
.tab-chip,
.action-btn,
.launch-card,
.ghost-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.status-icon {
  height: 56px;
  width: 56px;
  border-radius: 18px;
}

.ghost-link,
.ghost-pill,
.tab-chip,
.action-btn {
  border: 1px solid var(--detail-panel-border);
  background: var(--detail-ghost-bg);
  color: var(--text-primary);
}

.ghost-pill-subtle {
  color: var(--detail-subtle-text);
}

.ghost-link {
  border-radius: 9999px;
  padding: 8px 14px;
  font-size: 0.9rem;
}

.market-pill,
.ghost-pill {
  border-radius: 9999px;
  padding: 8px 14px;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.market-pill-cn {
  background: rgba(248, 113, 113, 0.14);
  color: #fca5a5;
}

.market-pill-hk {
  background: rgba(251, 191, 36, 0.14);
  color: #fcd34d;
}

.market-pill-us {
  background: rgba(96, 165, 250, 0.14);
  color: #93c5fd;
}

.price-value {
  font-size: clamp(2.6rem, 5vw, 4rem);
  line-height: 1;
  font-weight: 700;
  letter-spacing: -0.04em;
}

.hero-data-row {
  display: grid;
  gap: 18px;
  grid-template-columns: minmax(240px, 0.9fr) minmax(280px, 1fr);
  align-items: end;
}

.hero-price-block {
  min-width: 0;
}

.change-chip {
  border-radius: 9999px;
  padding: 8px 14px;
  font-size: 0.92rem;
  font-weight: 600;
}

.change-chip-up {
  background: rgba(248, 113, 113, 0.14);
  color: #fca5a5;
}

.change-chip-down {
  background: rgba(52, 211, 153, 0.14);
  color: #6ee7b7;
}

.change-chip-flat {
  background: rgba(148, 163, 184, 0.14);
  color: #cbd5e1;
}

.hero-mini-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 12px;
  min-width: 0;
}

.stat-inline-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.stat-inline-card {
  border-radius: 18px;
  border: 1px solid var(--detail-card-border);
  background: var(--detail-card-bg);
  padding: 14px 16px;
}

.stat-inline-card span {
  display: block;
  color: var(--text-secondary);
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stat-inline-card strong {
  display: block;
  margin-top: 8px;
  font-size: 1rem;
  font-weight: 600;
}

.hero-mini-cell,
.metric-card,
.signal-card,
.launch-card,
.news-card {
  border: 1px solid var(--detail-card-border);
  background: var(--detail-card-bg);
}

.hero-mini-cell {
  border-radius: 20px;
  padding: 14px 16px;
}

.hero-mini-cell span,
.metric-label,
.signal-card span {
  display: block;
  color: var(--text-secondary);
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-mini-cell strong,
.signal-card strong {
  display: block;
  margin-top: 8px;
  font-size: 1.2rem;
  font-weight: 600;
}

.action-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 220px;
}

.action-btn {
  width: 100%;
  border-radius: 18px;
  padding: 12px 16px;
  font-size: 0.95rem;
  transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
}

.action-btn:hover:not(:disabled),
.launch-card:hover:not(:disabled),
.ghost-link:hover {
  transform: translateY(-1px);
  background: var(--detail-ghost-hover);
}

.action-btn:disabled,
.tab-chip:disabled,
.launch-card:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn-primary {
  background: linear-gradient(135deg, #0ea5a2 0%, #22c55e 100%);
  border-color: transparent;
  color: white;
}

.metric-card {
  border-radius: 24px;
  padding: 18px;
}

.metric-value {
  display: block;
  margin-top: 10px;
  font-size: 1.2rem;
  font-weight: 600;
}

.metric-note,
.signal-card p {
  display: block;
  margin-top: 8px;
  color: var(--text-secondary);
  font-size: 0.82rem;
  line-height: 1.5;
}

.divider {
  margin: 20px 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--detail-divider), transparent);
}

.signal-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.signal-card {
  border-radius: 22px;
  padding: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid var(--detail-card-border);
  padding-bottom: 12px;
}

.info-row:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

.info-row span {
  color: var(--text-secondary);
  font-size: 0.92rem;
}

.info-row strong {
  text-align: right;
  font-size: 0.96rem;
  font-weight: 600;
}

.align-start {
  align-items: flex-start;
}

.tab-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tab-chip {
  border-radius: 9999px;
  padding: 9px 14px;
  font-size: 0.84rem;
}

.tab-chip.active {
  background: rgba(34, 197, 94, 0.14);
  border-color: rgba(34, 197, 94, 0.4);
  color: #86efac;
}

.chart-mask,
.empty-block {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.chart-mask {
  position: absolute;
  inset: 0;
  background: var(--detail-mask-bg);
  font-size: 0.95rem;
}

.chart-stage {
  border: 1px solid var(--detail-panel-border);
  background: var(--detail-chart-bg);
}

.empty-block {
  min-height: 240px;
  border-radius: 24px;
  border: 1px dashed var(--detail-empty-border);
  background: var(--detail-empty-bg);
}

.news-card,
.launch-card {
  width: 100%;
  border-radius: 22px;
  padding: 18px;
  text-align: left;
  transition: transform 0.18s ease, background 0.18s ease;
}

.report-overlay {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--detail-overlay);
  backdrop-filter: blur(8px);
  padding: 24px;
}

.report-dialog {
  width: min(1100px, 100%);
  max-height: calc(100vh - 64px);
  overflow: auto;
  border-radius: 28px;
  border: 1px solid var(--detail-panel-border);
  background: var(--detail-report-bg);
  padding: 24px;
  box-shadow: var(--detail-panel-shadow);
}

.report-content {
  border: 1px solid var(--detail-panel-border);
  border-radius: 24px;
  background: var(--detail-report-content);
  padding: 20px;
}

.report-markdown {
  color: var(--text-primary);
  line-height: 1.7;
}

.report-markdown :deep(h1),
.report-markdown :deep(h2),
.report-markdown :deep(h3) {
  margin: 1.1em 0 0.55em;
  font-weight: 700;
}

.report-markdown :deep(p),
.report-markdown :deep(li) {
  color: var(--text-secondary);
}

.report-markdown :deep(pre) {
  overflow: auto;
  border-radius: 16px;
  background: var(--detail-code-bg);
  padding: 16px;
}

.news-card h3,
.launch-card strong {
  display: block;
  margin-top: 10px;
  font-size: 1rem;
  font-weight: 600;
}

.news-card p,
.launch-card span,
.detail-list {
  margin-top: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.65;
}

.detail-list {
  padding-left: 18px;
}

.detail-list li + li {
  margin-top: 10px;
}

@media (max-width: 1279px) {
  .detail-shell {
    max-width: 1180px;
  }

  .hero-layout {
    grid-template-columns: 1fr;
  }

  .hero-data-row {
    grid-template-columns: 1fr;
  }

  .action-stack {
    flex-direction: row;
    flex-wrap: wrap;
    min-width: 0;
  }

  .action-btn {
    width: calc(50% - 6px);
  }
}

@media (max-width: 767px) {
  .panel,
  .hero-card {
    padding: 16px;
    border-radius: 24px;
  }

  .hero-mini-grid,
  .signal-grid,
  .stat-inline-grid {
    grid-template-columns: 1fr;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .info-row strong {
    text-align: left;
  }

  .action-stack {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }

  .detail-shell {
    max-width: 100%;
  }
}

</style>
