from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.TiebaCategoryViewSet)
router.register(r'tiebas', views.TiebaViewSet)
router.register(r'members', views.TiebaMemberViewSet)
router.register(r'announcements', views.TiebaAnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]