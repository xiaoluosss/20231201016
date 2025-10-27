<template>
  <div class="forgot-password-page">
    <div class="forgot-password-container">
      <div class="forgot-password-form">
        <div class="form-header">
          <h2>忘记密码</h2>
          <p>请输入您的邮箱地址，我们将发送重置密码的链接</p>
        </div>
        
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="forgotPasswordForm"
          @submit.prevent="handleSubmit"
        >
          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入注册时使用的邮箱"
              size="large"
              prefix-icon="Message"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              :loading="loading" 
              @click="handleSubmit"
              style="width: 100%"
            >
              发送重置链接
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="form-footer">
          <p>想起密码了？<router-link to="/login">返回登录</router-link></p>
        </div>
      </div>
      
      <div class="forgot-password-banner">
        <h3>重置密码</h3>
        <p>通过邮箱安全重置您的账户密码</p>
        <div class="steps">
          <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>输入邮箱</h4>
              <p>输入您注册时使用的邮箱地址</p>
            </div>
          </div>
          <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>接收邮件</h4>
              <p>查收我们发送的重置密码邮件</p>
            </div>
          </div>
          <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>重置密码</h4>
              <p>点击邮件中的链接设置新密码</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const forgotPasswordForm = ref()
const loading = ref(false)

const form = reactive({
  email: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!forgotPasswordForm.value) return
  
  try {
    const valid = await forgotPasswordForm.value.validate()
    if (!valid) return
    
    loading.value = true
    
    await userStore.forgotPassword(form.email)
    
    ElMessage.success('重置密码链接已发送到您的邮箱，请查收')
    
    // 3秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (error) {
    ElMessage.error(error.message || '发送重置链接失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.forgot-password-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.forgot-password-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 900px;
  width: 100%;
  overflow: hidden;
}

.forgot-password-form {
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

.forgot-password-banner {
  background: linear-gradient(135deg, #1890ff 0%, #722ed1 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.forgot-password-banner h3 {
  font-size: 28px;
  margin-bottom: 16px;
}

.forgot-password-banner p {
  font-size: 16px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-number {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 16px;
  margin-bottom: 4px;
  font-weight: 600;
}

.step-content p {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .forgot-password-container {
    grid-template-columns: 1fr;
  }
  
  .forgot-password-banner {
    display: none;
  }
}
</style>