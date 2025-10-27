from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .models import User, UserFollow
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserProfileSerializer, UserUpdateSerializer, UserFollowSerializer
)


class AuthViewSet(viewsets.ViewSet):
    """认证相关视图"""
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """用户注册"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                'message': '注册成功',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """用户登录"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': '登录成功',
                'user': UserProfileSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """用户登出"""
        logout(request)
        return Response({'message': '登出成功'})


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """关注用户"""
        target_user = self.get_object()
        if target_user == request.user:
            return Response({'error': '不能关注自己'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )
        
        if created:
            return Response({'message': '关注成功'})
        else:
            follow.delete()
            return Response({'message': '取消关注成功'})
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """获取用户的粉丝列表"""
        user = self.get_object()
        followers = UserFollow.objects.filter(following=user)
        serializer = UserFollowSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        """获取用户关注的列表"""
        user = self.get_object()
        following = UserFollow.objects.filter(follower=user)
        serializer = UserFollowSerializer(following, many=True)
        return Response(serializer.data)


class UserFollowViewSet(viewsets.ModelViewSet):
    """用户关注视图集"""
    
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserFollow.objects.filter(follower=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)