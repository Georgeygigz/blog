from django.urls import path
from .views import CreateArticleAPIView, EditArticleApiView

urlpatterns = [
    path('update/<str:article_id>', EditArticleApiView.as_view(), name='article-update'),
    path('', CreateArticleAPIView.as_view(), name='article'),
]