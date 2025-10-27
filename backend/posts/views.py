from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, PostImage, PostLike, PostCollect
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    PostLikeSerializer, PostCollectSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """帖子视图集"""
    
    queryset = Post.objects.filter(status=1)  # 只显示正常状态的帖子
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        
        # 按贴吧过滤
        tieba_id = self.request.query_params.get('tieba_id')
        if tieba_id:
            queryset = queryset.filter(tieba_id=tieba_id)
        
        # 按作者过滤
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # 按状态过滤
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset.order_by('-is_top', '-created_at')
    
    def perform_create(self, serializer):
        """创建帖子时设置作者"""
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """获取帖子详情时增加浏览数"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """点赞帖子"""
        post = self.get_object()
        
        # 检查是否已经点赞
        if PostLike.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'error': '您已经点赞过该帖子'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建点赞记录
        PostLike.objects.create(user=request.user, post=post)
        
        # 更新帖子点赞数
        post.like_count += 1
        post.save()
        
        return Response({'message': '点赞成功', 'like_count': post.like_count})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """取消点赞"""
        post = self.get_object()
        
        try:
            like = PostLike.objects.get(user=request.user, post=post)
            like.delete()
            
            # 更新帖子点赞数
            post.like_count -= 1
            post.save()
            
            return Response({'message': '取消点赞成功', 'like_count': post.like_count})
        except PostLike.DoesNotExist:
            return Response(
                {'error': '您还没有点赞过该帖子'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def collect(self, request, pk=None):
        """收藏帖子"""
        post = self.get_object()
        
        # 检查是否已经收藏
        if PostCollect.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'error': '您已经收藏过该帖子'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建收藏记录
        PostCollect.objects.create(user=request.user, post=post)
        
        # 更新帖子收藏数
        post.collect_count += 1
        post.save()
        
        return Response({'message': '收藏成功', 'collect_count': post.collect_count})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def uncollect(self, request, pk=None):
        """取消收藏"""
        post = self.get_object()
        
        try:
            collect = PostCollect.objects.get(user=request.user, post=post)
            collect.delete()
            
            # 更新帖子收藏数
            post.collect_count -= 1
            post.save()
            
            return Response({'message': '取消收藏成功', 'collect_count': post.collect_count})
        except PostCollect.DoesNotExist:
            return Response(
                {'error': '您还没有收藏过该帖子'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_top(self, request, pk=None):
        """设置帖子置顶"""
        post = self.get_object()
        
        # 检查权限
        try:
            from tiebas.models import TiebaMember
            member = TiebaMember.objects.get(user=request.user, tieba=post.tieba)
            if member.role < 1:  # 只有吧主可以操作
                return Response(
                    {'error': '权限不足'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        except TiebaMember.DoesNotExist:
            return Response(
                {'error': '您不是该贴吧成员'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.is_top = not post.is_top
        post.save()
        
        return Response({'is_top': post.is_top})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def set_essence(self, request, pk=None):
        """设置帖子精华"""
        post = self.get_object()
        
        # 检查权限
        try:
            from tiebas.models import TiebaMember
            member = TiebaMember.objects.get(user=request.user, tieba=post.tieba)
            if member.role < 1:  # 只有吧主可以操作
                return Response(
                    {'error': '权限不足'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        except TiebaMember.DoesNotExist:
            return Response(
                {'error': '您不是该贴吧成员'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.is_essence = not post.is_essence
        post.save()
        
        return Response({'is_essence': post.is_essence})


class PostLikeViewSet(viewsets.ModelViewSet):
    """帖子点赞视图集"""
    
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        
        # 只返回当前用户的点赞记录
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset


class PostCollectViewSet(viewsets.ModelViewSet):
    """帖子收藏视图集"""
    
    queryset = PostCollect.objects.all()
    serializer_class = PostCollectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        
        # 只返回当前用户的收藏记录
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset