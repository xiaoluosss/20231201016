<template>
  <div class="messages-page">
    <div class="messages-container">
      <!-- 消息侧边栏 -->
      <div class="messages-sidebar">
        <div class="sidebar-header">
          <h2>消息</h2>
          <el-button type="primary" @click="showNewMessageDialog">
            <el-icon><Plus /></el-icon>
            新消息
          </el-button>
        </div>
        
        <!-- 消息类型筛选 -->
        <div class="message-types">
          <el-radio-group v-model="activeMessageType" @change="filterConversations">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="unread">未读</el-radio-button>
            <el-radio-button label="private">私信</el-radio-button>
            <el-radio-button label="system">系统</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 搜索框 -->
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索对话"
            prefix-icon="Search"
            clearable
            @input="searchConversations"
          />
        </div>
        
        <!-- 对话列表 -->
        <div class="conversation-list">
          <div
            v-for="conversation in filteredConversations"
            :key="conversation.id"
            class="conversation-item"
            :class="{ active: activeConversation?.id === conversation.id }"
            @click="selectConversation(conversation)"
          >
            <div class="avatar-container">
              <el-avatar :size="48" :src="conversation.avatar" />
              <div v-if="conversation.unreadCount > 0" class="unread-badge">
                {{ conversation.unreadCount > 99 ? '99+' : conversation.unreadCount }}
              </div>
            </div>
            
            <div class="conversation-info">
              <div class="conversation-header">
                <span class="username">{{ conversation.username }}</span>
                <span class="time">{{ formatTime(conversation.lastMessageTime) }}</span>
              </div>
              
              <div class="last-message">
                <span class="message-preview">
                  {{ conversation.lastMessage }}
                </span>
                <el-icon v-if="conversation.type === 'system'" class="system-icon">
                  <Bell />
                </el-icon>
              </div>
            </div>
          </div>
          
          <div v-if="filteredConversations.length === 0" class="empty-conversations">
            <el-empty description="暂无消息" />
          </div>
        </div>
      </div>
      
      <!-- 消息内容区域 -->
      <div class="messages-content">
        <div v-if="activeConversation" class="chat-container">
          <!-- 聊天头部 -->
          <div class="chat-header">
            <div class="chat-user-info">
              <el-avatar :size="40" :src="activeConversation.avatar" />
              <div class="user-details">
                <span class="username">{{ activeConversation.username }}</span>
                <span v-if="activeConversation.online" class="online-status">在线</span>
                <span v-else class="online-status offline">离线</span>
              </div>
            </div>
            
            <div class="chat-actions">
              <el-button type="text" @click="showUserProfile(activeConversation.userId)">
                <el-icon><User /></el-icon>
                查看资料
              </el-button>
              <el-button type="text" @click="clearConversation">
                <el-icon><Delete /></el-icon>
                清空记录
              </el-button>
            </div>
          </div>
          
          <!-- 消息列表 -->
          <div class="messages-list" ref="messagesListRef">
            <div
              v-for="message in activeConversation.messages"
              :key="message.id"
              class="message-item"
              :class="{ 'own-message': message.isOwn, 'system-message': message.type === 'system' }"
            >
              <div class="message-avatar">
                <el-avatar :size="32" :src="message.avatar" />
              </div>
              
              <div class="message-content">
                <div class="message-header">
                  <span class="sender-name">{{ message.senderName }}</span>
                  <span class="message-time">{{ formatMessageTime(message.timestamp) }}</span>
                </div>
                
                <div class="message-body">
                  <div v-if="message.type === 'text'" class="text-message">
                    {{ message.content }}
                  </div>
                  
                  <div v-else-if="message.type === 'image'" class="image-message">
                    <el-image
                      :src="message.content"
                      :preview-src-list="[message.content]"
                      fit="cover"
                      class="message-image"
                    />
                  </div>
                  
                  <div v-else-if="message.type === 'system'" class="system-message-content">
                    <el-icon><Bell /></el-icon>
                    <span>{{ message.content }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="activeConversation.messages.length === 0" class="empty-messages">
              <el-empty description="暂无消息记录" />
            </div>
          </div>
          
          <!-- 消息输入框 -->
          <div v-if="activeConversation.type !== 'system'" class="message-input-area">
            <div class="input-toolbar">
              <el-button type="text" @click="toggleEmojiPicker">
                <el-icon><Smile /></el-icon>
              </el-button>
              
              <el-upload
                action="/api/upload/message-image/"
                :show-file-list="false"
                :before-upload="beforeImageUpload"
                :on-success="handleImageUploadSuccess"
              >
                <el-button type="text">
                  <el-icon><Picture /></el-icon>
                </el-button>
              </el-upload>
            </div>
            
            <div class="emoji-picker" v-show="showEmojiPicker">
              <span
                v-for="emoji in emojis"
                :key="emoji"
                class="emoji"
                @click="insertEmoji(emoji)"
              >
                {{ emoji }}
              </span>
            </div>
            
            <div class="input-container">
              <el-input
                v-model="newMessage"
                type="textarea"
                :rows="3"
                placeholder="输入消息..."
                @keydown.enter="sendMessage"
                ref="messageInputRef"
              />
              
              <el-button 
                type="primary" 
                @click="sendMessage" 
                :disabled="!newMessage.trim()"
                class="send-button"
              >
                发送
              </el-button>
            </div>
          </div>
          
          <div v-else class="system-message-notice">
            <p>系统消息无法回复</p>
          </div>
        </div>
        
        <div v-else class="no-conversation-selected">
          <el-empty description="选择一个对话开始聊天" />
        </div>
      </div>
    </div>
    
    <!-- 新消息对话框 -->
    <el-dialog v-model="newMessageDialogVisible" title="发送新消息" width="500px">
      <el-form :model="newMessageForm" label-width="80px">
        <el-form-item label="收件人">
          <el-select
            v-model="newMessageForm.recipientId"
            filterable
            remote
            reserve-keyword
            placeholder="搜索用户"
            :remote-method="searchUsers"
            :loading="searchingUsers"
          >
            <el-option
              v-for="user in searchUserResults"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            >
              <div style="display: flex; align-items: center;">
                <el-avatar :size="24" :src="user.avatar" style="margin-right: 8px;" />
                <span>{{ user.username }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="消息内容">
          <el-input
            v-model="newMessageForm.content"
            type="textarea"
            :rows="4"
            placeholder="输入消息内容..."
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="newMessageDialogVisible = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="sendNewMessage" 
          :disabled="!newMessageForm.recipientId || !newMessageForm.content.trim()"
        >
          发送
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Plus, Search, Bell, User, Delete, Smile, Picture } from '@element-plus/icons-vue'
import api from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const activeMessageType = ref('all')
const searchKeyword = ref('')
const activeConversation = ref(null)
const newMessageDialogVisible = ref(false)
const showEmojiPicker = ref(false)
const newMessage = ref('')
const searchingUsers = ref(false)

// 引用
const messagesListRef = ref(null)
const messageInputRef = ref(null)

// 表单数据
const newMessageForm = reactive({
  recipientId: '',
  content: ''
})

// 模拟数据
const conversations = ref([
  {
    id: 1,
    userId: 2,
    username: '张三',
    avatar: 'https://via.placeholder.com/40',
    type: 'private',
    unreadCount: 3,
    lastMessage: '你好，最近怎么样？',
    lastMessageTime: new Date(Date.now() - 1000 * 60 * 5), // 5分钟前
    online: true,
    messages: [
      {
        id: 1,
        senderId: 2,
        senderName: '张三',
        avatar: 'https://via.placeholder.com/40',
        content: '你好，最近怎么样？',
        type: 'text',
        timestamp: new Date(Date.now() - 1000 * 60 * 5),
        isOwn: false
      }
    ]
  },
  {
    id: 2,
    userId: 3,
    username: '李四',
    avatar: 'https://via.placeholder.com/40',
    type: 'private',
    unreadCount: 0,
    lastMessage: '明天一起吃饭吗？',
    lastMessageTime: new Date(Date.now() - 1000 * 60 * 30), // 30分钟前
    online: false,
    messages: [
      {
        id: 1,
        senderId: 3,
        senderName: '李四',
        avatar: 'https://via.placeholder.com/40',
        content: '明天一起吃饭吗？',
        type: 'text',
        timestamp: new Date(Date.now() - 1000 * 60 * 30),
        isOwn: false
      }
    ]
  },
  {
    id: 3,
    type: 'system',
    username: '系统通知',
    avatar: 'https://via.placeholder.com/40',
    unreadCount: 1,
    lastMessage: '您的帖子获得了10个赞',
    lastMessageTime: new Date(Date.now() - 1000 * 60 * 60), // 1小时前
    online: false,
    messages: [
      {
        id: 1,
        senderId: 0,
        senderName: '系统通知',
        avatar: 'https://via.placeholder.com/40',
        content: '您的帖子获得了10个赞',
        type: 'system',
        timestamp: new Date(Date.now() - 1000 * 60 * 60),
        isOwn: false
      }
    ]
  }
])

const searchUserResults = ref([])

// 表情列表
const emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']

// 计算属性：过滤对话列表
const filteredConversations = ref([])

const filterConversations = () => {
  let filtered = conversations.value
  
  // 按类型筛选
  if (activeMessageType.value !== 'all') {
    filtered = filtered.filter(conv => {
      if (activeMessageType.value === 'unread') {
        return conv.unreadCount > 0
      }
      return conv.type === activeMessageType.value
    })
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    filtered = filtered.filter(conv => 
      conv.username.toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  }
  
  filteredConversations.value = filtered
}

// 搜索对话
const searchConversations = () => {
  filterConversations()
}

// 选择对话
const selectConversation = (conversation) => {
  activeConversation.value = conversation
  
  // 标记为已读
  if (conversation.unreadCount > 0) {
    conversation.unreadCount = 0
  }
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesListRef.value) {
    messagesListRef.value.scrollTop = messagesListRef.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (time) => {
  const now = new Date()
  const messageTime = new Date(time)
  const diff = now - messageTime
  
  if (diff < 1000 * 60) {
    return '刚刚'
  } else if (diff < 1000 * 60 * 60) {
    return Math.floor(diff / (1000 * 60)) + '分钟前'
  } else if (diff < 1000 * 60 * 60 * 24) {
    return Math.floor(diff / (1000 * 60 * 60)) + '小时前'
  } else {
    return messageTime.toLocaleDateString()
  }
}

const formatMessageTime = (time) => {
  const messageTime = new Date(time)
  return messageTime.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 显示新消息对话框
const showNewMessageDialog = () => {
  newMessageDialogVisible.value = true
  newMessageForm.recipientId = ''
  newMessageForm.content = ''
  searchUserResults.value = []
}

// 搜索用户
const searchUsers = async (query) => {
  if (!query.trim()) {
    searchUserResults.value = []
    return
  }
  
  try {
    searchingUsers.value = true
    const response = await api.get(`/users/search/?q=${encodeURIComponent(query)}`)
    searchUserResults.value = response.data
  } catch (error) {
    console.error('搜索用户失败:', error)
    searchUserResults.value = []
  } finally {
    searchingUsers.value = false
  }
}

// 发送新消息
const sendNewMessage = async () => {
  try {
    await api.post('/messages/send/', newMessageForm)
    
    ElMessage.success('消息发送成功')
    newMessageDialogVisible.value = false
    
    // 刷新对话列表
    loadConversations()
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('消息发送失败')
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeConversation.value) return
  
  try {
    const message = {
      id: Date.now(),
      senderId: userStore.user?.id,
      senderName: userStore.user?.username || '我',
      avatar: userStore.user?.avatar || '',
      content: newMessage.value,
      type: 'text',
      timestamp: new Date(),
      isOwn: true
    }
    
    // 添加到消息列表
    activeConversation.value.messages.push(message)
    activeConversation.value.lastMessage = newMessage.value
    activeConversation.value.lastMessageTime = new Date()
    
    // 清空输入框
    newMessage.value = ''
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
    
    // 发送到服务器
    await api.post('/messages/send/', {
      recipientId: activeConversation.value.userId,
      content: message.content
    })
    
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('消息发送失败')
  }
}

// 切换表情选择器
const toggleEmojiPicker = () => {
  showEmojiPicker.value = !showEmojiPicker.value
}

// 插入表情
const insertEmoji = (emoji) => {
  newMessage.value += emoji
  showEmojiPicker.value = false
  
  // 聚焦输入框
  nextTick(() => {
    if (messageInputRef.value) {
      messageInputRef.value.focus()
    }
  })
}

// 图片上传前验证
const beforeImageUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isJPG) {
    ElMessage.error('图片只能是 JPG/PNG 格式!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// 图片上传成功
const handleImageUploadSuccess = (response) => {
  if (activeConversation.value) {
    const message = {
      id: Date.now(),
      senderId: userStore.user?.id,
      senderName: userStore.user?.username || '我',
      avatar: userStore.user?.avatar || '',
      content: response.url,
      type: 'image',
      timestamp: new Date(),
      isOwn: true
    }
    
    activeConversation.value.messages.push(message)
    activeConversation.value.lastMessage = '[图片]'
    activeConversation.value.lastMessageTime = new Date()
    
    nextTick(() => {
      scrollToBottom()
    })
  }
}

// 查看用户资料
const showUserProfile = (userId) => {
  router.push(`/profile/${userId}`)
}

// 清空对话记录
const clearConversation = async () => {
  if (!activeConversation.value) return
  
  try {
    await ElMessageBox.confirm('确定要清空此对话的所有消息记录吗？', '确认清空', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await api.delete(`/messages/conversation/${activeConversation.value.id}/`)
    
    activeConversation.value.messages = []
    ElMessage.success('消息记录已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空消息失败:', error)
      ElMessage.error('清空失败')
    }
  }
}

// 加载对话列表
const loadConversations = async () => {
  try {
    const response = await api.get('/messages/conversations/')
    conversations.value = response.data
    filterConversations()
  } catch (error) {
    console.error('加载对话列表失败:', error)
  }
}

onMounted(() => {
  // 检查用户是否登录
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  loadConversations()
  
  // 初始化过滤
  filterConversations()
})
</script>

<style scoped>
.messages-page {
  height: 100vh;
  background: #f5f5f5;
}

.messages-container {
  display: flex;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background: white;
}

.messages-sidebar {
  width: 350px;
  border-right: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h2 {
  margin: 0;
  color: #333;
}

.message-types {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.search-box {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f8f8f8;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background: #f8f9fa;
}

.conversation-item.active {
  background: #e6f7ff;
}

.avatar-container {
  position: relative;
  margin-right: 12px;
}

.unread-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ff4d4f;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 12px;
  min-width: 18px;
  text-align: center;
}

.conversation-info {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.username {
  font-weight: 600;
  color: #333;
}

.time {
  font-size: 12px;
  color: #999;
}

.last-message {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.message-preview {
  font-size: 14px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.system-icon {
  color: #1890ff;
}

.empty-conversations {
  padding: 40px 20px;
}

.messages-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.chat-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.online-status {
  font-size: 12px;
  color: #52c41a;
}

.online-status.offline {
  color: #999;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  gap: 12px;
}

.message-item.own-message {
  flex-direction: row-reverse;
}

.message-item.system-message {
  justify-content: center;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  max-width: 60%;
}

.own-message .message-content {
  text-align: right;
}

.message-header {
  margin-bottom: 8px;
}

.sender-name {
  font-size: 14px;
  color: #666;
  margin-right: 8px;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-body {
  word-wrap: break-word;
}

.text-message {
  background: #f0f0f0;
  padding: 8px 12px;
  border-radius: 12px;
  display: inline-block;
}

.own-message .text-message {
  background: #1890ff;
  color: white;
}

.image-message {
  max-width: 300px;
}

.message-image {
  width: 100%;
  border-radius: 8px;
  cursor: pointer;
}

.system-message-content {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff7e6;
  padding: 8px 16px;
  border-radius: 6px;
  color: #fa8c16;
  font-size: 14px;
}

.empty-messages {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-input-area {
  border-top: 1px solid #f0f0f0;
  padding: 16px 24px;
}

.input-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.emoji-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-height: 120px;
  overflow-y: auto;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 8px;
}

.emoji {
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
  border-radius: 4px;
}

.emoji:hover {
  background: #e6f7ff;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-container :deep(.el-textarea) {
  flex: 1;
}

.send-button {
  height: 40px;
}

.system-message-notice {
  text-align: center;
  padding: 20px;
  color: #999;
  border-top: 1px solid #f0f0f0;
}

.no-conversation-selected {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .messages-sidebar {
    width: 100%;
  }
  
  .messages-content {
    display: none;
  }
  
  .messages-content.active {
    display: flex;
  }
}
</style>