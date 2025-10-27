<template>
  <div class="create-post-page">
    <div class="create-post-container">
      <div class="header">
        <h1>发布新帖子</h1>
        <el-button @click="$router.back()">返回</el-button>
      </div>
      
      <div class="post-form">
        <!-- 选择贴吧 -->
        <div class="form-section">
          <label class="form-label">选择贴吧</label>
          <el-select 
            v-model="form.tieba_id" 
            placeholder="请选择贴吧"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="tieba in tiebas"
              :key="tieba.id"
              :label="tieba.name"
              :value="tieba.id"
            >
              <div class="tieba-option">
                <el-avatar :size="30" :src="tieba.avatar" />
                <span>{{ tieba.name }}</span>
                <span class="member-count">{{ tieba.member_count }} 成员</span>
              </div>
            </el-option>
          </el-select>
        </div>
        
        <!-- 帖子标题 -->
        <div class="form-section">
          <label class="form-label">帖子标题</label>
          <el-input
            v-model="form.title"
            placeholder="请输入帖子标题"
            maxlength="100"
            show-word-limit
          />
        </div>
        
        <!-- 帖子内容 -->
        <div class="form-section">
          <label class="form-label">帖子内容</label>
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="8"
            placeholder="请输入帖子内容..."
            maxlength="5000"
            show-word-limit
            resize="none"
          />
        </div>
        
        <!-- 图片上传 -->
        <div class="form-section">
          <label class="form-label">上传图片</label>
          <div class="upload-section">
            <el-upload
              v-model:file-list="imageList"
              action="/api/upload/image/"
              list-type="picture-card"
              :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeUpload"
              accept="image/*"
              :limit="9"
              multiple
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">
              支持上传最多9张图片，每张图片不超过5MB
            </div>
          </div>
        </div>
        
        <!-- 帖子类型 -->
        <div class="form-section">
          <label class="form-label">帖子类型</label>
          <el-radio-group v-model="form.post_type">
            <el-radio label="normal">普通帖子</el-radio>
            <el-radio label="question">提问</el-radio>
            <el-radio label="discussion">讨论</el-radio>
          </el-radio-group>
        </div>
        
        <!-- 匿名发布 -->
        <div class="form-section">
          <el-checkbox v-model="form.is_anonymous">
            匿名发布
          </el-checkbox>
          <div class="tip">匿名发布将隐藏您的身份信息</div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button @click="$router.back()">取消</el-button>
          <el-button 
            type="primary" 
            @click="submitForm"
            :loading="submitting"
            :disabled="!formValid"
          >
            发布帖子
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 图片预览 -->
    <el-dialog v-model="dialogVisible">
      <img w-full :src="dialogImageUrl" alt="Preview Image" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const form = ref({
  tieba_id: '',
  title: '',
  content: '',
  post_type: 'normal',
  is_anonymous: false,
  images: []
})

const tiebas = ref([])
const imageList = ref([])
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogImageUrl = ref('')

// 表单验证
const formValid = computed(() => {
  return form.value.tieba_id && 
         form.value.title.trim() && 
         form.value.content.trim()
})

// 处理图片预览
const handlePictureCardPreview = (file) => {
  dialogImageUrl.value = file.url
  dialogVisible.value = true
}

// 处理图片移除
const handleRemove = (file, fileList) => {
  form.value.images = form.value.images.filter(img => img !== file.url)
}

// 处理上传成功
const handleUploadSuccess = (response, file) => {
  form.value.images.push(response.url)
}

// 处理上传错误
const handleUploadError = (error) => {
  console.error('上传失败:', error)
  ElMessage.error('图片上传失败')
}

// 上传前验证
const beforeUpload = (file) => {
  const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif'
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isJPGOrPNG) {
    ElMessage.error('只能上传 JPG/PNG/GIF 格式的图片!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// 加载用户关注的贴吧
const loadUserTiebas = async () => {
  try {
    const response = await api.get('/user/tiebas/')
    tiebas.value = response.data
  } catch (error) {
    console.error('加载贴吧列表失败:', error)
  }
}

// 提交表单
const submitForm = async () => {
  if (!formValid.value) return
  
  try {
    submitting.value = true
    
    const postData = {
      ...form.value,
      title: form.value.title.trim(),
      content: form.value.content.trim()
    }
    
    const response = await api.post('/posts/', postData)
    
    ElMessage.success('帖子发布成功!')
    
    // 跳转到新发布的帖子页面
    router.push(`/post/${response.data.id}`)
  } catch (error) {
    console.error('发布失败:', error)
    ElMessage.error('帖子发布失败，请重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  // 检查用户是否登录
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再发布帖子')
    router.push('/login')
    return
  }
  
  loadUserTiebas()
})
</script>

<style scoped>
.create-post-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px 0;
}

.create-post-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.post-form {
  padding: 20px;
}

.form-section {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.tieba-option {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.member-count {
  margin-left: auto;
  color: #999;
  font-size: 12px;
}

.upload-section {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
}

.upload-tip {
  margin-top: 8px;
  color: #999;
  font-size: 12px;
}

.tip {
  margin-top: 4px;
  color: #999;
  font-size: 12px;
}

.form-actions {
  text-align: center;
  padding: 20px 0;
  border-top: 1px solid #f0f0f0;
}

.form-actions .el-button {
  margin: 0 8px;
  min-width: 100px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .create-post-container {
    margin: 0 10px;
  }
  
  .header {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 20px;
  }
  
  .post-form {
    padding: 15px;
  }
}
</style>