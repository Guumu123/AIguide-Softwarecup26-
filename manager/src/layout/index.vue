<template>
  <el-container class="layout-container">
    <el-aside width="240px">
      <sidebar />
    </el-aside>
    <el-container>
      <el-header>
        <navbar />
      </el-header>
      <el-main>
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  .el-aside {
    background-color: #304156;
    color: #fff;
  }
  .el-header {
    background-color: #fff;
    border-bottom: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    padding: 0 20px;
  }
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}

/* fade-transform */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.5s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
