"""app URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions

schema_view_ = get_schema_view(
    openapi.Info(
        title="My Awesome blog",
        default_version='v1',
        description="Official documentation for my awesome blog."
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swagger_ui_view = get_swagger_view()

urlpatterns = [
    url(r'^docs/$', schema_view_.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view_.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^redoc/$', schema_view_.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^docs/$', swagger_ui_view),
    path('users/', include(('app.api.authentication.urls', 'authentication'), namespace='authentication')),
    path('article/', include(('app.api.article.urls', 'article'), namespace='article')),
    path('comment/', include(('app.api.comment.urls', 'comment'), namespace='comment')),
    path('social/', include(('app.api.social.urls', 'social'), namespace='social')),
]
