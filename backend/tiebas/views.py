from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import TiebaCategory, Tieba, TiebaMember, TiebaAnnouncement
from .serializers import (
    TiebaCategorySerializer, TiebaSerializer, TiebaCreateSerializer,
    TiebaMemberSerializer, TiebaAnnouncementSerializer
)


class TiebaCategoryViewSet(viewsets.ModelViewSet):
    """贴吧分类视图集"""
    
    queryset = TiebaCategory.objects.filter(status=True)
    serializer_class = TiebaCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TiebaViewSet(viewsets.ModelViewSet):
    """贴吧视图集"""
    
    queryset = Tieba.objects.filter(status=1)  # 只显示正常状态的贴吧
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TiebaCreateSerializer
        return TiebaSerializer
    
    def perform_create(self, serializer):
        """创建贴吧时设置创建者"""
        tieba = serializer.save(owner=self.request.user)
        # 创建者自动成为大吧主
        TiebaMember.objects.create(
            user=self.request.user,
            tieba=tieba,
            role=2,  # 大吧主
            status=1  # 正常
        )
        # 更新贴吧成员数
        tieba.member_count = 1
        tieba.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        """加入贴吧"""
        tieba = self.get_object()
        
        # 检查是否已经是成员
        if TiebaMember.objects.filter(user=request.user, tieba=tieba).exists():
            return Response(
                {'error': '您已经是该贴吧成员'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建成员关系
        TiebaMember.objects.create(
            user=request.user,
            tieba=tieba,
            role=0,  # 普通成员
            status=1  # 正常
        )
        
        # 更新贴吧成员数
        tieba.member_count += 1
        tieba.save()
        
        return Response({'message': '成功加入贴吧'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None):
        """退出贴吧"""
        tieba = self.get_object()
        
        try:
            member = TiebaMember.objects.get(user=request.user, tieba=tieba)
            # 吧主不能退出贴吧
            if member.role >= 1:
                return Response(
                    {'error': '吧主不能退出贴吧，请先转让吧主权限'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            member.delete()
            
            # 更新贴吧成员数
            tieba.member_count -= 1
            tieba.save()
            
            return Response({'message': '成功退出贴吧'})
        except TiebaMember.DoesNotExist:
            return Response(
                {'error': '您不是该贴吧成员'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """推荐贴吧"""
        recommended_tiebas = Tieba.objects.filter(
            is_recommended=True, 
            status=1
        ).order_by('-member_count')[:10]
        serializer = self.get_serializer(recommended_tiebas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索贴吧"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        tiebas = Tieba.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            status=1
        ).order_by('-member_count')
        
        serializer = self.get_serializer(tiebas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """获取贴吧成员列表"""
        tieba = self.get_object()
        members = TiebaMember.objects.filter(tieba=tieba, status=1).order_by('-role', '-post_count')
        serializer = TiebaMemberSerializer(members, many=True)
        return Response(serializer.data)


class TiebaMemberViewSet(viewsets.ModelViewSet):
    """贴吧成员视图集"""
    
    queryset = TiebaMember.objects.filter(status=1)
    serializer_class = TiebaMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        tieba_id = self.request.query_params.get('tieba_id')
        if tieba_id:
            queryset = queryset.filter(tieba_id=tieba_id)
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def promote(self, request, pk=None):
        """提升成员角色"""
        member = self.get_object()
        
        # 检查操作者权限
        operator_member = TiebaMember.objects.get(
            user=request.user, 
            tieba=member.tieba
        )
        
        if operator_member.role < 2:  # 只有大吧主可以操作
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 提升角色
        if member.role < 2:
            member.role += 1
            member.save()
            return Response({'message': '角色提升成功'})
        
        return Response(
            {'error': '已经是最高角色'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def demote(self, request, pk=None):
        """降低成员角色"""
        member = self.get_object()
        
        # 检查操作者权限
        operator_member = TiebaMember.objects.get(
            user=request.user, 
            tieba=member.tieba
        )
        
        if operator_member.role < 2:  # 只有大吧主可以操作
            return Response(
                {'error': '权限不足'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 降低角色
        if member.role > 0:
            member.role -= 1
            member.save()
            return Response({'message': '角色降低成功'})
        
        return Response(
            {'error': '已经是最低角色'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class TiebaAnnouncementViewSet(viewsets.ModelViewSet):
    """贴吧公告视图集"""
    
    queryset = TiebaAnnouncement.objects.all()
    serializer_class = TiebaAnnouncementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        tieba_id = self.request.query_params.get('tieba_id')
        if tieba_id:
            queryset = queryset.filter(tieba_id=tieba_id)
        return queryset
    
    def perform_create(self, serializer):
        """创建公告时设置作者"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_top(self, request, pk=None):
        """切换置顶状态"""
        announcement = self.get_object()
        
        # 检查权限
        try:
            member = TiebaMember.objects.get(
                user=request.user, 
                tieba=announcement.tieba
            )
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
        
        announcement.is_top = not announcement.is_top
        announcement.save()
        
        return Response({'is_top': announcement.is_top})