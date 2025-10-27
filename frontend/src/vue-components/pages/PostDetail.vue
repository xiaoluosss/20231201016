<template>
  <div class="post-detail-page">
    <!-- 帖子内容 -->
    <div class="post-content-section">
      <div class="content-container">
        <!-- 帖子头部 -->
        <div class="post-header">
          <div class="post-meta">
            <el-avatar :size="50" :src="post.author?.avatar" />
            <div class="author-info">
              <div class="author-name">{{ post.author?.nickname }}</div>
              <div class="post-time">{{ formatTime(post.created_at) }}</div>
            </div>
          </div>
          
          <div class="post-actions">
            <el-button 
              :type="post.is_liked ? 'primary' : 'default'" 
              @click="toggleLike"
            >
              <i>👍</i> {{ post.likes_count }}
            </el-button>
            <el-button 
              :type="post.is_collected ? 'primary' : 'default'" 
              @click="toggleCollect"
            >
              <i>⭐</i> 收藏
            </el-button>
            <el-button type="default" @click="sharePost">
              <i>📤</i> 分享
            </el-button>
          </div>
        </div>
        
        <!-- 帖子标题和内容 -->
        <div class="post-body">
          <h1 class="post-title">{{ post.title }}</h1>
          <div class="post-text" v-html="formatContent(post.content)"></div>
          
          <!-- 帖子图片 -->
          <div class="post-images" v-if="post.images && post.images.length > 0">
            <img 
              v-for="(image, index) in post.images" 
              :key="index" 
              :src="image" 
              :alt="post.title"
              class="post-image"
              @click="viewImage(image)"
            />
          </div>
        </div>
        
        <!-- 帖子统计 -->
        <div class="post-stats">
          <span class="stat-item">
            <i>👁️</i> {{ post.views_count }} 浏览
          </span>
          <span class="stat-item">
            <i>💬</i> {{ post.comments_count }} 评论
          </span>
          <span class="stat-item">
            <i>👍</i> {{ post.likes_count }} 点赞
          </span>
        </div>
      </div>
    </div>
    
    <!-- 评论区域 -->
    <div class="comments-section">
      <div class="content-container">
        <h2 class="section-title">评论 ({{ comments.length }})</h2>
        
        <!-- 评论输入框 -->
        <div class="comment-input" v-if="userStore.isLoggedIn">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="3"
            placeholder="写下你的评论..."
            maxlength="500"
            show-word-limit
          />
          <div class="comment-actions">
            <el-button type="primary" @click="submitComment" :loading="commentLoading">
              发表评论
            </el-button>
          </div>
        </div>
        <div class="login-prompt" v-else>
          <p>请<a href="/login">登录</a>后发表评论</p>
        </div>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div 
            v-for="comment in comments" 
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <el-avatar :size="40" :src="comment.author.avatar" />
              <div class="comment-info">
                <div class="comment-author">{{ comment.author.nickname }}</div>
                <div class="comment-time">{{ formatTime(comment.created_at) }}</div>
              </div>
              <div class="comment-actions">
                <el-button 
                  size="small" 
                  :type="comment.is_liked ? 'primary' : 'default'"
                  @click="toggleCommentLike(comment)"
                >
                  <i>👍</i> {{ comment.likes_count }}
                </el-button>
              </div>
            </div>
            
            <div class="comment-content">
              <p>{{ comment.content }}</p>
              
              <!-- 评论图片 -->
              <div class="comment-images" v-if="comment.images && comment.images.length > 0">
                <img 
                  v-for="(image, index) in comment.images" 
                  :key="index" 
                  :src="image" 
                  class="comment-image"
                  @click="viewImage(image)"
                />
              </div>
            </div>
            
            <!-- 回复区域 -->
            <div class="comment-reply" v-if="userStore.isLoggedIn">
              <el-input
                v-model="comment.replyText"
                size="small"
                placeholder="回复..."
                @keyup.enter="submitReply(comment)"
              />
            </div>
          </div>
        </div>
        
        <!-- 加载更多评论 -->
        <div class="load-more" v-if="hasMoreComments">
          <el-button @click="loadMoreComments" :loading="loading">
            加载更多评论
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 图片查看器 -->
    <el-image-viewer
      v-if="showImageViewer"
      :url-list="[currentImage]"
      :initial-index="0"
      @close="showImageViewer = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'

const route = useRoute()
const userStore = useUserStore()

const post = ref({})
const comments = ref([])
const newComment = ref('')
const loading = ref(false)
const commentLoading = ref(false)
const hasMoreComments = ref(true)
const showImageViewer = ref(false)
const currentImage = ref('')
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

// 格式化内容（简单的换行处理）
const formatContent = (content) => {
  return content.replace(/\n/g, '<br>')
}

// 查看图片
const viewImage = (imageUrl) => {
  currentImage.value = imageUrl
  showImageViewer.value = true
}

// 点赞/取消点赞帖子
const toggleLike = async () => {
  if (!userStore.isLoggedIn) {
    // 跳转到登录页
    return
  }
  
  try {
    if (post.value.is_liked) {
      await api.delete(`/posts/${post.value.id}/like/`)
      post.value.is_liked = false
      post.value.likes_count -= 1
    } else {
      await api.post(`/posts/${post.value.id}/like/`)
      post.value.is_liked = true
      post.value.likes_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 收藏/取消收藏帖子
const toggleCollect = async () => {
  if (!userStore.isLoggedIn) {
    // 跳转到登录页
    return
  }
  
  try {
    if (post.value.is_collected) {
      await api.delete(`/posts/${post.value.id}/collect/`)
      post.value.is_collected = false
    } else {
      await api.post(`/posts/${post.value.id}/collect/`)
      post.value.is_collected = true
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 分享帖子
const sharePost = () => {
  // 实现分享逻辑
  console.log('分享帖子:', post.value.id)
}

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    commentLoading.value = true
    const response = await api.post(`/posts/${post.value.id}/comments/`, {
      content: newComment.value
    })
    
    comments.value.unshift(response.data)
    post.value.comments_count += 1
    newComment.value = ''
  } catch (error) {
    console.error('发表评论失败:', error)
  } finally {
    commentLoading.value = false
  }
}

// 点赞/取消点赞评论
const toggleCommentLike = async (comment) => {
  if (!userStore.isLoggedIn) {
    // 跳转到登录页
    return
  }
  
  try {
    if (comment.is_liked) {
      await api.delete(`/comments/${comment.id}/like/`)
      comment.is_liked = false
      comment.likes_count -= 1
    } else {
      await api.post(`/comments/${comment.id}/like/`)
      comment.is_liked = true
      comment.likes_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 提交回复
const submitReply = async (comment) => {
  if (!comment.replyText?.trim()) return
  
  try {
    // 实现回复逻辑
    console.log('回复评论:', comment.id, comment.replyText)
    comment.replyText = ''
  } catch (error) {
    console.error('回复失败:', error)
  }
}

// 加载帖子详情
const loadPostDetail = async () => {
  try {
    loading.value = true
    const response = await api.get(`/posts/${route.params.id}/`)
    post.value = response.data
  } catch (error) {
    console.error('加载帖子详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载评论
const loadComments = async () => {
  try {
    const response = await api.get(`/posts/${route.params.id}/comments/`, {
      params: { page: page.value }
    })
    
    if (page.value === 1) {
      comments.value = response.data.results
    } else {
      comments.value.push(...response.data.results)
    }
    
    hasMoreComments.value = !!response.data.next
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

// 加载更多评论
const loadMoreComments = async () => {
  page.value += 1
  await loadComments()
}

onMounted(async () => {
  await Promise.all([
    loadPostDetail(),
    loadComments()
  ])
})
</script>

<style scoped>
.post-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.content-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.post-content-section {
  background: white;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.post-header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-info {
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

.post-actions {
  display: flex;
  gap: 8px;
}

.post-body {
  padding: 20px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.post-text {
  line-height: 1.8;
  color: #333;
  margin-bottom: 20px;
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.post-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
}

.post-stats {
  padding: 16px 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 14px;
}

.comments-section {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.section-title {
  padding: 20px 20px 0;
  font-size: 18px;
  color: #333;
}

.comment-input {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.comment-actions {
  margin-top: 12px;
  text-align: right;
}

.login-prompt {
  padding: 20px;
  text-align: center;
  color: #666;
}

.login-prompt a {
  color: #1890ff;
  text-decoration: none;
}

.comments-list {
  padding: 0 20px;
}

.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.comment-info {
  flex: 1;
}

.comment-author {
  font-weight: bold;
  color: #333;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-content {
  margin-left: 52px;
}

.comment-content p {
  line-height: 1.6;
  color: #333;
  margin-bottom: 12px;
}

.comment-images {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.comment-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
}

.comment-reply {
  margin-left: 52px;
  margin-top: 12px;
}

.load-more {
  text-align: center;
  padding: 20px;
}
</style>