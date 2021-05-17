from django.shortcuts import render
from rest_framework import status
from rest_framework import generics, mixins
from ..helpers.renderers import RequestJSONRenderer
from .serializers import CommentSerializer,Comment
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Article
from rest_framework.serializers import ValidationError


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = CommentSerializer

    def post(self, request):
        """
        Handle user creating comments
        """
        comment = request.data

        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        article_id=request.data['article']
        article = Article.objects.get(pk=article_id)
        serializer.save(author=request.user, article=article)#user is a method in class request, and one currently logged in.
        #the tokens generated was unique depeding with who is logged in.
        data = serializer.data
        return_message = {
            "message":"Comment created successfully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_201_CREATED)


    def get(self, request):
        comment = Comment.objects.all()
        serializer = self.serializer_class(comment, many=True)
        return_message = {
            "message":"comment gotten successfully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_200_OK)


class EditCommentApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)#AllowAny here if logged in or not logged in you are allowed to comment.
    serializer_class = CommentSerializer

    def patch(self, request, comment_id):#patch mostly is updating
        comment = Article.objects.get(pk=comment_id)
        data = request.data

        serializer = self.serializer_class(comment, data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return_message = {
            "message":"Comment updated successfully",
            "data": serializer.data
        }

        return Response(return_message, status=status.HTTP_201_CREATED)


    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise ValidationError(
                "This Comment does not exist",
            )

        serializer = self.serializer_class(comment)
        data = serializer.data

        return_message = {
            "message":"Comment retrieved succefully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_200_OK)



    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise ValidationError(
                "The comment you want to delete does not exist"
            )

        comment.delete()
        serializer = self.serializer_class(comment)
        data = serializer.data

        return_message = {
            "message":"Comment deleted succefully",
            "data":serializer.data#shows the comment that is deleted
        }
        return Response(return_message, status=status.HTTP_200_OK)
