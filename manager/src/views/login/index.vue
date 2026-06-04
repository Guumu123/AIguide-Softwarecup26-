<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="header">
          <h2>AI 景区向导管理系统</h2>
        </div>
      </template>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" class="login-button" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate((valid: boolean) => {
    if (valid) {
      loading.value = true
      // 模拟登录
      setTimeout(() => {
        if (loginForm.username === 'admin' && loginForm.password === 'admin123') {
          localStorage.setItem('token', 'fake-jwt-token')
          ElMessage.success('登录成功')
          router.push('/')
        } else {
          ElMessage.error('用户名或密码错误')
        }
        loading.value = false
      }, 1000)
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2d3a4b;
  .login-card {
    width: 400px;
    .header {
      text-align: center;
      h2 {
        margin: 0;
        color: #333;
      }
    }
    .login-button {
      width: 100%;
    }
  }
}
</style>
