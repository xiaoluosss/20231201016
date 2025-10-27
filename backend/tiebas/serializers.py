from rest_framework import serializers
from .models import TiebaCategory, Tieba, TiebaMember, TiebaAnnouncement
from users.models import User


class TiebaCategorySerializer(serializers.ModelSerializer):
    """贴吧分类序列化器"""
    
    class Meta:
        model = TiebaCategory
        fields = ['id', 'name', 'description', 'sort_order', 'status', 'created_at']


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简化序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar']


class TiebaSerializer(serializers.ModelSerializer):
    """贴吧序列化器"""
    
    owner_info = UserSimpleSerializer(source='owner', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_member = serializers.SerializerMethodField()
    member_role = serializers.SerializerMethodField()
    
    class Meta:
        model = Tieba
        fields = [
            'id', 'name', 'description', 'avatar', 'banner', 
            'owner', 'owner_info', 'category', 'category_name',
            'member_count', 'post_count', 'today_post_count',
            'status', 'is_recommended', 'created_at', 'updated_at',
            'is_member', 'member_role'
        ]
        read_only_fields = ['owner', 'member_count', 'post_count', 'today_post_count']
    
    def get_is_member(self, obj):
        """检查当前用户是否为该贴吧成员"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TiebaMember.objects.filter(
                user=request.user, 
                tieba=obj, 
                status=1
            ).exists()
        return False
    
    def get_member_role(self, obj):
        """获取当前用户在该贴吧的角色"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                member = TiebaMember.objects.get(user=request.user, tieba=obj)
                return member.role
            except TiebaMember.DoesNotExist:
                return None
        return None


class TiebaCreateSerializer(serializers.ModelSerializer):
    """贴吧创建序列化器"""
    
    class Meta:
        model = Tieba
        fields = ['name', 'description', 'category']
    
    def validate_name(self, value):
        """验证贴吧名称"""
        if Tieba.objects.filter(name=value).exists():
            raise serializers.ValidationError("贴吧名称已存在")
        return value


class TiebaMemberSerializer(serializers.ModelSerializer):
    """贴吧成员序列化器"""
    
    user_info = UserSimpleSerializer(source='user', read_only=True)
    tieba_name = serializers.CharField(source='tieba.name', read_only=True)
    
    class Meta:
        model = TiebaMember
        fields = [
            'id', 'user', 'user_info', 'tieba', 'tieba_name',
            'role', 'status', 'post_count', 'comment_count',
            'joined_at', 'last_active_at'
        ]
        read_only_fields = ['user', 'tieba', 'post_count', 'comment_count']


class TiebaAnnouncementSerializer(serializers.ModelSerializer):
    """贴吧公告序列化器"""
    
    author_info = UserSimpleSerializer(source='author', read_only=True)
    tieba_name = serializers.CharField(source='tieba.name', read_only=True)
    
    class Meta:
        model = TiebaAnnouncement
        fields = [
            'id', 'tieba', 'tieba_name', 'author', 'author_info',
            'title', 'content', 'is_top', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author']