from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserFollow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """自定义用户管理界面"""
    
    list_display = [
        'username', 'nickname', 'phone', 'email', 
        'gender', 'status', 'post_count', 'created_at'
    ]
    list_filter = ['gender', 'status', 'is_staff', 'is_superuser']
    search_fields = ['username', 'nickname', 'phone', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': (
                'phone', 'avatar', 'nickname', 'gender', 
                'birthday', 'bio', 'status'
            )
        }),
        ('统计信息', {
            'fields': (
                'post_count', 'comment_count', 
                'follower_count', 'following_count'
            )
        }),
    )


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """用户关注管理"""
    
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']