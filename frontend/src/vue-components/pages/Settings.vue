<template>
  <div class="settings-page">
    <div class="settings-container">
      <div class="settings-header">
        <h1>设置</h1>
      </div>
      
      <div class="settings-content">
        <!-- 侧边栏导航 -->
        <div class="settings-nav">
          <el-menu
            :default-active="activeTab"
            class="settings-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="profile">
              <el-icon><User /></el-icon>
              <span>个人资料</span>
            </el-menu-item>
            <el-menu-item index="account">
              <el-icon><Setting /></el-icon>
              <span>账户设置</span>
            </el-menu-item>
            <el-menu-item index="privacy">
              <el-icon><Lock /></el-icon>
              <span>隐私设置</span>
            </el-menu-item>
            <el-menu-item index="notification">
              <el-icon><Bell /></el-icon>
              <span>通知设置</span>
            </el-menu-item>
            <el-menu-item index="appearance">
              <el-icon><Monitor /></el-icon>
              <span>外观设置</span>
            </el-menu-item>
          </el-menu>
        </div>
        
        <!-- 设置内容区域 -->
        <div class="settings-panel">
          <!-- 个人资料设置 -->
          <div v-if="activeTab === 'profile'" class="tab-content">
            <h2>个人资料设置</h2>
            <el-form :model="profileForm" label-width="120px">
              <el-form-item label="头像">
                <div class="avatar-upload">
                  <el-avatar :size="80" :src="profileForm.avatar" />
                  <el-upload
                    action="/api/upload/avatar/"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :before-upload="beforeAvatarUpload"
                  >
                    <el-button size="small">更换头像</el-button>
                  </el-upload>
                </div>
              </el-form-item>
              
              <el-form-item label="昵称">
                <el-input 
                  v-model="profileForm.nickname" 
                  maxlength="20" 
                  show-word-limit
                  placeholder="请输入昵称"
                />
              </el-form-item>
              
              <el-form-item label="个人简介">
                <el-input
                  v-model="profileForm.bio"
                  type="textarea"
                  :rows="3"
                  maxlength="200"
                  show-word-limit
                  placeholder="介绍一下自己吧~"
                />
              </el-form-item>
              
              <el-form-item label="性别">
                <el-radio-group v-model="profileForm.gender">
                  <el-radio label="male">男</el-radio>
                  <el-radio label="female">女</el-radio>
                  <el-radio label="unknown">保密</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <el-form-item label="生日">
                <el-date-picker
                  v-model="profileForm.birthday"
                  type="date"
                  placeholder="选择生日"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
              
              <el-form-item label="所在地">
                <el-cascader
                  v-model="profileForm.location"
                  :options="locationOptions"
                  placeholder="请选择所在地"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="saveProfile" :loading="saving">
                  保存修改
                </el-button>
              </el-form-item>
            </el-form>
          </div>
          
          <!-- 账户设置 -->
          <div v-if="activeTab === 'account'" class="tab-content">
            <h2>账户设置</h2>
            
            <div class="setting-section">
              <h3>修改密码</h3>
              <el-form :model="passwordForm" label-width="120px" :rules="passwordRules" ref="passwordFormRef">
                <el-form-item label="当前密码" prop="currentPassword">
                  <el-input
                    v-model="passwordForm.currentPassword"
                    type="password"
                    placeholder="请输入当前密码"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item label="新密码" prop="newPassword">
                  <el-input
                    v-model="passwordForm.newPassword"
                    type="password"
                    placeholder="请输入新密码"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item label="确认新密码" prop="confirmPassword">
                  <el-input
                    v-model="passwordForm.confirmPassword"
                    type="password"
                    placeholder="请再次输入新密码"
                    show-password
                  />
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="changePassword" :loading="changingPassword">
                    修改密码
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <div class="setting-section">
              <h3>绑定邮箱</h3>
              <div class="email-setting">
                <div class="current-email">
                  <span>当前邮箱：{{ userStore.user?.email || '未绑定' }}</span>
                  <el-button size="small" @click="showEmailDialog">
                    {{ userStore.user?.email ? '修改' : '绑定' }}
                  </el-button>
                </div>
              </div>
            </div>
            
            <div class="setting-section danger-zone">
              <h3>危险操作</h3>
              <div class="danger-actions">
                <el-button type="danger" @click="showDeleteDialog">
                  注销账户
                </el-button>
                <p class="danger-tip">此操作不可逆，请谨慎操作</p>
              </div>
            </div>
          </div>
          
          <!-- 隐私设置 -->
          <div v-if="activeTab === 'privacy'" class="tab-content">
            <h2>隐私设置</h2>
            
            <div class="setting-section">
              <h3>个人资料可见性</h3>
              <el-form label-width="200px">
                <el-form-item label="谁可以看到我的个人资料">
                  <el-radio-group v-model="privacyForm.profileVisibility">
                    <el-radio label="public">所有人</el-radio>
                    <el-radio label="followers">仅关注我的人</el-radio>
                    <el-radio label="private">仅自己</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="谁可以给我发私信">
                  <el-radio-group v-model="privacyForm.messageVisibility">
                    <el-radio label="public">所有人</el-radio>
                    <el-radio label="followers">仅关注我的人</el-radio>
                    <el-radio label="none">不允许任何人</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-form>
            </div>
            
            <div class="setting-section">
              <h3>内容可见性</h3>
              <el-form label-width="200px">
                <el-form-item label="谁可以看到我的帖子">
                  <el-radio-group v-model="privacyForm.postsVisibility">
                    <el-radio label="public">所有人</el-radio>
                    <el-radio label="followers">仅关注我的人</el-radio>
                    <el-radio label="private">仅自己</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="谁可以看到我的关注/粉丝列表">
                  <el-radio-group v-model="privacyForm.followVisibility">
                    <el-radio label="public">所有人</el-radio>
                    <el-radio label="followers">仅关注我的人</el-radio>
                    <el-radio label="private">仅自己</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-form>
            </div>
            
            <div class="setting-section">
              <el-button type="primary" @click="savePrivacySettings">
                保存隐私设置
              </el-button>
            </div>
          </div>
          
          <!-- 通知设置 -->
          <div v-if="activeTab === 'notification'" class="tab-content">
            <h2>通知设置</h2>
            
            <div class="setting-section">
              <h3>推送通知</h3>
              <el-form label-width="200px">
                <el-form-item label="新粉丝通知">
                  <el-switch v-model="notificationForm.newFollower" />
                </el-form-item>
                
                <el-form-item label="帖子被点赞通知">
                  <el-switch v-model="notificationForm.postLiked" />
                </el-form-item>
                
                <el-form-item label="帖子被评论通知">
                  <el-switch v-model="notificationForm.postCommented" />
                </el-form-item>
                
                <el-form-item label="评论被回复通知">
                  <el-switch v-model="notificationForm.commentReplied" />
                </el-form-item>
                
                <el-form-item label="系统消息通知">
                  <el-switch v-model="notificationForm.systemMessage" />
                </el-form-item>
              </el-form>
            </div>
            
            <div class="setting-section">
              <h3>邮件通知</h3>
              <el-form label-width="200px">
                <el-form-item label="重要通知邮件">
                  <el-switch v-model="notificationForm.emailImportant" />
                </el-form-item>
                
                <el-form-item label="营销邮件">
                  <el-switch v-model="notificationForm.emailMarketing" />
                </el-form-item>
              </el-form>
            </div>
            
            <div class="setting-section">
              <el-button type="primary" @click="saveNotificationSettings">
                保存通知设置
              </el-button>
            </div>
          </div>
          
          <!-- 外观设置 -->
          <div v-if="activeTab === 'appearance'" class="tab-content">
            <h2>外观设置</h2>
            
            <div class="setting-section">
              <h3>主题模式</h3>
              <div class="theme-options">
                <div 
                  class="theme-option"
                  :class="{ active: appearanceForm.theme === 'light' }"
                  @click="appearanceForm.theme = 'light'"
                >
                  <div class="theme-preview light"></div>
                  <span>浅色模式</span>
                </div>
                
                <div 
                  class="theme-option"
                  :class="{ active: appearanceForm.theme === 'dark' }"
                  @click="appearanceForm.theme = 'dark'"
                >
                  <div class="theme-preview dark"></div>
                  <span>深色模式</span>
                </div>
                
                <div 
                  class="theme-option"
                  :class="{ active: appearanceForm.theme === 'auto' }"
                  @click="appearanceForm.theme = 'auto'"
                >
                  <div class="theme-preview auto"></div>
                  <span>跟随系统</span>
                </div>
              </div>
            </div>
            
            <div class="setting-section">
              <h3>字体大小</h3>
              <el-slider
                v-model="appearanceForm.fontSize"
                :min="12"
                :max="18"
                :step="1"
                show-stops
              />
              <div class="font-size-preview">
                <span :style="{ fontSize: appearanceForm.fontSize + 'px' }">
                  这是一段预览文字
                </span>
              </div>
            </div>
            
            <div class="setting-section">
              <el-button type="primary" @click="saveAppearanceSettings">
                保存外观设置
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 邮箱绑定对话框 -->
    <el-dialog v-model="emailDialogVisible" title="绑定邮箱" width="400px">
      <el-form :model="emailForm" label-width="80px">
        <el-form-item label="邮箱地址">
          <el-input v-model="emailForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="验证码">
          <div class="verification-code">
            <el-input v-model="emailForm.code" placeholder="请输入验证码" />
            <el-button type="primary" @click="sendVerificationCode" :disabled="codeCountdown > 0">
              {{ codeCountdown > 0 ? `${codeCountdown}s后重发` : '发送验证码' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="emailDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="bindEmail" :loading="bindingEmail">
          确认绑定
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 注销账户确认对话框 -->
    <el-dialog v-model="deleteDialogVisible" title="确认注销账户" width="400px">
      <p>此操作将永久删除您的账户和所有数据，且无法恢复。请确认您要执行此操作。</p>
      <el-input v-model="deleteConfirm" placeholder="请输入"DELETE"以确认" />
      
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button 
          type="danger" 
          @click="confirmDeleteAccount" 
          :disabled="deleteConfirm !== 'DELETE'"
        >
          确认注销
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { User, Setting, Lock, Bell, Monitor } from '@element-plus/icons-vue'
import api from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('profile')
const saving = ref(false)
const changingPassword = ref(false)
const bindingEmail = ref(false)
const emailDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const codeCountdown = ref(0)
const deleteConfirm = ref('')

// 表单数据
const profileForm = reactive({
  avatar: '',
  nickname: '',
  bio: '',
  gender: 'unknown',
  birthday: '',
  location: []
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const privacyForm = reactive({
  profileVisibility: 'public',
  messageVisibility: 'public',
  postsVisibility: 'public',
  followVisibility: 'public'
})

const notificationForm = reactive({
  newFollower: true,
  postLiked: true,
  postCommented: true,
  commentReplied: true,
  systemMessage: true,
  emailImportant: true,
  emailMarketing: false
})

const appearanceForm = reactive({
  theme: 'light',
  fontSize: 14
})

const emailForm = reactive({
  email: '',
  code: ''
})

// 密码验证规则
const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 地区选项（简化版）
const locationOptions = [
  {
    value: 'beijing',
    label: '北京市',
    children: [
      { value: 'dongcheng', label: '东城区' },
      { value: 'xicheng', label: '西城区' }
    ]
  },
  {
    value: 'shanghai',
    label: '上海市',
    children: [
      { value: 'huangpu', label: '黄浦区' },
      { value: 'xuhui', label: '徐汇区' }
    ]
  }
]

// 菜单选择
const handleMenuSelect = (index) => {
  activeTab.value = index
}

// 头像上传成功
const handleAvatarSuccess = (response) => {
  profileForm.avatar = response.url
  ElMessage.success('头像上传成功')
}

// 头像上传前验证
const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像只能是 JPG/PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}

// 保存个人资料
const saveProfile = async () => {
  try {
    saving.value = true
    await api.put('/users/profile/', profileForm)
    
    // 更新store中的用户信息
    userStore.updateUserInfo(profileForm)
    
    ElMessage.success('个人资料更新成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('个人资料更新失败')
  } finally {
    saving.value = false
  }
}

// 修改密码
const changePassword = async () => {
  try {
    changingPassword.value = true
    await api.post('/users/change-password/', passwordForm)
    
    ElMessage.success('密码修改成功')
    
    // 清空表单
    Object.keys(passwordForm).forEach(key => {
      passwordForm[key] = ''
    })
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error('密码修改失败')
  } finally {
    changingPassword.value = false
  }
}

// 显示邮箱绑定对话框
const showEmailDialog = () => {
  emailForm.email = userStore.user?.email || ''
  emailDialogVisible.value = true
}

// 发送验证码
const sendVerificationCode = async () => {
  if (!emailForm.email) {
    ElMessage.warning('请输入邮箱地址')
    return
  }
  
  try {
    await api.post('/users/send-verification-code/', { email: emailForm.email })
    ElMessage.success('验证码已发送')
    
    // 开始倒计时
    codeCountdown.value = 60
    const timer = setInterval(() => {
      codeCountdown.value--
      if (codeCountdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    console.error('发送验证码失败:', error)
    ElMessage.error('验证码发送失败')
  }
}

// 绑定邮箱
const bindEmail = async () => {
  if (!emailForm.email || !emailForm.code) {
    ElMessage.warning('请填写邮箱和验证码')
    return
  }
  
  try {
    bindingEmail.value = true
    await api.post('/users/bind-email/', emailForm)
    
    ElMessage.success('邮箱绑定成功')
    emailDialogVisible.value = false
    
    // 更新用户信息
    userStore.updateUserInfo({ email: emailForm.email })
  } catch (error) {
    console.error('绑定邮箱失败:', error)
    ElMessage.error('邮箱绑定失败')
  } finally {
    bindingEmail.value = false
  }
}

// 保存隐私设置
const savePrivacySettings = async () => {
  try {
    await api.post('/users/privacy-settings/', privacyForm)
    ElMessage.success('隐私设置已保存')
  } catch (error) {
    console.error('保存隐私设置失败:', error)
    ElMessage.error('保存失败')
  }
}

// 保存通知设置
const saveNotificationSettings = async () => {
  try {
    await api.post('/users/notification-settings/', notificationForm)
    ElMessage.success('通知设置已保存')
  } catch (error) {
    console.error('保存通知设置失败:', error)
    ElMessage.error('保存失败')
  }
}

// 保存外观设置
const saveAppearanceSettings = async () => {
  try {
    await api.post('/users/appearance-settings/', appearanceForm)
    ElMessage.success('外观设置已保存')
    
    // 应用主题设置
    applyTheme(appearanceForm.theme)
  } catch (error) {
    console.error('保存外观设置失败:', error)
    ElMessage.error('保存失败')
  }
}

// 应用主题
const applyTheme = (theme) => {
  const html = document.documentElement
  html.classList.remove('light-theme', 'dark-theme')
  
  if (theme === 'dark') {
    html.classList.add('dark-theme')
  } else if (theme === 'light') {
    html.classList.add('light-theme')
  }
  // auto模式由系统决定
}

// 显示注销确认对话框
const showDeleteDialog = () => {
  deleteDialogVisible.value = true
  deleteConfirm.value = ''
}

// 确认注销账户
const confirmDeleteAccount = async () => {
  try {
    await api.delete('/users/delete-account/')
    ElMessage.success('账户已注销')
    
    // 退出登录
    userStore.logout()
    router.push('/')
  } catch (error) {
    console.error('注销账户失败:', error)
    ElMessage.error('注销失败')
  } finally {
    deleteDialogVisible.value = false
  }
}

// 加载用户设置
const loadUserSettings = async () => {
  try {
    const response = await api.get('/users/settings/')
    const settings = response.data
    
    // 填充表单数据
    Object.assign(profileForm, settings.profile || {})
    Object.assign(privacyForm, settings.privacy || {})
    Object.assign(notificationForm, settings.notification || {})
    Object.assign(appearanceForm, settings.appearance || {})
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

onMounted(() => {
  // 检查用户是否登录
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  // 初始化用户数据
  const user = userStore.user
  if (user) {
    profileForm.avatar = user.avatar || ''
    profileForm.nickname = user.nickname || ''
    profileForm.bio = user.bio || ''
  }
  
  loadUserSettings()
})
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px 0;
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.settings-header {
  padding: 20px 30px;
  border-bottom: 1px solid #f0f0f0;
}

.settings-header h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.settings-content {
  display: flex;
  min-height: 600px;
}

.settings-nav {
  width: 240px;
  border-right: 1px solid #f0f0f0;
}

.settings-menu {
  border: none;
}

.settings-panel {
  flex: 1;
  padding: 30px;
}

.tab-content h2 {
  margin: 0 0 24px 0;
  color: #333;
  font-size: 20px;
}

.setting-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.setting-section:last-child {
  border-bottom: none;
}

.setting-section h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 16px;
}

.verification-code {
  display: flex;
  gap: 8px;
}

.current-email {
  display: flex;
  align-items: center;
  gap: 12px;
}

.danger-zone {
  border-color: #ff4d4f;
}

.danger-actions {
  text-align: center;
}

.danger-tip {
  margin-top: 8px;
  color: #ff4d4f;
  font-size: 12px;
}

.theme-options {
  display: flex;
  gap: 16px;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border: 2px solid #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.theme-option:hover {
  border-color: #1890ff;
}

.theme-option.active {
  border-color: #1890ff;
  background: #f0f8ff;
}

.theme-preview {
  width: 60px;
  height: 40px;
  border-radius: 4px;
}

.theme-preview.light {
  background: #ffffff;
  border: 1px solid #f0f0f0;
}

.theme-preview.dark {
  background: #1f1f1f;
  border: 1px solid #333;
}

.theme-preview.auto {
  background: linear-gradient(45deg, #ffffff 50%, #1f1f1f 50%);
  border: 1px solid #f0f0f0;
}

.font-size-preview {
  margin-top: 12px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-content {
    flex-direction: column;
  }
  
  .settings-nav {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .settings-panel {
    padding: 20px;
  }
  
  .theme-options {
    flex-direction: column;
  }
}
</style>