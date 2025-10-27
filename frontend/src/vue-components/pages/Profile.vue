<template>
  <div class="profile-page">
    <div class="profile-container">
      <!-- 用户信息头部 -->
      <div class="profile-header">
        <div class="header-content">
          <div class="avatar-section">
            <el-avatar :size="100" :src="userInfo.avatar" />
            <div class="avatar-actions">
              <el-button size="small" @click="editAvatar">更换头像</el-button>
            </div>
          </div>
          
          <div class="info-section">
            <h1 class="username">{{ userInfo.nickname }}</h1>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.posts_count }}</span>
                <span class="stat-label">帖子</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.followers_count }}</span>
                <span class="stat-label">粉丝</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ userInfo.following_count }}</span>
                <span class="stat-label">关注</span>
              </div>
            </div>
            
            <div class="user-bio">
              <p>{{ userInfo.bio || '这个人很懒，还没有写简介~' }}</p>
            </div>
            
            <div class="action-buttons">
              <el-button 
                v-if="!isOwnProfile"
                :type="userInfo.is_followed ? 'default' : 'primary'"
                @click="toggleFollow"
              >
                {{ userInfo.is_followed ? '已关注' : '关注' }}
              </el-button>
              <el-button v-if="isOwnProfile" @click="editProfile">编辑资料</el-button>
              <el-button v-if="isOwnProfile" @click="showSettings">设置</el-button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 导航标签 -->
      <div class="profile-nav">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="帖子" name="posts">
            <div class="tab-content">
              <div class="posts-list" v-if="posts.length > 0">
                <div 
                  v-for="post in posts" 
                  :key="post.id"
                  class="post-item"
                  @click="viewPost(post)"
                >
                  <div class="post-header">
                    <span class="post-title">{{ post.title }}</span>
                    <span class="post-time">{{ formatTime(post.created_at) }}</span>
                  </div>
                  <div class="post-content">
                    {{ post.content.substring(0, 100) }}{{ post.content.length > 100 ? '...' : '' }}
                  </div>
                  <div class="post-stats">
                    <span class="stat">👁️ {{ post.views_count }}</span>
                    <span class="stat">💬 {{ post.comments_count }}</span>
                    <span class="stat">👍 {{ post.likes_count }}</span>
                  </div>
                </div>
              </div>
              <div class="empty-state" v-else>
                <p>还没有发布过帖子</p>
                <el-button v-if="isOwnProfile" type="primary" @click="createPost">
                  去发布第一个帖子
                </el-button>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="收藏" name="collections">
            <div class="tab-content">
              <div class="collections-list" v-if="collections.length > 0">
                <div 
                  v-for="item in collections" 
                  :key="item.id"
                  class="collection-item"
                  @click="viewPost(item.post)"
                >
                  <div class="post-header">
                    <span class="post-title">{{ item.post.title }}</span>
                    <span class="collection-time">{{ formatTime(item.created_at) }}</span>
                  </div>
                  <div class="post-content">
                    {{ item.post.content.substring(0, 100) }}{{ item.post.content.length > 100 ? '...' : '' }}
                  </div>
                </div>
              </div>
              <div class="empty-state" v-else>
                <p>还没有收藏任何帖子</p>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="关注" name="following">
            <div class="tab-content">
              <div class="following-list" v-if="following.length > 0">
                <div 
                  v-for="user in following" 
                  :key="user.id"
                  class="user-item"
                >
                  <el-avatar :size="50" :src="user.avatar" />
                  <div class="user-info">
                    <div class="username">{{ user.nickname }}</div>
                    <div class="user-bio">{{ user.bio || '这个人很懒，还没有写简介~' }}</div>
                  </div>
                  <div class="user-actions">
                    <el-button 
                      size="small" 
                      :type="user.is_followed ? 'default' : 'primary'"
                      @click="toggleUserFollow(user)"
                    >
                      {{ user.is_followed ? '已关注' : '关注' }}
                    </el-button>
                  </div>
                </div>
              </div>
              <div class="empty-state" v-else>
                <p>还没有关注任何人</p>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="粉丝" name="followers">
            <div class="tab-content">
              <div class="followers-list" v-if="followers.length > 0">
                <div 
                  v-for="user in followers" 
                  :key="user.id"
                  class="user-item"
                >
                  <el-avatar :size="50" :src="user.avatar" />
                  <div class="user-info">
                    <div class="username">{{ user.nickname }}</div>
                    <div class="user-bio">{{ user.bio || '这个人很懒，还没有写简介~' }}</div>
                  </div>
                  <div class="user-actions">
                    <el-button 
                      size="small" 
                      :type="user.is_followed ? 'default' : 'primary'"
                      @click="toggleUserFollow(user)"
                    >
                      {{ user.is_followed ? '已关注' : '关注' }}
                    </el-button>
                  </div>
                </div>
              </div>
              <div class="empty-state" v-else>
                <p>还没有粉丝</p>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    
    <!-- 编辑资料对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑资料" width="500px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="昵称">
          <el-input v-model="editForm.nickname" maxlength="20" show-word-limit />
        </el-form-item>
        <el-form-item label="简介">
          <el-input 
            v-model="editForm.bio" 
            type="textarea" 
            :rows="3"
            maxlength="200" 
            show-word-limit
            placeholder="介绍一下自己吧~"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProfile" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const userInfo = ref({})
const activeTab = ref('posts')
const posts = ref([])
const collections = ref([])
const following = ref([])
const followers = ref([])
const editDialogVisible = ref(false)
const saving = ref(false)

const editForm = ref({
  nickname: '',
  bio: ''
})

// 判断是否是自己的个人中心
const isOwnProfile = computed(() => {
  return route.params.id === userStore.user?.id.toString() || !route.params.id
})

// 格式化时间
const formatTime = (timeString) => {
  const date = new Date(timeString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return date.toLocaleDateString()
}

// 加载用户信息
const loadUserInfo = async () => {
  try {
    const userId = route.params.id || userStore.user?.id
    const response = await api.get(`/users/${userId}/`)
    userInfo.value = response.data
    editForm.value.nickname = userInfo.value.nickname
    editForm.value.bio = userInfo.value.bio || ''
  } catch (error) {
    console.error('加载用户信息失败:', error)
  }
}

// 加载用户帖子
const loadUserPosts = async () => {
  try {
    const userId = route.params.id || userStore.user?.id
    const response = await api.get(`/users/${userId}/posts/`)
    posts.value = response.data
  } catch (error) {
    console.error('加载用户帖子失败:', error)
  }
}

// 加载用户收藏
const loadUserCollections = async () => {
  try {
    const userId = route.params.id || userStore.user?.id
    const response = await api.get(`/users/${userId}/collections/`)
    collections.value = response.data
  } catch (error) {
    console.error('加载用户收藏失败:', error)
  }
}

// 加载用户关注列表
const loadUserFollowing = async () => {
  try {
    const userId = route.params.id || userStore.user?.id
    const response = await api.get(`/users/${userId}/following/`)
    following.value = response.data
  } catch (error) {
    console.error('加载关注列表失败:', error)
  }
}

// 加载用户粉丝列表
const loadUserFollowers = async () => {
  try {
    const userId = route.params.id || userStore.user?.id
    const response = await api.get(`/users/${userId}/followers/`)
    followers.value = response.data
  } catch (error) {
    console.error('加载粉丝列表失败:', error)
  }
}

// 切换标签
const handleTabClick = (tab) => {
  switch (tab.paneName) {
    case 'posts':
      loadUserPosts()
      break
    case 'collections':
      loadUserCollections()
      break
    case 'following':
      loadUserFollowing()
      break
    case 'followers':
      loadUserFollowers()
      break
  }
}

// 关注/取消关注用户
const toggleFollow = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  try {
    if (userInfo.value.is_followed) {
      await api.delete(`/users/${userInfo.value.id}/follow/`)
      userInfo.value.is_followed = false
      userInfo.value.followers_count -= 1
    } else {
      await api.post(`/users/${userInfo.value.id}/follow/`)
      userInfo.value.is_followed = true
      userInfo.value.followers_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 关注/取消关注其他用户
const toggleUserFollow = async (user) => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  try {
    if (user.is_followed) {
      await api.delete(`/users/${user.id}/follow/`)
      user.is_followed = false
    } else {
      await api.post(`/users/${user.id}/follow/`)
      user.is_followed = true
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 编辑资料
const editProfile = () => {
  editDialogVisible.value = true
}

// 保存资料
const saveProfile = async () => {
  try {
    saving.value = true
    await api.put(`/users/${userStore.user.id}/`, editForm.value)
    
    // 更新本地用户信息
    userInfo.value.nickname = editForm.value.nickname
    userInfo.value.bio = editForm.value.bio
    
    // 更新store中的用户信息
    userStore.updateUserInfo(editForm.value)
    
    editDialogVisible.value = false
    ElMessage.success('资料更新成功')
  } catch (error) {
    console.error('保存资料失败:', error)
    ElMessage.error('资料更新失败')
  } finally {
    saving.value = false
  }
}

// 更换头像
const editAvatar = () => {
  // 实现头像上传逻辑
  console.log('更换头像')
}

// 显示设置
const showSettings = () => {
  router.push('/settings')
}

// 查看帖子
const viewPost = (post) => {
  router.push(`/post/${post.id}`)
}

// 创建帖子
const createPost = () => {
  router.push('/create-post')
}

onMounted(async () => {
  await loadUserInfo()
  await loadUserPosts()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 20px;
}

.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 30px;
  padding: 0 40px;
}

.avatar-section {
  text-align: center;
}

.avatar-actions {
  margin-top: 10px;
}

.info-section {
  flex: 1;
}

.username {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 16px 0;
}

.user-stats {
  display: flex;
  gap: 30px;
  margin-bottom: 16px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 24px;
  font-weight: bold;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.user-bio {
  margin-bottom: 20px;
  font-size: 14px;
  opacity: 0.9;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.profile-nav {
  padding: 0 20px;
}

.tab-content {
  padding: 20px 0;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-item {
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.post-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.post-title {
  font-weight: bold;
  color: #333;
  font-size: 16px;
}

.post-time {
  color: #999;
  font-size: 12px;
}

.post-content {
  color: #666;
  line-height: 1.6;
  margin-bottom: 8px;
}

.post-stats {
  display: flex;
  gap: 16px;
}

.stat {
  color: #999;
  font-size: 12px;
}

.collections-list,
.following-list,
.followers-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.collection-item {
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.collection-item:hover {
  border-color: #1890ff;
}

.collection-time {
  color: #999;
  font-size: 12px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
}

.user-info {
  flex: 1;
}

.user-info .username {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0 0 4px 0;
}

.user-info .user-bio {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
    padding: 0 20px;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .profile-nav {
    padding: 0 10px;
  }
}
</style>