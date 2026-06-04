<template>
  <div class="conversation-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>对话管理</span>
          <el-button type="primary">导出记录</el-button>
        </div>
      </template>
      <el-table :data="conversations" style="width: 100%">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="content" label="对话内容" />
        <el-table-column prop="sentiment" label="情感" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.sentiment === '积极' ? 'success' : 'warning'">
              {{ scope.row.sentiment }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button link type="primary">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const conversations = ref([
  { time: '2024-05-20 14:20:00', user: 'User_827', content: '九龙灌浴表演时间是什么时候？', sentiment: '积极' },
  { time: '2024-05-20 14:18:00', user: 'User_156', content: '怎么去灵山大佛？', sentiment: '积极' },
  { time: '2024-05-20 14:15:00', user: 'User_334', content: '梵宫现在人多吗？', sentiment: '中性' }
])
</script>
