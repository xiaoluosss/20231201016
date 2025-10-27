<template>
  <div class="tiebas-page">
    <div class="page-header">
      <div class="header-container">
        <h1>贴吧列表</h1>
        <p>发现您感兴趣的社区</p>
        
        <!-- 搜索和筛选 -->
        <div class="search-filter">
          <div class="search-box">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索贴吧..."
              size="large"
              prefix-icon="Search"
              @input="handleSearch"
            />
          </div>
          
          <div class="filter-options">
            <el-select v-model="selectedCategory" placeholder="全部分类" @change="handleFilter">
              <el-option label="全部分类" value="" />
              <el-option 
                v-for="category in categories" 
                :key="category.id" 
                :label="category.name" 
                :value="category.id" 
              />
            </el-select>
            
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort">
              <el-option label="按成员数排序" value="members" />
              <el-option label="按创建时间排序" value="created" />
              <el-option label="按活跃度排序" value="activity" />
            </el-select>
          </div>
        </div>
      </div>
    </div>
    
    <div class="page-content">
      <div class="content-container">
        <!-- 分类导航 -->
        <div class="category-nav">
          <div 
            v-for="category in categories" 
            :key="category.id"
            :class="['category-item', { active: selectedCategory === category.id }]"
            @click="selectCategory(category.id)"
          >
            <div class="category-icon">{{ category.icon }}</div>
            <span class="category-name">{{ category.name }}</span>
          </div>
        </div>
        
        <!-- 贴吧列表 -->
        <div class="tiebas-grid">
          <div 
            v-for="tieba in tiebas" 
            :key="tieba.id"
            class="tieba-card"
            @click="viewTieba(tieba.id)"
          >
            <div class="tieba-header">
              <el-avatar :size="60" :src="tieba.avatar" />
              <div class="tieba-info">
                <h3 class="tieba-name">{{ tieba.name }}</h3>
                <p class="tieba-desc">{{ tieba.description }}</p>
                <div class="tieba-stats">
                  <span class="stat">成员: {{ tieba.members_count }}</span>
                  <span class="stat">帖子: {{ tieba.posts_count }}</span>
                </div>
              </div>
            </div>
            
            <div class="tieba-footer">
              <div class="category-tag">{{ getCategoryName(tieba.category) }}</div>
              <el-button 
                size="small" 
                :type="tieba.is_followed ? 'default' : 'primary'"
                @click.stop="toggleFollow(tieba)"
              >
                {{ tieba.is_followed ? '已关注' : '关注' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 加载更多 -->
        <div class="load-more" v-if="hasMore">
          <el-button @click="loadMore" :loading="loading">
            加载更多
          </el-button>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="!loading && tiebas.length === 0">
          <div class="empty-icon">🏷️</div>
          <h3>暂无贴吧</h3>
          <p>当前筛选条件下没有找到贴吧</p>
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

const searchKeyword = ref('')
const selectedCategory = ref('')
const sortBy = ref('members')
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

const categories = ref([
  { id: 1, name: '游戏', icon: '🎮' },
  { id: 2, name: '动漫', icon: '📺' },
  { id: 3, name: '科技', icon: '💻' },
  { id: 4, name: '体育', icon: '⚽' },
  { id: 5, name: '音乐', icon: '🎵' },
  { id: 6, name: '影视', icon: '🎬' },
  { id: 7, name: '生活', icon: '🏠' },
  { id: 8, name: '学习', icon: '📚' }
])

const tiebas = ref([])

// 获取分类名称
const getCategoryName = (categoryId) => {
  const category = categories.value.find(cat => cat.id === categoryId)
  return category ? category.name : '其他'
}

// 搜索贴吧
const handleSearch = () => {
  page.value = 1
  hasMore.value = true
  loadTiebas()
}

// 筛选分类
const handleFilter = () => {
  page.value = 1
  hasMore.value = true
  loadTiebas()
}

// 排序
const handleSort = () => {
  page.value = 1
  hasMore.value = true
  loadTiebas()
}

// 选择分类
const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  page.value = 1
  hasMore.value = true
  loadTiebas()
}

// 查看贴吧详情
const viewTieba = (tiebaId) => {
  router.push(`/tiebas/${tiebaId}`)
}

// 关注/取消关注贴吧
const toggleFollow = async (tieba) => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  try {
    if (tieba.is_followed) {
      await api.delete(`/tiebas/${tieba.id}/follow/`)
      tieba.is_followed = false
      tieba.members_count -= 1
    } else {
      await api.post(`/tiebas/${tieba.id}/follow/`)
      tieba.is_followed = true
      tieba.members_count += 1
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

// 加载贴吧列表
const loadTiebas = async () => {
  try {
    loading.value = true
    const params = {
      page: page.value,
      search: searchKeyword.value,
      category: selectedCategory.value,
      ordering: sortBy.value
    }
    
    const response = await api.get('/tiebas/', { params })
    
    if (page.value === 1) {
      tiebas.value = response.data.results
    } else {
      tiebas.value.push(...response.data.results)
    }
    
    hasMore.value = !!response.data.next
  } catch (error) {
    console.error('加载贴吧失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = async () => {
  page.value += 1
  await loadTiebas()
}

onMounted(() => {
  loadTiebas()
})
</script>

<style scoped>
.tiebas-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.page-header {
  background: white;
  padding: 40px 0 20px;
  border-bottom: 1px solid #e8e8e8;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 8px;
}

.page-header p {
  color: #666;
  margin-bottom: 30px;
}

.search-filter {
  display: flex;
  gap: 20px;
  align-items: center;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.filter-options {
  display: flex;
  gap: 12px;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.category-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
  margin-bottom: 30px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.category-item:hover {
  border-color: #1890ff;
  transform: translateY(-2px);
}

.category-item.active {
  border-color: #1890ff;
  background: #e6f7ff;
}

.category-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.category-name {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.tiebas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.tieba-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #f0f0f0;
}

.tieba-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.tieba-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.tieba-info {
  flex: 1;
}

.tieba-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.tieba-desc {
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tieba-stats {
  display: flex;
  gap: 16px;
}

.stat {
  font-size: 12px;
  color: #999;
}

.tieba-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-tag {
  background: #f0f0f0;
  color: #666;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.load-more {
  text-align: center;
  padding: 20px 0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #666;
}
</style>