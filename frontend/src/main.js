import { createAppWithReact } from 'veaury'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import routes from './router'
import './styles/index.css'

// 创建 Pinia 状态管理
const pinia = createPinia()

// 创建 Vue Router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 创建 Veaury 混合应用
const app = createAppWithReact({
  rootComponent: App,
  vueOptions: {
    plugins: [pinia, router]
  },
  reactOptions: {
    // React 全局配置
  }
})

// 挂载应用
app.mount('#app')