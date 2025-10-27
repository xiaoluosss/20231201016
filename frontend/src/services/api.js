import axios from 'axios'
import { ElMessage } from 'element-plus'
import authService from './auth'

// 创建axios实例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 是否正在刷新token
let isRefreshing = false
// 重试队列
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  
  failedQueue = []
}

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加认证token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    if (error.response) {
      const { status, data } = error.response
      
      // 处理401错误（token过期）
      if (status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          // 如果正在刷新token，将请求加入队列
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          }).then(token => {
            originalRequest.headers.Authorization = 'Bearer ' + token
            return api(originalRequest)
          }).catch(err => {
            return Promise.reject(err)
          })
        }
        
        originalRequest._retry = true
        isRefreshing = true
        
        try {
          // 尝试刷新token
          const newToken = await authService.refreshToken()
          
          // 更新Authorization头
          api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
          
          // 处理队列中的请求
          processQueue(null, newToken)
          
          // 重试原始请求
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return api(originalRequest)
        } catch (refreshError) {
          // 刷新token失败，清除认证信息并跳转到登录页
          processQueue(refreshError, null)
          authService.logout()
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }
      
      // 处理其他错误
      switch (status) {
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          // 表单验证错误
          if (data.errors) {
            const errorMessages = Object.values(data.errors).flat().join(', ')
            ElMessage.error(errorMessages)
          } else {
            ElMessage.error(data.message || '数据验证失败')
          }
          break
        case 429:
          ElMessage.error('请求过于频繁，请稍后再试')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        case 502:
          ElMessage.error('网关错误')
          break
        case 503:
          ElMessage.error('服务暂时不可用')
          break
        default:
          ElMessage.error(data?.message || `请求失败 (${status})`)
      }
    } else {
      // 网络错误
      ElMessage.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

// 初始化认证状态
authService.init()

export default api