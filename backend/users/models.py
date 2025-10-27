from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""
    
    GENDER_CHOICES = [
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    ]
    
    STATUS_CHOICES = [
        (0, '禁用'),
        (1, '正常'),
        (2, '未激活'),
    ]
    
    # 扩展字段
    phone = models.CharField('手机号', max_length=20, unique=True, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    nickname = models.CharField('昵称', max_length=50, null=True, blank=True)
    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICES, default=0)
    birthday = models.DateField('生日', null=True, blank=True)
    bio = models.TextField('个人简介', max_length=500, null=True, blank=True)
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=1)
    
    # 统计字段
    post_count = models.IntegerField('发帖数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    follower_count = models.IntegerField('粉丝数', default=0)
    following_count = models.IntegerField('关注数', default=0)
    
    # 时间字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    last_login_at = models.DateTimeField('最后登录时间', null=True, blank=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.username or self.nickname or self.phone


class UserFollow(models.Model):
    """用户关注关系"""
    
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following_relationships',
        verbose_name='关注者'
    )
    following = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower_relationships',
        verbose_name='被关注者'
    )
    created_at = models.DateTimeField('关注时间', auto_now_add=True)
    
    class Meta:
        db_table = 'user_follow'
        verbose_name = '用户关注'
        verbose_name_plural = '用户关注'
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f'{self.follower} 关注 {self.following}'