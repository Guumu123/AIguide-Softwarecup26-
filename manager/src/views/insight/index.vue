<template>
  <div class="insight-container">
    <!-- 顶部统计卡 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">游客总数</div>
          <div class="stat-value primary">{{ formatNum(overview.total_tourists) }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">平均满意度</div>
          <div class="stat-value success">{{ overview.avg_satisfaction }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">人均消费</div>
          <div class="stat-value warning">&yen;{{ overview.avg_cost }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">平均停留时长</div>
          <div class="stat-value danger">{{ overview.avg_duration }}h</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 游客画像 & 消费对比 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card header="游客画像分布">
          <div ref="portraitChart" style="height: 380px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="性别-消费对比">
          <div ref="genderChart" style="height: 380px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 年龄-满意度 & 停留时长分布 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card header="年龄-满意度散点图">
          <div ref="ageSatisfactionChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="停留时长分布">
          <div ref="durationChart" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 游客聚类画像 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card header="游客聚类画像">
          <el-table :data="clusters" style="width: 100%">
            <el-table-column prop="type" label="群体类型" width="120">
              <template #default="scope">
                <el-tag :type="scope.row.tagType">{{ scope.row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="ratio" label="占比" width="100" />
            <el-table-column prop="avgAge" label="平均年龄" width="100" />
            <el-table-column prop="avgCost" label="人均消费" width="120" />
            <el-table-column prop="avgSatisfaction" label="满意度" width="100" />
            <el-table-column prop="hotAttractions" label="偏好景点" min-width="300">
              <template #default="scope">
                <el-tag v-for="a in scope.row.hotAttractions" :key="a" size="small" class="mr-4" type="info">{{ a }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="suggestion" label="运营建议" min-width="250" show-overflow-tooltip />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const overview = ref({
  total_tourists: 142560,
  avg_satisfaction: 4.6,
  avg_cost: 358,
  avg_duration: 3.2
})

const clusters = ref([
  {
    type: '亲子家庭', tagType: 'success', ratio: '35%', avgAge: 35, avgCost: 520, avgSatisfaction: 4.7,
    hotAttractions: ['百子戏弥勒', '九龙灌浴', '灵山大佛'],
    suggestion: '增设亲子互动项目，推出家庭套票优惠'
  },
  {
    type: '年轻情侣', tagType: 'primary', ratio: '28%', avgAge: 26, avgCost: 380, avgSatisfaction: 4.5,
    hotAttractions: ['梵天花海', '五灯湖', '灵山梵宫'],
    suggestion: '开发夜景游览线路，增加拍照打卡点'
  },
  {
    type: '老年游客', tagType: 'warning', ratio: '22%', avgAge: 65, avgCost: 210, avgSatisfaction: 4.8,
    hotAttractions: ['灵山大佛', '祥符禅寺', '五印坛城'],
    suggestion: '增加休息设施，提供慢行游览解说'
  },
  {
    type: '独行游客', tagType: 'info', ratio: '15%', avgAge: 32, avgCost: 310, avgSatisfaction: 4.3,
    hotAttractions: ['灵山梵宫', '无尽意斋', '鹿鸣谷'],
    suggestion: '推出单人游览套餐，优化自助讲解体验'
  }
])

const portraitChart = ref()
const genderChart = ref()
const ageSatisfactionChart = ref()
const durationChart = ref()

const formatNum = (n: number) => {
  return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toString()
}

onMounted(() => {
  // 游客画像雷达图
  const portrait = echarts.init(portraitChart.value)
  portrait.setOption({
    legend: { data: ['亲子家庭', '年轻情侣', '老年游客', '独行游客'] },
    radar: {
      center: ['50%', '55%'],
      radius: '65%',
      indicator: [
        { name: '文化偏好', max: 100 },
        { name: '自然风光', max: 100 },
        { name: '互动体验', max: 100 },
        { name: '静谧禅修', max: 100 },
        { name: '美食购物', max: 100 }
      ]
    },
    series: [{
      type: 'radar',
      data: [
        { value: [60, 40, 90, 30, 70], name: '亲子家庭', areaStyle: { color: 'rgba(103,194,58,0.25)' } },
        { value: [50, 80, 60, 40, 60], name: '年轻情侣', areaStyle: { color: 'rgba(64,158,255,0.25)' } },
        { value: [90, 50, 20, 80, 30], name: '老年游客', areaStyle: { color: 'rgba(230,162,60,0.25)' } },
        { value: [70, 70, 30, 70, 20], name: '独行游客', areaStyle: { color: 'rgba(144,147,153,0.25)' } }
      ]
    }]
  })

  // 性别-消费对比
  const gender = echarts.init(genderChart.value)
  gender.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['门票', '餐饮', '购物', '娱乐', '交通'] },
    xAxis: { type: 'category', data: ['男性', '女性'] },
    yAxis: { type: 'value', name: '金额(元)' },
    series: [
      { name: '门票', type: 'bar', stack: 'total', data: [180, 170], color: '#409EFF' },
      { name: '餐饮', type: 'bar', stack: 'total', data: [120, 130], color: '#67C23A' },
      { name: '购物', type: 'bar', stack: 'total', data: [150, 180], color: '#E6A23C' },
      { name: '娱乐', type: 'bar', stack: 'total', data: [80, 85], color: '#F56C6C' },
      { name: '交通', type: 'bar', stack: 'total', data: [60, 55], color: '#909399' }
    ]
  })

  // 年龄-满意度散点图
  const ageSat = echarts.init(ageSatisfactionChart.value)
  const scatterData: [number, number, string][] = []
  const ages = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
  ages.forEach(age => {
    for (let i = 0; i < 5; i++) {
      scatterData.push([age, 3 + Math.random() * 2, age > 50 ? '老年游客' : '年轻游客'])
    }
  })
  ageSat.setOption({
    tooltip: {
      formatter: (params: any) => `${params.data[2]}<br/>年龄: ${params.data[0]}岁<br/>满意度: ${params.data[1].toFixed(1)}`
    },
    xAxis: { type: 'value', name: '年龄(岁)', min: 18, max: 75 },
    yAxis: { type: 'value', name: '满意度', min: 2, max: 5 },
    series: [{
      type: 'scatter',
      data: scatterData,
      color: (params: any) => params.data[2] === '老年游客' ? '#67C23A' : '#409EFF',
      symbolSize: 10
    }]
  })

  // 停留时长分布直方图
  const duration = echarts.init(durationChart.value)
  duration.setOption({
    xAxis: {
      type: 'category',
      data: ['0-1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h', '>6h']
    },
    yAxis: { type: 'value', name: '游客数' },
    series: [{
      type: 'bar',
      data: [1520, 8500, 18540, 22100, 16800, 9200, 3900],
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#409EFF' },
          { offset: 1, color: '#79bbff' }
        ])
      }
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
.mr-4 {
  margin-right: 4px;
}
.mt-20 {
  margin-top: 20px;
}
</style>
