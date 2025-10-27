from django.db import models
from django.conf import settings


class Post(models.Model):
    """帖子模型"""
    
    STATUS_CHOICES = [
        (0, '待审核'),
        (1, '正常'),
        (2, '精华'),
        (3, '置顶'),
        (4, '删除'),
    ]
    
    title = models.CharField('标题', max_length=255)
    content = models.TextField('内容')
    
    # 关联字段
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='作者'
    )
    tieba = models.ForeignKey(
        'tiebas.Tieba', 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='所属贴吧'
    )
    
    # 统计字段
    view_count = models.IntegerField('浏览数', default=0)
    reply_count = models.IntegerField('回复数', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    collect_count = models.IntegerField('收藏数', default=0)
    
    # 管理字段
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    is_top = models.BooleanField('是否置顶', default=False)
    is_essence = models.BooleanField('是否精华', default=False)
    
    # 时间字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    last_reply_at = models.DateTimeField('最后回复时间', null=True, blank=True)
    
    class Meta:
        db_table = 'post'
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-is_top', '-created_at']
    
    def __str__(self):
        return self.title


class PostImage(models.Model):
    """帖子图片"""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='帖子'
    )
    image = models.ImageField('图片', upload_to='post_images/')
    description = models.CharField('描述', max_length=200, null=True, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'post_image'
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片'
        ordering = ['sort_order']
    
    def __str__(self):
        return f'{self.post.title} - 图片'


class PostLike(models.Model):
    """帖子点赞"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='post_likes',
        verbose_name='用户'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name='帖子'
    )
    created_at = models.DateTimeField('点赞时间', auto_now_add=True)
    
    class Meta:
        db_table = 'post_like'
        verbose_name = '帖子点赞'
        verbose_name_plural = '帖子点赞'
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f'{self.user} 点赞 {self.post}'


class PostCollect(models.Model):
    """帖子收藏"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='post_collects',
        verbose_name='用户'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='collects',
        verbose_name='帖子'
    )
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)
    
    class Meta:
        db_table = 'post_collect'
        verbose_name = '帖子收藏'
        verbose_name_plural = '帖子收藏'
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f'{self.user} 收藏 {self.post}'