<template>
  <div class="search-page">
    <div class="search-container">
      <!-- 搜索框 -->
      <div class="search-header">
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索帖子、贴吧、用户..."
            size="large"
            @keyup.enter="performSearch"
          >
            <template #append>
              <el-button @click="performSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </div>
        
        <!-- 搜索筛选 -->
        <div class="search-filters">
          <el-radio-group v-model="searchType" @change="handleTypeChange">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="posts">帖子</el-radio-button>
            <el-radio-button label="tiebas">贴吧</el-radio-button>
            <el-radio-button label="users">用户</el-radio-button>
          </el-radio-group>
          
          <el-select v-model="sortBy" placeholder="排序方式" style="margin-left: 12px;">
            <el-option label="相关度" value="relevance" />
            <el-option label="最新" value="latest" />
            <el-option label="最热" value="hot" />
          </el-select>
        </div>
      </div>
      
      <!-- 搜索结果 -->
      <div class="search-results">
        <!-- 搜索结果统计 -->
        <div class="results-stats">
          找到约 {{ totalResults }} 条结果
        </div>
        
        <!-- 帖子搜索结果 -->
        <div v-if="searchType === 'all' || searchType === 'posts'" class="results-section">
          <h3 class="section-title">帖子</h3>
          <div class="posts-results">
            <div 
              v-for="post in postsResults" 
              :key="post.id"
              class="post-result"
              @click="viewPost(post)"
            >
              <div class="post-header">
                <el-avatar :size="30" :src="post.author.avatar" />
                <div class="post-meta">
                  <div class="author-name">{{ post.author.nickname }}</div>
                  <div class="post-time">{{ formatTime(post.created_at) }}</div>
                </div>
                <div class="tieba-tag">{{ post.tieba_name }}</div>
              </div>
              <div class="post-content">
                <h4 class="post-title">{{ highlightKeywords(post.title) }}</h4>
                <p class="post-excerpt">{{ highlightKeywords(post.excerpt) }}</p>
              </div>
              <div class="post-stats">
                <span class="stat">👁️ {{ post.views_count }}</span>
                <span class="stat">💬 {{ post.comments_count }}</span>
                <span class="stat">👍 {{ post.likes_count }}</span>
              </div>
            </div>
          </div>
          <div class="load-more" v-if="postsResults.length > 0 && hasMorePosts">
            <el-button @click="loadMorePosts" :loading="loading">
              加载更多帖子
            </el-button>
          </div>
        </div>
        
        <!-- 贴吧搜索结果 -->
        <div v-if="searchType === 'all' || searchType === 'tiebas'" class="results-section">
          <h3 class="section-title">贴吧</h3>
          <div class="tiebas-results">
            <div 
              v-for="tieba in tiebasResults" 
              :key="tieba.id"
              class="tieba-result"
              @click="viewTieba(tieba)"
            >
              <el-avatar :size="50" :src="tieba.avatar" />
              <div class="tieba-info">
                <h4 class="tieba-name">{{ highlightKeywords(tieba.name) }}</h4>
                <p class="tieba-desc">{{ tieba.description }}</p>
                <div class="tieba-stats">
                  <span class="stat">{{ tieba.member_count }} 成员</span>
                  <span class="stat">{{ tieba.posts_count }} 帖子</span>
                </div>
              </div>
              <div class="tieba-actions">
                <el-button 
                  size="small" 
                  :type="tieba.is_followed ? 'default' : 'primary'"
                  @click.stop="toggleFollowTieba(tieba)"
                >
                  {{ tieba.is_followed ? '已关注' : '关注' }}
                </el-button>
              </div>
            </div>
          </div>
          <div class="load-more" v-if="tiebasResults.length > 0 && hasMoreTiebas">
            <el-button @click="loadMoreTiebas" :loading="loading">
              加载更多贴吧
            </el-button>
          </div>
        </div>
        
        <!-- 用户搜索结果 -->
        <div v-if="searchType === 'all' || searchType === 'users'" class="results-section">
          <h3 class="section-title">用户</h3>
          <div class="users-results">
            <div 
              v-for="user in usersResults" 
              :key="user.id"
              class="user-result"
              @click="viewProfile(user)"
            >
              <el-avatar :size="50" :src="user.avatar" />
              <div class="user-info">
                <h4 class="user-name">{{ highlightKeywords(user.nickname) }}</h4>
                <p class="user-bio">{{ user.bio || '这个人很懒，还没有写简介~' }}</p>
                <div class="user-stats">
                  <span class="stat">{{ user.posts_count }} 帖子</span>
                  <span class="stat">{{ user.followers_count }} 粉丝</span>
                </div>
              </div>
              <div class="user-actions">
                <el-button 
                  size="small" 
                  :type="user.is_followed ? 'default' : 'primary'"
                  @click.stop="toggleFollowUser(user)"
                >
                  {{ user.is_followed ? '已关注' : '关注' }}
                </el-button>
              </div>
            </div>
          </div>
          <div class="load-more" v-if="usersResults.length > 0 && hasMoreUsers">
            <el-button @click="loadMoreUsers" :loading="loading">
              加载更多用户
            </el-button>
          </div>
        </div>
        
        <!-- 无结果 -->
        <div v-if="!loading && totalResults === 0" class="no-results">
          <div class="empty-state">
            <el-icon size="64"><Search /></el-icon>
            <h3>没有找到相关结果</h3>
            <p>尝试使用其他关键词或调整搜索条件</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const searchType = ref('all')
const sortBy = ref('relevance')
const loading = ref(false)

// 搜索结果数据
const postsResults = ref([])
const tiebasResults = ref([])
const usersResults = ref([])

// 分页信息
const postsPage = ref(1)
const tiebasPage = ref(1)
const usersPage = ref(1)
const hasMorePosts = ref(true)
const hasMoreTiebas = ref(true)
const hasMoreUsers = ref(true)

// 总结果数
const totalResults = computed(() => {
  let total = 0
  if (searchType.value === 'all' || searchType.value === 'posts') {
    total += postsResults.value.length
  }
  if (searchType.value === 'all' || searchType.value === 'tiebas') {
    total += tiebasResults.value.length
  }
  if (searchType.value === 'all' || searchType.value === 'users') {
    total += usersResults.value.length
  }
  return total
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

// 高亮关键词
const highlightKeywords = (text) => {
  if (!searchQuery.value.trim() || !text) return text
  
  const regex = new RegExp(`(${searchQuery.value})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 执行搜索
const performSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  loading.value = true
  
  // 重置分页
  postsPage.value = 1
  tiebasPage.value = 1
  usersPage.value = 1
  postsResults.value = []
  tiebasResults.value = []
  usersResults.value = []
  
  try {
    await Promise.all([
      searchPosts(),
      searchTiebas(),
      searchUsers()
    ])
  } catch (error) {
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索帖子
const searchPosts = async () => {
  if (searchType.value !== 'all' && searchType.value !== 'posts') return
  
  try {
    const response = await api.get('/search/posts/', {
      params: {
        q: searchQuery.value,
        page: postsPage.value,
        sort: sortBy.value
      }
    })
    
    if (postsPage.value === 1) {
      postsResults.value = response.data.results
    } else {
      postsResults.value.push(...response.data.results)
    }
    
    hasMorePosts.value = !!response.data.next
  } catch (error) {
    console.error('搜索帖子失败:', error)
  }
}

// 搜索贴吧
const searchTiebas = async () => {
  if (searchType.value !== 'all' && searchType.value !== 'tiebas') return
  
  try {
    const response = await api.get('/search/tiebas/', {
      params: {
        q: searchQuery.value,
        page: tiebasPage.value
      }
    })
    
    if (tiebasPage.value === 1) {
      tiebasResults.value = response.data.results
    } else {
      tiebasResults.value.push(...response.data.results)
    }
    
    hasMoreTiebas.value = !!response.data.next
  } catch (error) {
    console.error('搜索贴吧失败:', error)
  }
}

// 搜索用户
const searchUsers = async () => {
  if (searchType.value !== 'all' && searchType.value !== 'users') return
  
  try {
    const response = await api.get('/search/users/', {
      params: {
        q: searchQuery.value,
        page: usersPage.value
      }
    })
    
    if (usersPage.value === 1) {
      usersResults.value = response.data.results
    } else {
      usersResults.value.push(...response.data.results)
    }
    
    hasMoreUsers.value = !!response.data.next
  } catch (error) {
    console.error('搜索用户失败:', error)
  }
}

// 处理搜索类型变化
const handleTypeChange = () => {
  if (searchQuery.value.trim()) {
    performSearch()
  }
}

// 加载更多帖子
const loadMorePosts = async () => {
  postsPage.value += 1
  await searchPosts()
}

// 加载更多贴吧
const loadMoreTiebas = async () => {
  tiebasPage.value += 1
  await searchTiebas()
}

// 加载更多用户
const loadMoreUsers = async () => {
  usersPage.value += 1
  await searchUsers()
}

// 查看帖子
const viewPost = (post) => {
  router.push(`/post/${post.id}`)
}

// 查看贴吧
const viewTieba = (tieba) => {
  router.push(`/tiebas/${tieba.id}`)
}

// 查看用户资料
const viewProfile = (user) => {
  router.push(`/profile/${user.id}`)
}

// 关注/取消关注贴吧
const toggleFollowTieba = async (tieba) => {
  try {
    if (tieba.is_followed) {
      await api.delete(`/tiebas/${tieba.id}/follow/`)
      tieba.is_followed = false
      tieba.member_count -= 1
    } else {
      await api.post(`/tiebas/${tieba.id}/follow/`)
      tieba.is_followed = true
      tieba.member_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 关注/取消关注用户
const toggleFollowUser = async (user) => {
  try {
    if (user.is_followed) {
      await api.delete(`/users/${user.id}/follow/`)
      user.is_followed = false
      user.followers_count -= 1
    } else {
      await api.post(`/users/${user.id}/follow/`)
      user.is_followed = true
      user.followers_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

onMounted(() => {
  // 如果有URL参数，自动搜索
  if (route.query.q) {
    searchQuery.value = route.query.q
    if (route.query.type) {
      searchType.value = route.query.type
    }
    performSearch()
  }
})
</script>

<style scoped>
.search-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px 0;
}

.search-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.search-header {
  padding: 30px;
  border-bottom: 1px solid #f0f0f0;
}

.search-box {
  margin-bottom: 20px;
}

.search-filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.search-results {
  padding: 0 30px 30px;
}

.results-stats {
  color: #999;
  font-size: 14px;
  margin-bottom: 20px;
}

.results-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.posts-results,
.tiebas-results,
.users-results {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-result,
.tieba-result,
.user-result {
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.post-result:hover,
.tieba-result:hover,
.user-result:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.post-meta {
  flex: 1;
}

.author-name {
  font-weight: bold;
  color: #333;
}

.post-time {
  color: #999;
  font-size: 12px;
}

.tieba-tag {
  background: #f0f0f0;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.post-content {
  margin-bottom: 12px;
}

.post-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.post-title :deep(mark) {
  background: #fffb8f;
  color: #333;
}

.post-excerpt {
  color: #666;
  line-height: 1.6;
  font-size: 14px;
}

.post-excerpt :deep(mark) {
  background: #fffb8f;
  color: #333;
}

.post-stats {
  display: flex;
  gap: 16px;
}

.stat {
  color: #999;
  font-size: 12px;
}

.tieba-result,
.user-result {
  display: flex;
  align-items: center;
  gap: 16px;
}

.tieba-info,
.user-info {
  flex: 1;
}

.tieba-name,
.user-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.tieba-name :deep(mark),
.user-name :deep(mark) {
  background: #fffb8f;
  color: #333;
}

.tieba-desc,
.user-bio {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.tieba-stats,
.user-stats {
  display: flex;
  gap: 12px;
}

.tieba-actions,
.user-actions {
  flex-shrink: 0;
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
}

.empty-state {
  color: #999;
}

.empty-state h3 {
  margin: 16px 0 8px;
  font-size: 18px;
}

.empty-state p {
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-header {
    padding: 20px;
  }
  
  .search-results {
    padding: 0 20px 20px;
  }
  
  .search-filters {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .tieba-result,
  .user-result {
    flex-direction: column;
    text-align: center;
  }
}
</style>