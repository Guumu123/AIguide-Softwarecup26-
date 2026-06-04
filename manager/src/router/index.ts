import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '数据总览', icon: 'Odometer' }
      },
      {
        path: 'conversation',
        name: 'Conversation',
        component: () => import('@/views/conversation/index.vue'),
        meta: { title: '对话管理', icon: 'ChatLineRound' }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        meta: { title: '知识库管理', icon: 'Reading' }
      },
      {
        path: 'avatar',
        name: 'Avatar',
        component: () => import('@/views/avatar/index.vue'),
        meta: { title: '数字人管理', icon: 'User' }
      },
      {
        path: 'sentiment',
        name: 'Sentiment',
        component: () => import('@/views/sentiment/index.vue'),
        meta: { title: '游客感受度', icon: 'PieChart' }
      },
      {
        path: 'insight',
        name: 'Insight',
        component: () => import('@/views/insight/index.vue'),
        meta: { title: '游客洞察', icon: 'DataAnalysis' }
      },
      {
        path: 'route-analysis',
        name: 'RouteAnalysis',
        component: () => import('@/views/route-analysis/index.vue'),
        meta: { title: '路线效果分析', icon: 'Guide' }
      }
    ]
  },
  {
    path: '/data-screen',
    name: 'DataScreen',
    component: () => import('@/views/data-screen/index.vue'),
    meta: { title: '数据大屏' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
