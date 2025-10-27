<template>
  <div class="tieba-detail-page">
    <!-- 贴吧头部信息 -->
    <div class="tieba-header">
      <div class="header-container">
        <div class="tieba-info">
          <el-avatar :size="80" :src="tieba.avatar" />
          <div class="tieba-details">
            <h1 class="tieba-name">{{ tieba.name }}</h1>
            <p class="tieba-desc">{{ tieba.description }}</p>
            <div class="tieba-stats">
              <span class="stat">成员: {{ tieba.members_count }}</span>
              <span class="stat">帖子: {{ tieba.posts_count }}</span>
              <span class="stat">创建于: {{ formatDate(tieba.created_at) }}</span>
            </div>
          </div>
        </div>
        
        <div class="tieba-actions">
          <el-button 
            :type="tieba.is_followed ? 'default' : 'primary'" 
            size="large"
            @click="toggleFollow"
          >
            {{ tieba.is_followed ? '已关注' : '关注贴吧' }}
          </el-button>
          <el-button 
            type="primary" 
            size="large"
            @click="$router.push(`/posts/create?tieba=${tieba.id}`)"
            v-if="userStore.isLoggedIn"
          >
            发帖
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-container">
        <!-- 左侧帖子列表 -->
        <div class="posts-section">
          <!-- 帖子筛选 -->
          <div class="posts-filter">
            <el-radio-group v-model="postFilter" @change="loadPosts">
              <el-radio-button label="latest">最新</el-radio-button>
              <el-radio-button label="hot">热门</el-radio-button>
              <el-radio-button label="essence">精华</el-radio-button>
            </el-radio-group>
          </div>

          <!-- 帖子列表 -->
          <div class="posts-list">
            <div 
              v-for="post in posts" 
              :key="post.id"
              class="post-item"
              @click="viewPost(post.id)"
            >
              <div class="post-header">
                <el-avatar :size="40" :src="post.author.avatar" />
                <div class="post-info">
                  <div class="author-name">{{ post.author.nickname }}</div>
                  <div class="post-time">{{ formatTime(post.created_at) }}</div>
                </div>
                <el-tag v-if="post.is_essence" type="warning" size="small">精华</el-tag>
              </div>
              
              <div class="post-content">
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-excerpt">{{ post.content.substring(0, 150) }}...</p>
                
                <div v-if="post.images && post.images.length > 0" class="post-images">
                  <img 
                    v-for="(image, index) in post.images.slice(0, 3)" 
                    :key="index" 
                    :src="image" 
                    :alt="post.title"
                    class="post-image"
                  />
                </div>
              </div>
              
              <div class="post-stats">
                <span class="stat-item">
                  <i>👍</i> {{ post.likes_count }}
                </span>
                <span class="stat-item">
                  <i>💬</i> {{ post.comments_count }}
                </span>
                <span class="stat-item">
                  <i>👁️</i> {{ post.views_count }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- 加载更多 -->
          <div class="load-more" v-if="hasMore">
            <el-button @click="loadMorePosts" :loading="loading">
              加载更多
            </el-button>
          </div>
        </div>
        
        <!-- 右侧边栏 -->
        <div class="sidebar">
          <!-- 贴吧公告 -->
          <div class="sidebar-section" v-if="announcements.length > 0">
            <h3>贴吧公告</h3>
            <div class="announcements">
              <div 
                v-for="announcement in announcements" 
                :key="announcement.id"
                class="announcement-item"
              >
                <h4>{{ announcement.title }}</h4>
                <p>{{ announcement.content }}</p>
                <div class="announcement-time">{{ formatTime(announcement.created_at) }}</div>
              </div>
            </div>
          </div>
          
          <!-- 贴吧管理 -->
          <div class="sidebar-section" v-if="tieba.is_admin">
            <h3>贴吧管理</h3>
            <div class="admin-actions">
              <el-button type="primary" size="small" style="width: 100%; margin-bottom: 8px;">
                发布公告
              </el-button>
              <el-button type="default" size="small" style="width: 100%;">
                管理成员
              </el-button>
            </div>
          </div>
          
          <!-- 热门帖子 -->
          <div class="sidebar-section">
            <h3>热门帖子</h3>
            <div class="hot-posts">
              <div 
                v-for="post in hotPosts" 
                :key="post.id"
                class="hot-post-item"
                @click="viewPost(post.id)"
              >
                <div class="hot-post-title">{{ post.title }}</div>
                <div class="hot-post-stats">
                  <span>{{ post.likes_count }} 赞</span>
                  <span>{{ post.comments_count }} 评论</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const tieba = ref({})
const posts = ref([])
const announcements = ref([])
const hotPosts = ref([])
const loading = ref(false)
const hasMore = ref(true)
const page = ref(1)
const postFilter = ref('latest')

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

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// 查看帖子详情
const viewPost = (postId) => {
  router.push(`/posts/${postId}`)
}

// 关注/取消关注贴吧
const toggleFollow = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  try {
    if (tieba.value.is_followed) {
      await api.delete(`/tiebas/${tieba.value.id}/follow/`)
      tieba.value.is_followed = false
      tieba.value.members_count -= 1
    } else {
      await api.post(`/tiebas/${tieba.value.id}/follow/`)
      tieba.value.is_followed = true
      tieba.value.members_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 加载贴吧详情
const loadTiebaDetail = async () => {
  try {
    const response = await api.get(`/tiebas/${route.params.id}/`)
    tieba.value = response.data
  } catch (error) {
    console.error('加载贴吧详情失败:', error)
  }
}

// 加载帖子列表
const loadPosts = async () => {
  try {
    loading.value = true
    page.value = 1
    
    const params = {
      page: page.value,
      ordering: postFilter.value === 'latest' ? '-created_at' : 
                postFilter.value === 'hot' ? '-likes_count' : '-created_at'
    }
    
    const response = await api.get(`/tiebas/${route.params.id}/posts/`, { params })
    posts.value = response.data.results
    hasMore.value = !!response.data.next
  } catch (error) {
    console.error('加载帖子失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多帖子
const loadMorePosts = async () => {
  try {
    page.value += 1
    
    const params = {
      page: page.value,
      ordering: postFilter.value === 'latest' ? '-created_at' : 
                postFilter.value === 'hot' ? '-likes_count' : '-created_at'
    }
    
    const response = await api.get(`/tiebas/${route.params.id}/posts/`, { params })
    posts.value.push(...response.data.results)
    hasMore.value = !!response.data.next
  } catch (error) {
    console.error('加载更多帖子失败:', error)
  }
}

// 加载公告
const loadAnnouncements = async () => {
  try {
    const response = await api.get(`/tiebas/${route.params.id}/announcements/`)
    announcements.value = response.data
  } catch (error) {
    console.error('加载公告失败:', error)
  }
}

// 加载热门帖子
const loadHotPosts = async () => {
  try {
    const response = await api.get(`/tiebas/${route.params.id}/hot-posts/`)
    hotPosts.value = response.data
  } catch (error) {
    console.error('加载热门帖子失败:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    loadTiebaDetail(),
    loadPosts(),
    loadAnnouncements(),
    loadHotPosts()
  ])
})
</script>

<style scoped>
.tieba-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.tieba-header {
  background: white;
  border-bottom: 1px solid #e8e8e8;
  padding: 30px 0;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tieba-info {
  display: flex;
  gap: 20px;
  align-items: center;
}

.tieba-details {
  flex: 1;
}

.tieba-name {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.tieba-desc {
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.tieba-stats {
  display: flex;
  gap: 20px;
}

.stat {
  color: #999;
  font-size: 14px;
}

.tieba-actions {
  display: flex;
  gap: 12px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.posts-filter {
  background: white;
  padding: 16px 20px;
  border-radius: 8px 8px 0 0;
  margin-bottom: 1px;
}

.posts-list {
  background: white;
  border-radius: 0 0 8px 8px;
}

.post-item {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.post-item:hover {
  background: #fafafa;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  gap: 12px;
}

.post-info {
  flex: 1;
}

.author-name {
  font-weight: bold;
  color: #333;
}

.post-time {
  font-size: 12px;
  color: #999;
}

.post-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.post-excerpt {
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.post-images {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.post-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.post-stats {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 14px;
}

.load-more {
  text-align: center;
  padding: 20px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.sidebar-section h3 {
  margin-bottom: 16px;
  color: #333;
}

.announcement-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.announcement-item:last-child {
  border-bottom: none;
}

.announcement-item h4 {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.announcement-item p {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  margin-bottom: 8px;
}

.announcement-time {
  font-size: 12px;
  color: #999;
}

.hot-post-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.hot-post-item:hover {
  background: #fafafa;
}

.hot-post-item:last-child {
  border-bottom: none;
}

.hot-post-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hot-post-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #999;
}
</style>