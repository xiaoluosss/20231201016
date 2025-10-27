from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Comment, CommentLike, CommentImage
from .serializers import (
    CommentSerializer, CommentCreateSerializer, 
    CommentLikeSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    
    queryset = Comment.objects.filter(status=1)  # 只显示正常状态的评论
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        
        # 按帖子过滤
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # 按作者过滤
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # 只显示顶级评论（parent为None）
        if self.request.query_params.get('top_level') == 'true':
            queryset = queryset.filter(parent__isnull=True)
        
        return queryset.order_by('floor_number')
    
    def perform_create(self, serializer):
        """创建评论时设置作者和楼层号"""
        post = serializer.validated_data.get('post')
        parent = serializer.validated_data.get('parent')
        
        # 如果是顶级评论，计算楼层号
        if not parent:
            last_comment = Comment.objects.filter(post=post, parent__isnull=True).order_by('-floor_number').first()
            floor_number = last_comment.floor_number + 1 if last_comment else 1
        else:
            floor_number = parent.floor_number  # 回复使用父评论的楼层号
        
        serializer.save(author=self.request.user, floor_number=floor_number)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """点赞评论"""
        comment = self.get_object()
        
        # 检查是否已经点赞
        if CommentLike.objects.filter(user=request.user, comment=comment).exists():
            return Response(
                {'error': '您已经点赞过该评论'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建点赞记录
        CommentLike.objects.create(user=request.user, comment=comment)
        
        # 更新评论点赞数
        comment.like_count += 1
        comment.save()
        
        return Response({'message': '点赞成功', 'like_count': comment.like_count})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """取消点赞"""
        comment = self.get_object()
        
        try:
            like = CommentLike.objects.get(user=request.user, comment=comment)
            like.delete()
            
            # 更新评论点赞数
            comment.like_count -= 1
            comment.save()
            
            return Response({'message': '取消点赞成功', 'like_count': comment.like_count})
        except CommentLike.DoesNotExist:
            return Response(
                {'error': '您还没有点赞过该评论'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """获取评论的回复列表"""
        comment = self.get_object()
        replies = Comment.objects.filter(parent=comment, status=1).order_by('created_at')
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)


class CommentLikeViewSet(viewsets.ModelViewSet):
    """评论点赞视图集"""
    
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        
        # 只返回当前用户的点赞记录
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset