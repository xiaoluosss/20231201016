import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth'
import api from '@/services/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isLoggedIn = computed(() => authService.isLoggedIn())
  const isLoading = ref(false)

  // 登录
  const login = async (credentials) => {
    try {
      isLoading.value = true
      const result = await authService.login(credentials)
      
      if (result.user) {
        user.value = result.user
        token.value = result.token
        authService.setUserInfo(result.user)
      }
      
      return result
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const register = async (userData) => {
    try {
      isLoading.value = true
      const result = await authService.register(userData)
      
      // 如果注册后自动登录
      if (result.token && result.user) {
        user.value = result.user
        token.value = result.token
        authService.setUserInfo(result.user)
      }
      
      return result
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = () => {
    authService.logout()
    user.value = null
    token.value = ''
  }

  // 更新用户信息
  const updateUserInfo = (updates) => {
    const updatedUser = authService.updateUserInfo(updates)
    if (updatedUser) {
      user.value = updatedUser
    }
    return updatedUser
  }

  // 检查权限
  const hasPermission = (permission) => {
    return authService.hasPermission(permission)
  }

  // 检查角色
  const hasRole = (role) => {
    return authService.hasRole(role)
  }

  // 获取当前用户信息
  const getCurrentUser = () => {
    return authService.getCurrentUser()
  }

  // 刷新用户信息
  const refreshUserInfo = async () => {
    try {
      const response = await api.get('/users/profile/')
      if (response.data) {
        user.value = response.data
        authService.setUserInfo(response.data)
      }
    } catch (error) {
      console.error('Failed to refresh user info:', error)
    }
  }

  // 获取验证码
  const getCaptcha = async (email) => {
    try {
      const response = await api.post('/auth/captcha', { email })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '获取验证码失败')
    }
  }

  // 忘记密码
  const forgotPassword = async (email) => {
    try {
      const response = await api.post('/auth/forgot-password', { email })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '发送重置邮件失败')
    }
  }

  // 重置密码
  const resetPassword = async (token, password) => {
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
  const verifyEmail = async (token) => {
    try {
      const response = await api.post('/auth/verify-email', { token })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || '邮箱验证失败')
    }
  }

  // 初始化用户状态
  const init = () => {
    const currentUser = authService.getCurrentUser()
    if (currentUser) {
      user.value = currentUser
    }
    
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      token.value = savedToken
    }
  }

  // 立即初始化
  init()

  return {
    user,
    token,
    isLoggedIn,
    isLoading,
    login,
    register,
    logout,
    updateUserInfo,
    hasPermission,
    hasRole,
    getCurrentUser,
    refreshUserInfo,
    forgotPassword,
    resetPassword,
    verifyEmail
  }
})