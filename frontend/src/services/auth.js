import api from './api'
import { ElMessage } from 'element-plus'

class AuthService {
  // 用户登录
  async login(credentials) {
    try {
      const response = await api.post('/auth/login/', credentials)
      
      if (response.data.token) {
        // 保存token到localStorage
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('refreshToken', response.data.refreshToken)
        
        // 设置默认Authorization头
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
        
        return response.data
      }
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }
  
  // 用户注册
  async register(userData) {
    try {
      const response = await api.post('/auth/register/', userData)
      return response.data
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }
  
  // 用户登出
  logout() {
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
    
    // 清除API头
    delete api.defaults.headers.common['Authorization']
    
    // 重定向到登录页
    window.location.href = '/login'
  }
  
  // 刷新token
  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }
      
      const response = await api.post('/auth/refresh/', {
        refreshToken: refreshToken
      })
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token)
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
        return response.data.token
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      this.logout()
      throw error
    }
  }
  
  // 检查用户是否已登录
  isLoggedIn() {
    const token = localStorage.getItem('token')
    if (!token) return false
    
    // 检查token是否过期
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp > Date.now() / 1000
    } catch (error) {
      return false
    }
  }
  
  // 获取当前用户信息
  getCurrentUser() {
    const userInfo = localStorage.getItem('userInfo')
    return userInfo ? JSON.parse(userInfo) : null
  }
  
  // 保存用户信息
  setUserInfo(userInfo) {
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  }
  
  // 更新用户信息
  updateUserInfo(updates) {
    const currentUser = this.getCurrentUser()
    if (currentUser) {
      const updatedUser = { ...currentUser, ...updates }
      this.setUserInfo(updatedUser)
      return updatedUser
    }
    return null
  }
  
  // 检查权限
  hasPermission(permission) {
    const user = this.getCurrentUser()
    if (!user) return false
    
    // 管理员拥有所有权限
    if (user.role === 'admin') return true
    
    // 检查用户权限
    return user.permissions && user.permissions.includes(permission)
  }
  
  // 检查角色
  hasRole(role) {
    const user = this.getCurrentUser()
    return user && user.role === role
  }
  
  // 获取验证码
  async getCaptcha(email) {
    try {
      const response = await api.post('/auth/captcha', { email })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '获取验证码失败')
    }
  }

  // 忘记密码
  async forgotPassword(email) {
    try {
      const response = await api.post('/auth/forgot-password', { email })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '发送重置邮件失败')
    }
  }

  // 重置密码
  async resetPassword(token, password) {
    try {
      const response = await api.post('/auth/reset-password', { 
        token, 
        password 
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '重置密码失败')
    }
  }

  // 验证邮箱
  async verifyEmail(token) {
    try {
      const response = await api.post('/auth/verify-email', { token })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '邮箱验证失败')
    }
  }

  // 刷新用户信息
  async refreshUserInfo() {
    try {
      const response = await api.get('/user/profile')
      const userInfo = response.data
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
      return userInfo
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      throw error
    }
  }
  
  // 初始化认证状态
  init() {
    const token = localStorage.getItem('token')
    if (token && this.isLoggedIn()) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      this.logout()
    }
  }
}

// 创建单例实例
export default new AuthService()