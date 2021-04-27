from django.shortcuts import render
from rest_framework import status
from rest_framework import generics, mixins
from ..helpers.renderers import RequestJSONRenderer
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Article
from rest_framework.serializers import ValidationError


# Create your views here.
class CreateArticleAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request):
        """
        Handle user posts
        """
        article = request.data

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user)
        data = serializer.data
        return_message = {
            "message":"Article created successfully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_201_CREATED)


class EditArticleApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)#AllowAny here if logged in or not logged in you are allowed to comment.
    serializer_class = ArticleSerializer

    def patch(self, request, article_id):#patch mostly is updating
        article = Article.objects.get(pk=article_id)
        data = request.data

        serializer = self.serializer_class(article, data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return_message = {
            "message":"Article updated successfully",
            "data": serializer.data
        }

        return Response(return_message, status=status.HTTP_201_CREATED)


    def get(self, request, article_id):
        # import pdb;pdb.set_trace()
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise ValidationError(
                "This Article does not exist",
            )

        serializer = self.serializer_class(article)
        data = serializer.data

        return_message = {
            "message":"Article retrieved succefully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_200_OK)





    def delete(self, request, article_id):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise ValidationError(
                "The article you want to delete does not exist"
            )

        article.delete()
        serializer = self.serializer_class(article)
        data = serializer.data

        return_message = {
            "message":"Article deleted succefully",
            "data":serializer.data#shows the article that is deleted
        }
        return Response(return_message, status=status.HTTP_200_OK)

