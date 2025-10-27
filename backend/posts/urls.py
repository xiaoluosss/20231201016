from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'likes', views.PostLikeViewSet)
router.register(r'collects', views.PostCollectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]