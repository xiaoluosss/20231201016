<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <AppHeader />

    <!-- 主要内容区域 -->
    <main class="app-main">
      <router-view />
    </main>

    <!-- 底部信息 -->
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/vue-components/layout/AppHeader.vue'
import AppFooter from '@/vue-components/layout/AppFooter.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  padding-top: 64px; /* 为固定头部留出空间 */
  min-height: calc(100vh - 64px);
}
</style>