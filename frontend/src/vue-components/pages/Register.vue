<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-form">
        <div class="form-header">
          <h2>注册百度贴吧</h2>
          <p>创建您的账户，开始探索兴趣社区</p>
        </div>
        
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="registerForm"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱"
              size="large"
              prefix-icon="Message"
            />
          </el-form-item>
          
          <el-form-item prop="nickname">
            <el-input
              v-model="form.nickname"
              placeholder="请输入昵称"
              size="large"
              prefix-icon="Edit"
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
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请确认密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-checkbox v-model="form.agreeTerms">
              我已阅读并同意 <a href="#" class="terms-link">服务条款</a> 和 <a href="#" class="terms-link">隐私政策</a>
            </el-checkbox>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              :loading="loading" 
              @click="handleRegister"
              style="width: 100%"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="form-footer">
          <p>已有账户？<router-link to="/login">立即登录</router-link></p>
        </div>
      </div>
      
      <div class="register-banner">
        <h3>加入我们，发现更多</h3>
        <p>成为百度贴吧的一员，开启精彩的社区之旅</p>
        <div class="benefits">
          <div class="benefit-item">
            <div class="benefit-icon">🎯</div>
            <div class="benefit-content">
              <h4>精准兴趣推荐</h4>
              <p>根据您的兴趣智能推荐相关贴吧</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">🤝</div>
            <div class="benefit-content">
              <h4>结识志同道合的朋友</h4>
              <p>在兴趣社区中认识更多有趣的人</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">📈</div>
            <div class="benefit-content">
              <h4>内容创作与分享</h4>
              <p>发布帖子，分享见解，获得认可</p>
            </div>
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

const registerForm = ref()
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  nickname: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const validateTerms = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请同意服务条款和隐私政策'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 30, message: '昵称长度在 2 到 30 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  agreeTerms: [
    { validator: validateTerms, trigger: 'change' }
  ]
}

const handleRegister = async () => {
  if (!registerForm.value) return
  
  try {
    const valid = await registerForm.value.validate()
    if (!valid) return
    
    loading.value = true
    
    const registerData = {
      username: form.value.username,
      email: form.value.email,
      nickname: form.value.nickname,
      password: form.value.password
    }
    
    await userStore.register(registerData)
    
    ElMessage.success('注册成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  overflow: hidden;
}

.register-form {
  padding: 40px;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
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

.terms-link {
  color: #1890ff;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
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

.register-banner {
  background: linear-gradient(135deg, #52c41a 0%, #1890ff 100%);
  color: white;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.register-banner h3 {
  font-size: 28px;
  margin-bottom: 16px;
}

.register-banner p {
  font-size: 16px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.benefits {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.benefit-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.benefit-content h4 {
  font-size: 18px;
  margin-bottom: 8px;
  font-weight: 600;
}

.benefit-content p {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .register-container {
    grid-template-columns: 1fr;
  }
  
  .register-banner {
    display: none;
  }
}
</style>