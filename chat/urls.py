from django.urls import path
from . import views

urlpatterns = [
    path('plans/<int:plan_id>/messages/', 
         views.MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='plan-messages'),
]
