<template>
  <div class="route-analysis-container">
    <!-- 概览统计 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">推荐路线总数</div>
          <div class="stat-value primary">{{ overview.total_routes }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">今日使用次数</div>
          <div class="stat-value success">{{ overview.today_usage }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">平均评分</div>
          <div class="stat-value warning">{{ overview.avg_rating }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">采纳率</div>
          <div class="stat-value danger">{{ overview.adoption_rate }}%</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 热门路线 & 使用趋势 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="14">
        <el-card header="热门路线 TOP 5">
          <el-table :data="hotRoutes" style="width: 100%">
            <el-table-column prop="rank" label="排名" width="60">
              <template #default="scope">
                <el-tag :type="scope.row.rank <= 3 ? 'danger' : 'info'" size="small">{{ scope.row.rank }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="路线名称" min-width="180" />
            <el-table-column prop="usage" label="使用次数" width="100" />
            <el-table-column prop="rating" label="用户评分" width="180">
              <template #default="scope">
                <div class="rating-cell">
                  <el-rate v-model="scope.row.rating" disabled show-score text-color="#E6A23C" />
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="avgDuration" label="平均耗时" width="100" />
            <el-table-column prop="trend" label="趋势" width="100">
              <template #default="scope">
                <span :class="scope.row.trend > 0 ? 'trend-up' : 'trend-down'">
                  <el-icon><component :is="scope.row.trend > 0 ? 'Top' : 'Bottom'" /></el-icon>
                  {{ Math.abs(scope.row.trend) }}%
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card header="7日使用趋势">
          <div ref="usageTrendChart" style="height: 320px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 线路评分分布 & 优化建议 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card header="路线评分分布">
          <div ref="ratingChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="路线优化建议">
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in suggestions"
              :key="index"
              :type="item.priority === '高' ? 'danger' : item.priority === '中' ? 'warning' : 'primary'"
              :timestamp="item.date"
            >
              <strong>{{ item.title }}</strong>
              <p class="suggestion-desc">{{ item.desc }}</p>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, shallowRef } from 'vue'
import * as echarts from 'echarts'

const overview = ref({
  total_routes: 24,
  today_usage: 1284,
  avg_rating: 4.7,
  adoption_rate: 82
})

const hotRoutes = ref([
  { rank: 1, name: '灵山大佛深度游', usage: 452, rating: 4.8, avgDuration: '2.5h', trend: 12 },
  { rank: 2, name: '梵宫艺术之旅', usage: 385, rating: 4.9, avgDuration: '2.0h', trend: -3 },
  { rank: 3, name: '九龙灌浴祈福线', usage: 312, rating: 4.7, avgDuration: '1.8h', trend: 8 },
  { rank: 4, name: '五印坛城文化线', usage: 256, rating: 4.6, avgDuration: '2.2h', trend: 5 },
  { rank: 5, name: '祥符禅寺古迹线', usage: 198, rating: 4.5, avgDuration: '1.5h', trend: 15 }
])

const suggestions = ref([
  { title: '灵山大佛线需增加讲解密度', desc: '游客反馈大佛区域讲解间隔过长，建议在佛手广场和佛像下方各增加一个讲解点。', priority: '高', date: '2024-05-20' },
  { title: '梵宫路线可分流优化', desc: '周末梵宫路线拥挤，建议引入分时段推荐策略，分散游客流量。', priority: '高', date: '2024-05-19' },
  { title: '亲子路线缺乏互动', desc: '亲子家庭反馈路线缺少互动环节，建议增加趣味问答和寻宝打卡。', priority: '中', date: '2024-05-18' },
  { title: '老年路线步行强度过大', desc: '65岁以上用户反馈部分路线步行距离过长，建议增加休息点标注和慢行建议。', priority: '中', date: '2024-05-17' }
])

const usageTrendChart = ref()
const ratingChart = ref()

onMounted(() => {
  // 7日使用趋势柱状图
  const trend = echarts.init(usageTrendChart.value)
  trend.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['5-14', '5-15', '5-16', '5-17', '5-18', '5-19', '5-20']
    },
    yAxis: { type: 'value', name: '使用次数' },
    series: [
      {
        type: 'bar',
        data: [980, 1050, 1120, 1254, 1380, 1420, 1284],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409EFF' },
            { offset: 1, color: '#a0cfff' }
          ]),
          borderRadius: [4, 4, 0, 0]
        }
      },
      {
        type: 'line',
        data: [980, 1050, 1120, 1254, 1380, 1420, 1284],
        smooth: true,
        lineStyle: { color: '#67C23A', width: 2 },
        itemStyle: { color: '#67C23A' },
        symbol: 'circle',
        symbolSize: 6
      }
    ]
  })

  // 评分分布
  const rating = echarts.init(ratingChart.value)
  rating.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '50%'],
      roseType: 'radius',
      label: { show: true, formatter: '{b}: {c}条' },
      data: [
        { value: 15, name: '5星', itemStyle: { color: '#67C23A' } },
        { value: 6, name: '4星', itemStyle: { color: '#409EFF' } },
        { value: 2, name: '3星', itemStyle: { color: '#E6A23C' } },
        { value: 1, name: '2星', itemStyle: { color: '#F56C6C' } },
        { value: 0, name: '1星', itemStyle: { color: '#909399' } }
      ]
    }]
  })
})
</script>

<style scoped lang="scss">
.stat-card {
  text-align: center;
  .stat-title {
    color: #909399;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .stat-value {
    font-size: 28px;
    font-weight: bold;
    &.primary { color: #409EFF; }
    &.success { color: #67C23A; }
    &.warning { color: #E6A23C; }
    &.danger { color: #F56C6C; }
  }
}
.rating-cell {
  display: flex;
  align-items: center;
}
.trend-up { color: #F56C6C; }
.trend-down { color: #67C23A; }
.suggestion-desc {
  color: #606266;
  margin: 4px 0 0;
  font-size: 13px;
  line-height: 1.5;
}
.mt-20 {
  margin-top: 20px;
}
</style>
