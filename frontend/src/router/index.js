import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { setupRouterGuard } from './guards'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/vue-components/pages/Home.vue'),
    meta: { title: '首页 - 贴吧' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/vue-components/pages/Login.vue'),
    meta: { title: '登录 - 贴吧' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/vue-components/pages/Register.vue'),
    meta: { title: '注册 - 贴吧' }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/vue-components/pages/ForgotPassword.vue'),
    meta: { title: '忘记密码 - 贴吧' }
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('@/vue-components/pages/ResetPassword.vue'),
    meta: { title: '重置密码 - 贴吧' }
  },
  {
    path: '/tiebas',
    name: 'Tiebas',
    component: () => import('@/vue-components/pages/Tiebas.vue'),
    meta: { title: '贴吧列表 - 贴吧' }
  },
  {
    path: '/tiebas/:id',
    name: 'TiebaDetail',
    component: () => import('@/vue-components/pages/TiebaDetail.vue'),
    meta: { title: '贴吧详情 - 贴吧' }
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('@/vue-components/pages/PostDetail.vue'),
    meta: { title: '帖子详情 - 贴吧' }
  },
  {
    path: '/create-post',
    name: 'CreatePost',
    component: () => import('@/vue-components/pages/CreatePost.vue'),
    meta: { title: '发布帖子 - 贴吧' }
  },
  {
    path: '/profile/:id?',
    name: 'Profile',
    component: () => import('@/vue-components/pages/Profile.vue'),
    meta: { title: '个人中心 - 贴吧' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/vue-components/pages/Settings.vue'),
    meta: { title: '设置 - 贴吧' }
  },
  {
    path: '/messages',
    name: 'Messages',
    component: () => import('@/vue-components/pages/Messages.vue'),
    meta: { title: '消息 - 贴吧' }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/vue-components/pages/Search.vue'),
    meta: { title: '搜索 - 贴吧' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/vue-components/pages/NotFoundPage.vue'),
    meta: { title: '页面未找到 - 贴吧' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 设置路由守卫
setupRouterGuard(router)

export default router