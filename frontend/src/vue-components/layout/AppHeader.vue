<template>
  <header class="app-header">
    <div class="header-container">
      <!-- Logo -->
      <div class="logo">
        <router-link to="/" class="logo-link">
          <span class="logo-text">百度贴吧</span>
        </router-link>
      </div>

      <!-- 搜索框 -->
      <div class="search-box">
        <input 
          v-model="searchKeyword" 
          type="text" 
          placeholder="搜索贴吧、帖子、用户..." 
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <button class="search-btn" @click="handleSearch">
          <i class="search-icon">🔍</i>
        </button>
      </div>

      <!-- 导航菜单 -->
      <nav class="nav-menu">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/tiebas" class="nav-item">贴吧</router-link>
        <router-link to="/" class="nav-item">热门</router-link>
      </nav>

      <!-- 用户操作区域 -->
      <div class="user-actions">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32" :src="userStore.user?.avatar" />
              <span class="username">{{ userStore.user?.nickname || userStore.user?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToProfile">个人中心</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="$router.push('/login')" size="small">登录</el-button>
          <el-button @click="$router.push('/register')" size="small">注册</el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    // 实现搜索逻辑
    console.log('搜索关键词:', searchKeyword.value)
  }
}

const goToProfile = () => {
  if (userStore.user) {
    router.push(`/user/${userStore.user.id}`)
  }
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  z-index: 1000;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  margin-right: 40px;
}

.logo-link {
  text-decoration: none;
  color: #1890ff;
  font-size: 24px;
  font-weight: bold;
}

.search-box {
  flex: 1;
  max-width: 400px;
  display: flex;
  margin-right: 40px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px 0 0 4px;
  outline: none;
}

.search-input:focus {
  border-color: #1890ff;
}

.search-btn {
  padding: 8px 16px;
  background: #1890ff;
  border: 1px solid #1890ff;
  border-radius: 0 4px 4px 0;
  color: white;
  cursor: pointer;
}

.nav-menu {
  display: flex;
  margin-right: 40px;
}

.nav-item {
  margin: 0 16px;
  text-decoration: none;
  color: #333;
  font-size: 14px;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #1890ff;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #333;
}
</style>