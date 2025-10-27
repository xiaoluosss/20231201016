import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 需要登录的路由
const authRoutes = [
  '/settings',
  '/messages',
  '/create-post',
  '/profile'
]

// 需要特定权限的路由
const permissionRoutes = {
  '/admin': ['admin'],
  '/moderator': ['admin', 'moderator']
}

// 检查路由是否需要登录
const requiresAuth = (to) => {
  return authRoutes.some(route => to.path.startsWith(route))
}

// 检查路由是否需要特定权限
const requiresPermission = (to) => {
  for (const [route, permissions] of Object.entries(permissionRoutes)) {
    if (to.path.startsWith(route)) {
      return permissions
    }
  }
  return null
}

// 路由守卫
const routerGuard = (to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 检查是否需要登录
  if (requiresAuth(to)) {
    if (!userStore.isLoggedIn) {
      ElMessage.warning('请先登录')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
  }
  
  // 检查是否需要特定权限
  const requiredPermissions = requiresPermission(to)
  if (requiredPermissions) {
    if (!userStore.isLoggedIn) {
      ElMessage.warning('请先登录')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    const hasPermission = requiredPermissions.some(permission => 
      userStore.hasRole(permission)
    )
    
    if (!hasPermission) {
      ElMessage.error('权限不足')
      next(from.path === '/' ? '/' : from.fullPath)
      return
    }
  }
  
  // 如果已经登录，访问登录/注册页时重定向到首页
  if (userStore.isLoggedIn && (to.path === '/login' || to.path === '/register')) {
    ElMessage.info('您已登录')
    next(from.query.redirect || '/')
    return
  }
  
  next()
}

// 全局前置守卫
export const setupRouterGuard = (router) => {
  router.beforeEach(routerGuard)
}

export default routerGuard