<template>
  <div class="conversation-container">
    <!-- 筛选栏 -->
    <el-card class="mb-20">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm"
          />
        </el-form-item>
        <el-form-item label="情感类型">
          <el-select v-model="filterForm.sentiment" placeholder="全部" clearable style="width: 120px">
            <el-option label="积极" value="积极" />
            <el-option label="中性" value="中性" />
            <el-option label="消极" value="消极" />
          </el-select>
        </el-form-item>
        <el-form-item label="语音情感">
          <el-select v-model="filterForm.voiceEmotion" placeholder="全部" clearable style="width: 120px">
            <el-option label="happy" value="happy" />
            <el-option label="sad" value="sad" />
            <el-option label="neutral" value="neutral" />
            <el-option label="angry" value="angry" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 对话表格 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>对话记录</span>
          <div>
            <el-tag type="info" class="mr-10">共 {{ total }} 条</el-tag>
            <el-button type="primary" @click="handleExport">导出记录</el-button>
          </div>
        </div>
      </template>

      <el-table :data="conversations" style="width: 100%" v-loading="loading">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="message" label="用户问题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="response" label="AI 回答" min-width="250" show-overflow-tooltip />
        <el-table-column prop="textSentiment" label="文本情感" width="100">
          <template #default="scope">
            <el-tag :type="sentimentTag(scope.row.textSentiment)" size="small">
              {{ scope.row.textSentiment }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="voiceSentiment" label="语音情感" width="100">
          <template #default="scope">
            <el-tag :type="voiceTag(scope.row.voiceSentiment)" size="small">
              {{ scope.row.voiceSentiment }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="finalEmotion" label="融合情感" width="100">
          <template #default="scope">
            <el-tag :type="emotionTag(scope.row.finalEmotion)" size="small">
              {{ scope.row.finalEmotion }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="viewDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination mt-20">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="对话详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ currentDetail.user }}</el-descriptions-item>
        <el-descriptions-item label="时间">{{ currentDetail.time }}</el-descriptions-item>
        <el-descriptions-item label="文本情感">{{ currentDetail.textSentiment }}</el-descriptions-item>
        <el-descriptions-item label="语音情感">{{ currentDetail.voiceSentiment }}</el-descriptions-item>
        <el-descriptions-item label="融合情感">{{ currentDetail.finalEmotion }}</el-descriptions-item>
        <el-descriptions-item label="置信度">{{ currentDetail.confidence }}</el-descriptions-item>
        <el-descriptions-item label="用户问题" :span="2">{{ currentDetail.message }}</el-descriptions-item>
        <el-descriptions-item label="AI 回答" :span="2">{{ currentDetail.response }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const detailVisible = ref(false)
const currentDetail = ref<any>({})

const filterForm = reactive({
  dateRange: null as any,
  sentiment: '',
  voiceEmotion: ''
})

const conversations = ref([
  {
    time: '2024-05-20 14:20:00', user: 'User_827',
    message: '九龙灌浴表演时间是什么时候？',
    response: '九龙灌浴每天有两场表演：上午10:00和下午15:00，建议提前10分钟占位。',
    textSentiment: '积极', voiceSentiment: 'happy', finalEmotion: 'happy', confidence: 0.92
  },
  {
    time: '2024-05-20 14:18:00', user: 'User_156',
    message: '怎么去灵山大佛？',
    response: '沿景区中轴线直行约500米即到灵山大佛，途中经过百子戏弥勒和降魔壁。',
    textSentiment: '中性', voiceSentiment: 'neutral', finalEmotion: 'neutral', confidence: 0.85
  },
  {
    time: '2024-05-20 14:15:00', user: 'User_334',
    message: '梵宫现在人多吗？',
    response: '梵宫目前游客较多，建议先游览周边景点如五印坛城，稍后再前往梵宫。',
    textSentiment: '消极', voiceSentiment: 'sad', finalEmotion: 'sad', confidence: 0.78
  },
  {
    time: '2024-05-20 14:10:00', user: 'User_098',
    message: '附近有吃饭的地方吗？',
    response: '景区内设有灵山蔬食馆，提供素斋，位于九龙灌浴东侧200米处。',
    textSentiment: '中性', voiceSentiment: 'neutral', finalEmotion: 'neutral', confidence: 0.90
  },
  {
    time: '2024-05-20 14:05:00', user: 'User_762',
    message: '灵山大佛有多高？',
    response: '灵山大佛通高88米，佛体79米，莲花瓣9米。含台基总高101.5米。',
    textSentiment: '积极', voiceSentiment: 'happy', finalEmotion: 'happy', confidence: 0.95
  }
])

const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(1256)

const sentimentTag = (s: string) => {
  const map: Record<string, string> = { '积极': 'success', '中性': 'info', '消极': 'danger' }
  return map[s] || 'info'
}

const voiceTag = (s: string) => {
  const map: Record<string, string> = { 'happy': 'success', 'neutral': 'info', 'sad': 'warning', 'angry': 'danger' }
  return map[s] || 'info'
}

const emotionTag = (s: string) => {
  const map: Record<string, string> = { 'happy': 'success', 'neutral': 'info', 'sad': 'warning' }
  return map[s] || 'info'
}

const handleFilter = () => {
  loading.value = true
  setTimeout(() => { loading.value = false }, 300)
}

const resetFilter = () => {
  filterForm.dateRange = null
  filterForm.sentiment = ''
  filterForm.voiceEmotion = ''
}

const handleExport = () => {
  ElMessage.success('对话记录导出中...')
}

const viewDetail = (row: any) => {
  currentDetail.value = row
  detailVisible.value = true
}

const handleSizeChange = () => {}
const handleCurrentChange = () => {}
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mr-10 {
  margin-right: 10px;
}
.mb-20 {
  margin-bottom: 20px;
}
.mt-20 {
  margin-top: 20px;
}
.pagination {
  display: flex;
  justify-content: flex-end;
}
</style>
