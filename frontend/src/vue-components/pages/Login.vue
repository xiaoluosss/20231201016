<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-form">
        <div class="form-header">
          <h2>登录百度贴吧</h2>
          <p>欢迎回来，请登录您的账户</p>
        </div>
        
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="loginForm"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名或邮箱"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              :loading="loading" 
              @click="handleLogin"
              style="width: 100%"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="form-footer">
          <p>还没有账户？<router-link to="/register">立即注册</router-link></p>
        </div>
      </div>
      
      <div class="login-banner">
        <h3>加入百度贴吧</h3>
        <p>发现兴趣圈子，结交志同道合的朋友</p>
        <div class="features">
          <div class="feature-item">
            <i>👥</i>
            <span>海量兴趣社区</span>
          </div>
          <div class="feature-item">
            <i>💬</i>
            <span>实时交流互动</span>
          </div>
          <div class="feature-item">
            <i>📱</i>
            <span>多平台支持</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const loginForm = ref()
const loading = ref(false)

const form = ref({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginForm.value) return
  
  try {
    const valid = await loginForm.value.validate()
    if (!valid) return
    
    loading.value = true
    await userStore.login(form.value)
    
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 900px;
  width: 100%;
  overflow: hidden;
}

.login-form {
  padding: 60px 40px;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-header h2 {
  color: #333;
  margin-bottom: 8px;
  font-size: 28px;
}

.form-header p {
  color: #666;
  font-size: 14px;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
}

.form-footer a {
  color: #1890ff;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

.login-banner {
  background: linear-gradient(135deg, #1890ff 0%, #722ed1 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-banner h3 {
  font-size: 28px;
  margin-bottom: 16px;
}

.login-banner p {
  font-size: 16px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
}

.feature-item i {
  font-size: 20px;
}

@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  
  .login-banner {
    display: none;
  }
}
</style>