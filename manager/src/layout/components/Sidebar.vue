<template>
  <div class="sidebar-wrapper">
    <div class="logo">
      <span>AI 景区向导管理后台</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      router
    >
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <span>数据总览</span>
      </el-menu-item>
      <el-menu-item index="/conversation">
        <el-icon><ChatLineRound /></el-icon>
        <span>对话管理</span>
      </el-menu-item>
      <el-menu-item index="/knowledge">
        <el-icon><Reading /></el-icon>
        <span>知识库管理</span>
      </el-menu-item>
      <el-menu-item index="/avatar">
        <el-icon><User /></el-icon>
        <span>数字人管理</span>
      </el-menu-item>
      <el-menu-item index="/sentiment">
        <el-icon><PieChart /></el-icon>
        <span>游客感受度</span>
      </el-menu-item>
      <el-menu-item index="/insight">
        <el-icon><DataAnalysis /></el-icon>
        <span>游客洞察</span>
      </el-menu-item>
      <el-menu-item index="/route-analysis">
        <el-icon><Guide /></el-icon>
        <span>路线效果分析</span>
      </el-menu-item>
      <el-menu-item index="/data-screen">
        <el-icon><Monitor /></el-icon>
        <span>数据大屏</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeMenu = computed(() => {
  return route.path
})
</script>

<style scoped lang="scss">
.sidebar-wrapper {
  height: 100%;
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 10px;
    font-weight: bold;
    font-size: 16px;
    border-bottom: 1px solid #1f2d3d;
    white-space: nowrap;
    overflow: hidden;
  }
  .el-menu {
    border-right: none;
  }
}
</style>
