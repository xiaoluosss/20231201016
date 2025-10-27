<template>
  <div class="reset-password-page">
    <div class="reset-password-container">
      <div class="reset-password-form">
        <div class="form-header">
          <h2>重置密码</h2>
          <p>请设置您的新密码</p>
        </div>
        
        <el-form 
          :model="form" 
          :rules="rules" 
          ref="resetPasswordForm"
          @submit.prevent="handleSubmit"
        >
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入新密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请确认新密码"
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
              @click="handleSubmit"
              style="width: 100%"
            >
              重置密码
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="password-requirements">
          <h4>密码要求：</h4>
          <ul>
            <li :class="{ 'met': form.password.length >= 6 }">至少6个字符</li>
            <li :class="{ 'met': /[a-z]/.test(form.password) }">包含小写字母</li>
            <li :class="{ 'met': /[A-Z]/.test(form.password) }">包含大写字母</li>
            <li :class="{ 'met': /\d/.test(form.password) }">包含数字</li>
          </ul>
        </div>
      </div>
      
      <div class="reset-password-banner">
        <h3>安全提示</h3>
        <p>为了您的账户安全，请设置一个强密码</p>
        <div class="security-tips">
          <div class="tip-item">
            <i>🔒</i>
            <span>不要使用过于简单的密码</span>
          </div>
          <div class="tip-item">
            <i>🔄</i>
            <span>定期更换密码</span>
          </div>
          <div class="tip-item">
            <i>🚫</i>
            <span>不要与其他网站使用相同密码</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const resetPasswordForm = ref()
const loading = ref(false)

const form = reactive({
  password: '',
  confirmPassword: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' },
    { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, message: '密码必须包含大小写字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ]
}

onMounted(() => {
  // 检查是否有重置令牌
  if (!route.query.token) {
    ElMessage.error('无效的重置链接')
    router.push('/forgot-password')
  }
})

const handleSubmit = async () => {
  if (!resetPasswordForm.value) return
  
  try {
    const valid = await resetPasswordForm.value.validate()
    if (!valid) return
    
    loading.value = true
    
    await userStore.resetPassword(route.query.token, form.password)
    
    ElMessage.success('密码重置成功，请重新登录')
    
    // 2秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    ElMessage.error(error.message || '重置密码失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-password-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.reset-password-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 900px;
  width: 100%;
  overflow: hidden;
}

.reset-password-form {
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

.password-requirements {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.password-requirements h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
}

.password-requirements ul {
  margin: 0;
  padding-left: 20px;
  list-style: none;
}

.password-requirements li {
  color: #999;
  font-size: 12px;
  margin-bottom: 4px;
  position: relative;
}

.password-requirements li::before {
  content: '✗';
  position: absolute;
  left: -20px;
}

.password-requirements li.met {
  color: #52c41a;
}

.password-requirements li.met::before {
  content: '✓';
}

.reset-password-banner {
  background: linear-gradient(135deg, #1890ff 0%, #722ed1 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.reset-password-banner h3 {
  font-size: 28px;
  margin-bottom: 16px;
}

.reset-password-banner p {
  font-size: 16px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.security-tips {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}

.tip-item i {
  font-size: 18px;
}

@media (max-width: 768px) {
  .reset-password-container {
    grid-template-columns: 1fr;
  }
  
  .reset-password-banner {
    display: none;
  }
}
</style>