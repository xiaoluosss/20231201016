from django.db import models
from django.conf import settings


class Comment(models.Model):
    """评论模型"""
    
    STATUS_CHOICES = [
        (0, '待审核'),
        (1, '正常'),
        (2, '删除'),
    ]
    
    content = models.TextField('内容')
    
    # 关联字段
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='作者'
    )
    post = models.ForeignKey(
        'posts.Post', 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='帖子'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        verbose_name='父评论'
    )
    
    # 楼层信息
    floor_number = models.IntegerField('楼层', default=1)
    
    # 统计字段
    like_count = models.IntegerField('点赞数', default=0)
    reply_count = models.IntegerField('回复数', default=0)
    
    # 管理字段
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    
    # 时间字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['floor_number']
    
    def __str__(self):
        return f'{self.author} 评论: {self.content[:50]}'


class CommentLike(models.Model):
    """评论点赞"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comment_likes',
        verbose_name='用户'
    )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name='评论'
    )
    created_at = models.DateTimeField('点赞时间', auto_now_add=True)
    
    class Meta:
        db_table = 'comment_like'
        verbose_name = '评论点赞'
        verbose_name_plural = '评论点赞'
        unique_together = ('user', 'comment')
    
    def __str__(self):
        return f'{self.user} 点赞评论'


class CommentImage(models.Model):
    """评论图片"""
    
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='评论'
    )
    image = models.ImageField('图片', upload_to='comment_images/')
    sort_order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'comment_image'
        verbose_name = '评论图片'
        verbose_name_plural = '评论图片'
        ordering = ['sort_order']
    
    def __str__(self):
        return f'{self.comment} - 图片'