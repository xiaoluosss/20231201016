<template>
  <footer class="app-footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>关于我们</h3>
          <p>百度贴吧是全球最大的中文社区，为用户提供基于兴趣关键词的交流平台。</p>
        </div>
        
        <div class="footer-section">
          <h3>联系我们</h3>
          <p>邮箱: contact@tieba.com</p>
          <p>电话: 400-123-4567</p>
        </div>
        
        <div class="footer-section">
          <h3>友情链接</h3>
          <div class="links">
            <a href="#" class="footer-link">百度</a>
            <a href="#" class="footer-link">百度知道</a>
            <a href="#" class="footer-link">百度百科</a>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 百度贴吧. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 底部信息组件逻辑
</script>

<style scoped>
.app-footer {
  background: #f5f5f5;
  border-top: 1px solid #e8e8e8;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 30px;
}

.footer-section h3 {
  margin-bottom: 16px;
  color: #333;
  font-size: 16px;
}

.footer-section p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 8px;
}

.links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-link {
  color: #666;
  text-decoration: none;
}

.footer-link:hover {
  color: #1890ff;
}

.footer-bottom {
  border-top: 1px solid #e8e8e8;
  padding-top: 20px;
  text-align: center;
  color: #999;
}
</style>