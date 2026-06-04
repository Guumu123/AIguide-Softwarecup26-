<template>
  <div class="navbar">
    <div class="breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ route.meta.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="right-menu">
      <el-dropdown trigger="click">
        <div class="avatar-wrapper">
          <el-avatar :size="32" icon="UserFilled" />
          <span class="username">管理员</span>
          <el-icon><CaretBottom /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped lang="scss">
.navbar {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .avatar-wrapper {
    display: flex;
    align-items: center;
    cursor: pointer;
    .username {
      margin: 0 8px;
    }
  }
}
</style>
