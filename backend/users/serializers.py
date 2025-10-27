from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserFollow


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password_confirm', 'nickname']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次密码不一致")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户已被禁用')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('用户名和密码必须提供')


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'nickname', 
            'avatar', 'gender', 'birthday', 'bio',
            'post_count', 'comment_count', 'follower_count', 'following_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'gender', 'birthday', 'bio']


class UserFollowSerializer(serializers.ModelSerializer):
    """用户关注序列化器"""
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    following_username = serializers.CharField(source='following.username', read_only=True)
    
    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'follower_username', 'following_username', 'created_at']
        read_only_fields = ['id', 'created_at']