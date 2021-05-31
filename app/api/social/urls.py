from django.urls import path
from .views import UserFollowAPIView, UserUnfollowApiView

urlpatterns = [
    path('', UserFollowAPIView.as_view(), name='follow'),
    path('unfollow/<str:followee_id>', UserUnfollowApiView.as_view(), name='unfollow'),
]
