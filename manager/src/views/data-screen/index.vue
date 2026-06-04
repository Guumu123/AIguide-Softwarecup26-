<template>
  <div class="data-screen">
    <div class="header">
      <div class="header-left">
        <span class="time">{{ currentTime }}</span>
      </div>
      <div class="header-center">
        <h1>AI 景区向导实时数据监控大屏</h1>
      </div>
      <div class="header-right">
        <el-button type="primary" link @click="router.back()">退出大屏</el-button>
      </div>
    </div>

    <div class="content">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="card chart-box">
            <div class="card-title">今日服务人次</div>
            <div class="stat-value">2,840</div>
            <div ref="serviceChart" style="height: 200px;"></div>
          </div>
          <div class="card chart-box mt-20">
            <div class="card-title">热门问答 TOP 10</div>
            <div class="list-container">
              <div v-for="(item, index) in hotQA" :key="index" class="list-item">
                <span class="rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
                <span class="text">{{ item.question }}</span>
                <span class="count">{{ item.count }}</span>
              </div>
            </div>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="card map-box">
            <div class="card-title">实时情感波动</div>
            <div ref="realtimeSentimentChart" style="height: 500px;"></div>
          </div>
          <el-row :gutter="20" class="mt-20">
            <el-col :span="12">
              <div class="card chart-box">
                <div class="card-title">游客画像</div>
                <div ref="portraitChart" style="height: 250px;"></div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="card chart-box">
                <div class="card-title">游客来源地</div>
                <div ref="sourceChart" style="height: 250px;"></div>
              </div>
            </el-col>
          </el-row>
        </el-col>

        <el-col :span="6">
          <div class="card chart-box">
            <div class="card-title">游客满意度趋势</div>
            <div ref="satisfactionChart" style="height: 250px;"></div>
          </div>
          <div class="card chart-box mt-20">
            <div class="card-title">实时交互日志</div>
            <div class="log-container">
              <div v-for="(log, index) in logs" :key="index" class="log-item">
                <span class="log-time">{{ log.time }}</span>
                <span class="log-text">{{ log.text }}</span>
                <el-tag size="small" :type="log.type">{{ log.sentiment }}</el-tag>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const currentTime = ref('')
let timer: any = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString()
}

const hotQA = [
  { question: '九龙灌浴表演时间？', count: 156 },
  { question: '怎么去梵宫？', count: 124 },
  { question: '灵山大佛门票多少钱？', count: 98 },
  { question: '哪里有素斋？', count: 85 },
  { question: '怎么租借轮椅？', count: 64 },
  { question: '梵宫几点关门？', count: 52 },
  { question: '有没有行李寄存？', count: 48 },
  { question: '怎么预约讲解？', count: 36 },
  { question: '景区有摆渡车吗？', count: 32 },
  { question: '出口在哪里？', count: 28 }
]

const logs = ref([
  { time: '14:20:01', text: '游客咨询九龙灌浴表演时间', sentiment: '积极', type: 'success' },
  { time: '14:19:55', text: '游客反馈梵宫排队较长', sentiment: '中性', type: 'warning' },
  { time: '14:19:42', text: '游客点赞数字人形象', sentiment: '积极', type: 'success' },
  { time: '14:19:30', text: '游客询问洗手间位置', sentiment: '积极', type: 'success' },
  { time: '14:19:15', text: '游客反馈讲解音量过小', sentiment: '消极', type: 'danger' }
])

const serviceChart = ref()
const realtimeSentimentChart = ref()
const portraitChart = ref()
const sourceChart = ref()
const satisfactionChart = ref()

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)

  // 初始化图表
  const service = echarts.init(serviceChart.value)
  service.setOption({
    grid: { top: 10, bottom: 30, left: 40, right: 10 },
    xAxis: { type: 'category', data: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00'], axisLabel: { color: '#fff' } },
    yAxis: { type: 'value', axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
    series: [{ type: 'bar', data: [200, 500, 800, 1200, 900, 300], itemStyle: { color: '#409EFF' } }]
  })

  const sentiment = echarts.init(realtimeSentimentChart.value)
  sentiment.setOption({
    grid: { top: 40, bottom: 40, left: 50, right: 20 },
    xAxis: { type: 'time', axisLabel: { color: '#fff' } },
    yAxis: { type: 'value', min: 0, max: 100, axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
    series: [{
      name: '情感值',
      type: 'line',
      smooth: true,
      showSymbol: false,
      areaStyle: { color: 'rgba(103, 194, 58, 0.3)' },
      lineStyle: { color: '#67C23A' },
      data: (function () {
        let res = []
        let len = 50
        let now = new Date()
        while (len--) {
          res.push({
            name: now.toString(),
            value: [now.getTime(), Math.round(Math.random() * 20 + 70)]
          })
          now = new Date(now.getTime() - 5000)
        }
        return res
      })()
    }]
  })

  const portrait = echarts.init(portraitChart.value)
  portrait.setOption({
    radar: {
      indicator: [
        { name: '文化兴趣', max: 100 },
        { name: '消费能力', max: 100 },
        { name: '停留时长', max: 100 },
        { name: '互动频率', max: 100 },
        { name: '活跃程度', max: 100 }
      ],
      splitArea: { show: false },
      splitLine: { lineStyle: { color: '#333' } }
    },
    series: [{
      type: 'radar',
      data: [
        { value: [80, 60, 90, 70, 85], name: '当前群体画像', itemStyle: { color: '#E6A23C' } }
      ]
    }]
  })

  const source = echarts.init(sourceChart.value)
  source.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 40, name: '本省', itemStyle: { color: '#409EFF' } },
        { value: 30, name: '邻省', itemStyle: { color: '#67C23A' } },
        { value: 20, name: '远途', itemStyle: { color: '#E6A23C' } },
        { value: 10, name: '海外', itemStyle: { color: '#F56C6C' } }
      ],
      label: { color: '#fff' }
    }]
  })

  const satisfaction = echarts.init(satisfactionChart.value)
  satisfaction.setOption({
    grid: { top: 10, bottom: 30, left: 40, right: 10 },
    xAxis: { type: 'category', data: ['5-14', '5-15', '5-16', '5-17', '5-18', '5-19', '5-20'], axisLabel: { color: '#fff' } },
    yAxis: { type: 'value', min: 4, max: 5, axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
    series: [{ type: 'line', data: [4.5, 4.6, 4.5, 4.7, 4.8, 4.7, 4.9], color: '#409EFF' }]
  })
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped lang="scss">
.data-screen {
  background-color: #030409;
  min-height: 100vh;
  color: #fff;
  padding: 20px;
  box-sizing: border-box;

  .header {
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1a2c4d;
    margin-bottom: 20px;
    h1 {
      margin: 0;
      font-size: 32px;
      letter-spacing: 4px;
      color: #00eaff;
      text-shadow: 0 0 10px #00eaff;
    }
    .time {
      font-size: 18px;
      color: #00eaff;
    }
  }

  .card {
    background: rgba(16, 20, 31, 0.8);
    border: 1px solid #1a2c4d;
    padding: 20px;
    border-radius: 4px;
    position: relative;
    &::before {
      content: '';
      position: absolute;
      top: 0; left: 0; width: 10px; height: 10px;
      border-top: 2px solid #00eaff;
      border-left: 2px solid #00eaff;
    }
    &::after {
      content: '';
      position: absolute;
      top: 0; right: 0; width: 10px; height: 10px;
      border-top: 2px solid #00eaff;
      border-right: 2px solid #00eaff;
    }
    .card-title {
      font-size: 18px;
      color: #00eaff;
      margin-bottom: 20px;
      font-weight: bold;
    }
  }

  .stat-value {
    font-size: 36px;
    font-weight: bold;
    color: #ffeb3b;
    text-align: center;
    margin-bottom: 10px;
  }

  .list-container {
    .list-item {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
      .rank {
        width: 24px;
        height: 24px;
        line-height: 24px;
        text-align: center;
        border-radius: 50%;
        margin-right: 10px;
        font-size: 12px;
        background: #1a2c4d;
      }
      .rank-1 { background: #f56c6c; }
      .rank-2 { background: #e6a23c; }
      .rank-3 { background: #409eff; }
      .text { flex: 1; font-size: 14px; }
      .count { color: #00eaff; }
    }
  }

  .log-container {
    height: 300px;
    overflow-y: auto;
    .log-item {
      margin-bottom: 15px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 10px;
      .log-time { color: #909399; }
      .log-text { flex: 1; }
    }
  }
}
</style>
