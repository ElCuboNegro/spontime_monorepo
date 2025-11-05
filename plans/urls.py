from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plans', views.PlanViewSet, basename='plan')
router.register(r'tags', views.InterestTagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
