from django.db import models
from django.conf import settings


class TiebaCategory(models.Model):
    """贴吧分类"""
    
    name = models.CharField('分类名称', max_length=50, unique=True)
    description = models.TextField('分类描述', max_length=500, null=True, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    status = models.BooleanField('状态', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'tieba_category'
        verbose_name = '贴吧分类'
        verbose_name_plural = '贴吧分类'
    
    def __str__(self):
        return self.name


class Tieba(models.Model):
    """贴吧模型"""
    
    STATUS_CHOICES = [
        (0, '待审核'),
        (1, '正常'),
        (2, '封禁'),
        (3, '隐藏'),
    ]
    
    name = models.CharField('贴吧名称', max_length=100, unique=True)
    description = models.TextField('贴吧描述', max_length=1000)
    avatar = models.ImageField('贴吧头像', upload_to='tieba_avatars/', null=True, blank=True)
    banner = models.ImageField('贴吧横幅', upload_to='tieba_banners/', null=True, blank=True)
    
    # 关联字段
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_tiebas',
        verbose_name='创建者'
    )
    category = models.ForeignKey(
        TiebaCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='分类'
    )
    
    # 统计字段
    member_count = models.IntegerField('成员数', default=0)
    post_count = models.IntegerField('帖子数', default=0)
    today_post_count = models.IntegerField('今日帖子数', default=0)
    
    # 管理字段
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    is_recommended = models.BooleanField('是否推荐', default=False)
    
    # 时间字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'tieba'
        verbose_name = '贴吧'
        verbose_name_plural = '贴吧'
    
    def __str__(self):
        return self.name


class TiebaMember(models.Model):
    """贴吧成员"""
    
    ROLE_CHOICES = [
        (0, '普通成员'),
        (1, '小吧主'),
        (2, '大吧主'),
    ]
    
    STATUS_CHOICES = [
        (0, '申请中'),
        (1, '正常'),
        (2, '封禁'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tieba_memberships',
        verbose_name='用户'
    )
    tieba = models.ForeignKey(
        Tieba, 
        on_delete=models.CASCADE, 
        related_name='members',
        verbose_name='贴吧'
    )
    
    role = models.SmallIntegerField('角色', choices=ROLE_CHOICES, default=0)
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    
    # 统计字段
    post_count = models.IntegerField('发帖数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    
    # 时间字段
    joined_at = models.DateTimeField('加入时间', auto_now_add=True)
    last_active_at = models.DateTimeField('最后活跃时间', auto_now=True)
    
    class Meta:
        db_table = 'tieba_member'
        verbose_name = '贴吧成员'
        verbose_name_plural = '贴吧成员'
        unique_together = ('user', 'tieba')
    
    def __str__(self):
        return f'{self.user} - {self.tieba}'


class TiebaAnnouncement(models.Model):
    """贴吧公告"""
    
    tieba = models.ForeignKey(
        Tieba, 
        on_delete=models.CASCADE, 
        related_name='announcements',
        verbose_name='贴吧'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='发布者'
    )
    
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    is_top = models.BooleanField('是否置顶', default=False)
    
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'tieba_announcement'
        verbose_name = '贴吧公告'
        verbose_name_plural = '贴吧公告'
        ordering = ['-is_top', '-created_at']
    
    def __str__(self):
        return self.title