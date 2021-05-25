from django.urls import path
from .views import FollowAPIView

urlpatterns = [
    path('', FollowAPIView.as_view(), name='follow_api'),
]
