from rest_framework import serializers
from .models import Comment, CommentLike, CommentImage
from users.models import User
from posts.models import Post


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简化序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar']


class PostSimpleSerializer(serializers.ModelSerializer):
    """帖子简化序列化器"""
    
    class Meta:
        model = Post
        fields = ['id', 'title']


class CommentImageSerializer(serializers.ModelSerializer):
    """评论图片序列化器"""
    
    class Meta:
        model = CommentImage
        fields = ['id', 'image', 'sort_order']


class CommentReplySerializer(serializers.ModelSerializer):
    """评论回复序列化器"""
    
    author_info = UserSimpleSerializer(source='author', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_info', 'parent',
            'floor_number', 'like_count', 'reply_count', 'status',
            'created_at', 'updated_at', 'is_liked'
        ]
        read_only_fields = ['author', 'floor_number', 'like_count', 'reply_count']
    
    def get_is_liked(self, obj):
        """检查当前用户是否点赞了该评论"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    
    author_info = UserSimpleSerializer(source='author', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    replies = CommentReplySerializer(many=True, read_only=True)
    images = CommentImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_info', 'post', 'post_title',
            'parent', 'floor_number', 'like_count', 'reply_count', 'status',
            'created_at', 'updated_at', 'replies', 'images', 'is_liked'
        ]
        read_only_fields = ['author', 'floor_number', 'like_count', 'reply_count']
    
    def get_is_liked(self, obj):
        """检查当前用户是否点赞了该评论"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['content', 'post', 'parent', 'images']
    
    def validate(self, attrs):
        """验证评论数据"""
        post = attrs.get('post')
        parent = attrs.get('parent')
        
        # 如果parent存在，确保parent的post与当前post一致
        if parent and parent.post != post:
            raise serializers.ValidationError("回复的评论必须属于同一个帖子")
        
        return attrs
    
    def create(self, validated_data):
        """创建评论"""
        images = validated_data.pop('images', [])
        comment = Comment.objects.create(**validated_data)
        
        # 创建评论图片
        for i, image in enumerate(images):
            CommentImage.objects.create(
                comment=comment,
                image=image,
                sort_order=i
            )
        
        # 更新帖子回复数
        post = comment.post
        post.reply_count += 1
        post.last_reply_at = comment.created_at
        post.save()
        
        # 如果是对评论的回复，更新父评论的回复数
        if comment.parent:
            comment.parent.reply_count += 1
            comment.parent.save()
        
        return comment


class CommentLikeSerializer(serializers.ModelSerializer):
    """评论点赞序列化器"""
    
    user_info = UserSimpleSerializer(source='user', read_only=True)
    comment_content = serializers.CharField(source='comment.content', read_only=True)
    
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'user_info', 'comment', 'comment_content', 'created_at']
        read_only_fields = ['user', 'comment']