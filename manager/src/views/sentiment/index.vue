<template>
  <div class="sentiment-report">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="title">今日对话数</div>
          <div class="value">{{ report.total_conversations }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="title">积极占比</div>
          <div class="value success">{{ report.sentiment_dist.positive }}%</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="title">消极占比</div>
          <div class="value danger">{{ report.sentiment_dist.negative }}%</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="title">满意度评分</div>
          <div class="value warning">{{ report.satisfaction_score }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 关注点分析 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card header="高频关注点词云">
          <div ref="wordCloudChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="热点话题 TOP 10">
          <el-table :data="report.hot_topics" style="width: 100%">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="topic" label="话题" />
            <el-table-column prop="count" label="提及次数" width="100" />
            <el-table-column prop="trend" label="趋势" width="100">
              <template #default="scope">
                <el-icon v-if="scope.row.trend > 0" color="#f56c6c"><Top /></el-icon>
                <el-icon v-else color="#67c23a"><Bottom /></el-icon>
                {{ Math.abs(scope.row.trend) }}%
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 情感趋势 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card header="7日情感趋势">
          <div ref="trendChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="情感分布对比">
          <div ref="pieChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 服务建议 -->
    <el-row class="mt-20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>AI 生成服务建议</span>
              <el-tag type="info">基于 LLM 自动总结</el-tag>
            </div>
          </template>
          <el-table :data="report.service_suggestions" style="width: 100%">
            <el-table-column prop="issue" label="识别问题" width="300" />
            <el-table-column prop="action" label="改进建议" />
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.priority === '高' ? 'danger' : 'warning'">
                  {{ scope.row.priority }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const report = ref({
  total_conversations: 1256,
  sentiment_dist: { positive: 65, neutral: 25, negative: 10 },
  satisfaction_score: 4.8,
  hot_topics: [
    { topic: '九龙灌浴表演时间', count: 452, trend: 12 },
    { topic: '梵宫门票预约', count: 385, trend: -5 },
    { topic: '素斋位置', count: 312, trend: 8 },
    { topic: '灵山大佛高度', count: 256, trend: 2 },
    { topic: '轮椅租赁', count: 198, trend: 15 }
  ],
  service_suggestions: [
    { issue: '多名游客反馈九龙灌浴排队时间长', action: '建议增加表演场次或提前广播提示', priority: '高' },
    { issue: '梵宫内部导览指示不够清晰', action: '建议优化数字人导航中的实时位置指引', priority: '中' },
    { issue: '关于景区文史背景的深度提问增加', action: '建议丰富知识库中的历史文化分块内容', priority: '高' }
  ]
})

const wordCloudChart = ref()
const trendChart = ref()
const pieChart = ref()

onMounted(() => {
  // 模拟词云 (使用散点图模拟)
  const wc = echarts.init(wordCloudChart.value)
  wc.setOption({
    series: [{
      type: 'graph',
      layout: 'force',
      force: { repulsion: 100 },
      data: [
        { name: '九龙灌浴', value: 50, symbolSize: 80, itemStyle: { color: '#409EFF' } },
        { name: '梵宫', value: 40, symbolSize: 70, itemStyle: { color: '#67C23A' } },
        { name: '灵山大佛', value: 45, symbolSize: 75, itemStyle: { color: '#E6A23C' } },
        { name: '素斋', value: 30, symbolSize: 50, itemStyle: { color: '#F56C6C' } },
        { name: '门票', value: 25, symbolSize: 45, itemStyle: { color: '#909399' } },
        { name: '交通', value: 20, symbolSize: 40, itemStyle: { color: '#009688' } }
      ],
      label: { show: true, position: 'inside' }
    }]
  })

  const trend = echarts.init(trendChart.value)
  trend.setOption({
    legend: { data: ['积极', '中性', '消极'] },
    xAxis: { type: 'category', data: ['5-14', '5-15', '5-16', '5-17', '5-18', '5-19', '5-20'] },
    yAxis: { type: 'value' },
    series: [
      { name: '积极', type: 'line', stack: 'total', data: [60, 62, 65, 63, 68, 70, 65], color: '#67C23A' },
      { name: '中性', type: 'line', stack: 'total', data: [30, 28, 25, 27, 22, 20, 25], color: '#E6A23C' },
      { name: '消极', type: 'line', stack: 'total', data: [10, 10, 10, 10, 10, 10, 10], color: '#F56C6C' }
    ]
  })

  const pie = echarts.init(pieChart.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: '70%',
      data: [
        { value: 65, name: '积极', itemStyle: { color: '#67C23A' } },
        { value: 25, name: '中性', itemStyle: { color: '#E6A23C' } },
        { value: 10, name: '消极', itemStyle: { color: '#F56C6C' } }
      ]
    }]
  })
})
</script>

<style scoped lang="scss">
.stat-card {
  text-align: center;
  .title {
    color: #909399;
    font-size: 14px;
    margin-bottom: 10px;
  }
  .value {
    font-size: 28px;
    font-weight: bold;
    &.success { color: #67C23A; }
    &.danger { color: #F56C6C; }
    &.warning { color: #E6A23C; }
  }
}
</style>
