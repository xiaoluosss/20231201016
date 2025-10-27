from rest_framework import serializers
from .models import Post, PostImage, PostLike, PostCollect
from users.models import User
from tiebas.models import Tieba


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简化序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar']


class TiebaSimpleSerializer(serializers.ModelSerializer):
    """贴吧简化序列化器"""
    
    class Meta:
        model = Tieba
        fields = ['id', 'name', 'avatar']


class PostImageSerializer(serializers.ModelSerializer):
    """帖子图片序列化器"""
    
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'description', 'sort_order']


class PostSerializer(serializers.ModelSerializer):
    """帖子序列化器"""
    
    author_info = UserSimpleSerializer(source='author', read_only=True)
    tieba_info = TiebaSimpleSerializer(source='tieba', read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'author_info', 
            'tieba', 'tieba_info', 'view_count', 'reply_count', 
            'like_count', 'collect_count', 'status', 'is_top', 
            'is_essence', 'created_at', 'updated_at', 'last_reply_at',
            'images', 'is_liked', 'is_collected'
        ]
        read_only_fields = ['author', 'view_count', 'reply_count', 'like_count', 'collect_count']
    
    def get_is_liked(self, obj):
        """检查当前用户是否点赞了该帖子"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False
    
    def get_is_collected(self, obj):
        """检查当前用户是否收藏了该帖子"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostCollect.objects.filter(user=request.user, post=obj).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """帖子创建序列化器"""
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tieba', 'images']
    
    def validate(self, attrs):
        """验证帖子数据"""
        # 检查用户是否是该贴吧成员
        request = self.context.get('request')
        tieba = attrs.get('tieba')
        
        if request and request.user.is_authenticated:
            from tiebas.models import TiebaMember
            if not TiebaMember.objects.filter(user=request.user, tieba=tieba, status=1).exists():
                raise serializers.ValidationError("您不是该贴吧成员，无法发帖")
        
        return attrs
    
    def create(self, validated_data):
        """创建帖子"""
        images = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        
        # 创建帖子图片
        for i, image in enumerate(images):
            PostImage.objects.create(
                post=post,
                image=image,
                sort_order=i
            )
        
        # 更新贴吧帖子统计
        tieba = post.tieba
        tieba.post_count += 1
        tieba.today_post_count += 1
        tieba.save()
        
        return post


class PostLikeSerializer(serializers.ModelSerializer):
    """帖子点赞序列化器"""
    
    user_info = UserSimpleSerializer(source='user', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'user_info', 'post', 'post_title', 'created_at']
        read_only_fields = ['user', 'post']


class PostCollectSerializer(serializers.ModelSerializer):
    """帖子收藏序列化器"""
    
    user_info = UserSimpleSerializer(source='user', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = PostCollect
        fields = ['id', 'user', 'user_info', 'post', 'post_title', 'created_at']
        read_only_fields = ['user', 'post']