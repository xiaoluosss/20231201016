<template>
  <div class="home-page">
    <!-- 顶部轮播图 -->
    <section class="banner-section">
      <div class="banner-container">
        <el-carousel height="300px" :interval="5000">
          <el-carousel-item v-for="item in banners" :key="item.id">
            <img :src="item.image" :alt="item.title" class="banner-image" />
            <div class="banner-content">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>
    </section>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-container">
        <!-- 左侧帖子列表 -->
        <div class="posts-section">
          <div class="section-header">
            <h2>热门帖子</h2>
            <el-button type="primary" @click="$router.push('/posts/create')" v-if="userStore.isLoggedIn">
              发帖
            </el-button>
          </div>
          
          <div class="posts-list">
            <div v-for="post in posts" :key="post.id" class="post-item">
              <div class="post-header">
                <el-avatar :size="40" :src="post.author.avatar" />
                <div class="post-info">
                  <div class="author-name">{{ post.author.nickname }}</div>
                  <div class="post-time">{{ formatTime(post.created_at) }}</div>
                </div>
                <div class="tieba-tag">{{ post.tieba.name }}</div>
              </div>
              
              <div class="post-content">
                <h3 class="post-title" @click="viewPost(post.id)">{{ post.title }}</h3>
                <p class="post-excerpt">{{ post.content.substring(0, 100) }}...</p>
                
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
          
          <div class="load-more">
            <el-button @click="loadMorePosts" :loading="loading">
              加载更多
            </el-button>
          </div>
        </div>
        
        <!-- 右侧边栏 -->
        <div class="sidebar">
          <!-- 热门贴吧 -->
          <div class="sidebar-section">
            <h3>热门贴吧</h3>
            <div class="tieba-list">
              <div v-for="tieba in hotTiebas" :key="tieba.id" class="tieba-item">
                <el-avatar :size="32" :src="tieba.avatar" />
                <div class="tieba-info">
                  <div class="tieba-name">{{ tieba.name }}</div>
                  <div class="tieba-stats">{{ tieba.members_count }} 成员</div>
                </div>
                <el-button size="small" type="primary">关注</el-button>
              </div>
            </div>
          </div>
          
          <!-- 推荐用户 -->
          <div class="sidebar-section">
            <h3>推荐用户</h3>
            <div class="user-list">
              <div v-for="user in recommendedUsers" :key="user.id" class="user-item">
                <el-avatar :size="40" :src="user.avatar" />
                <div class="user-info">
                  <div class="user-name">{{ user.nickname }}</div>
                  <div class="user-desc">{{ user.description || '这个人很懒，什么都没写' }}</div>
                </div>
                <el-button size="small">关注</el-button>
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
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

const banners = ref([
  { id: 1, title: '欢迎来到百度贴吧', description: '全球最大的中文社区', image: '/images/banner1.jpg' },
  { id: 2, title: '发现兴趣圈子', description: '找到志同道合的朋友', image: '/images/banner2.jpg' },
  { id: 3, title: '分享你的见解', description: '畅所欲言，交流思想', image: '/images/banner3.jpg' }
])

const posts = ref([])
const hotTiebas = ref([])
const recommendedUsers = ref([])
const loading = ref(false)
const page = ref(1)

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

// 查看帖子详情
const viewPost = (postId) => {
  router.push(`/posts/${postId}`)
}

// 加载帖子
const loadPosts = async () => {
  try {
    loading.value = true
    const response = await api.get('/posts/', { params: { page: page.value } })
    if (page.value === 1) {
      posts.value = response.data.results
    } else {
      posts.value.push(...response.data.results)
    }
  } catch (error) {
    console.error('加载帖子失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多帖子
const loadMorePosts = async () => {
  page.value += 1
  await loadPosts()
}

// 加载热门贴吧
const loadHotTiebas = async () => {
  try {
    const response = await api.get('/tiebas/hot/')
    hotTiebas.value = response.data
  } catch (error) {
    console.error('加载热门贴吧失败:', error)
  }
}

// 加载推荐用户
const loadRecommendedUsers = async () => {
  try {
    const response = await api.get('/users/recommended/')
    recommendedUsers.value = response.data
  } catch (error) {
    console.error('加载推荐用户失败:', error)
  }
}

onMounted(async () => {
  await Promise.all([
    loadPosts(),
    loadHotTiebas(),
    loadRecommendedUsers()
  ])
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.banner-section {
  margin-bottom: 20px;
}

.banner-container {
  max-width: 1200px;
  margin: 0 auto;
}

.banner-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.banner-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  color: white;
  padding: 20px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-list {
  background: white;
  border-radius: 8px;
  overflow: hidden;
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

.tieba-tag {
  background: #e6f7ff;
  color: #1890ff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
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

.tieba-item,
.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.tieba-info,
.user-info {
  flex: 1;
}

.tieba-name,
.user-name {
  font-weight: bold;
  color: #333;
}

.tieba-stats,
.user-desc {
  font-size: 12px;
  color: #999;
}
</style>