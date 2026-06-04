<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in statCards" :key="item.title">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" :style="{ color: item.color }">
              <el-icon :size="32"><component :is="item.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card header="7日对话趋势">
          <div ref="trendChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="情感分布">
          <div ref="sentimentChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card header="热门路线 TOP 5">
          <el-table :data="hotRoutes" style="width: 100%">
            <el-table-column prop="name" label="路线名称" />
            <el-table-column prop="usage" label="使用次数" width="100" />
            <el-table-column prop="score" label="评分" width="100">
              <template #default="scope">
                <el-rate v-model="scope.row.score" disabled />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="最近反馈">
          <el-timeline>
            <el-timeline-item
              v-for="(activity, index) in recentFeedbacks"
              :key="index"
              :type="activity.type"
              :timestamp="activity.timestamp"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const statCards = [
  { title: '今日对话数', value: '1,284', icon: 'ChatDotRound', color: '#409EFF' },
  { title: '活跃用户', value: '856', icon: 'User', color: '#67C23A' },
  { title: '满意度', value: '94.2%', icon: 'Star', color: '#E6A23C' },
  { title: '平均响应时间', value: '0.8s', icon: 'Timer', color: '#F56C6C' }
]

const hotRoutes = [
  { name: '灵山大佛深度游', usage: 452, score: 4.8 },
  { name: '梵宫艺术之旅', usage: 385, score: 4.9 },
  { name: '九龙灌浴祈福线', usage: 312, score: 4.7 },
  { name: '五印坛城文化线', usage: 256, score: 4.6 },
  { name: '祥符禅寺古迹线', usage: 198, score: 4.5 }
]

const recentFeedbacks = [
  { content: '讲解非常详细，声音好听', timestamp: '2024-05-20 10:30', type: 'success' },
  { content: '九龙灌浴时间提醒很准确', timestamp: '2024-05-20 09:45', type: 'primary' },
  { content: '希望能增加更多互动内容', timestamp: '2024-05-20 09:15', type: 'warning' },
  { content: '梵宫内部导航有点迷路', timestamp: '2024-05-19 16:20', type: 'danger' }
]

const trendChart = ref()
const sentimentChart = ref()

onMounted(() => {
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    tooltip: { trigger: 'axis' },
    series: [{
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: 'line',
      smooth: true,
      color: '#409EFF',
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64,158,255,0.5)' },
          { offset: 1, color: 'rgba(64,158,255,0)' }
        ])
      }
    }]
  })

  const sentiment = echarts.init(sentimentChart.value)
  sentiment.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: '0%' },
    series: [{
      name: '情感占比',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: false },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 735, name: '积极', itemStyle: { color: '#67C23A' } },
        { value: 580, name: '中性', itemStyle: { color: '#E6A23C' } },
        { value: 184, name: '消极', itemStyle: { color: '#F56C6C' } }
      ]
    }]
  })
})
</script>

<style scoped lang="scss">
.stat-item {
  display: flex;
  align-items: center;
  .stat-icon {
    margin-right: 15px;
  }
  .stat-title {
    color: #909399;
    font-size: 14px;
    margin-bottom: 5px;
  }
  .stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #303133;
  }
}
</style>
