from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . models import Article
from .models import Article
from ..helpers.serialization_errors import error_dict
from ..comment.serializers import CommentRetrieveSerializer, Comment


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True,
    allow_null=False,# the box for email field will not be empty
        validators=[
            UniqueValidator(
                queryset=Article.objects.all(),
                message=error_dict['already_exist'].format("Article"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
        })#serializers have no variable max_length
    author =  serializers.CharField(required=False)
    content = serializers.CharField(required=True)
    slug = serializers.CharField(required=True)


    class Meta:
        model = Article#this refers to model class
        fields = ('title','content','author','status', 'slug', 'created_at')

#This serializer class is used by get at views, where one article is retrieved. We did this to solve the error of
#list is not collable when we used comment, and because the ArticleSerializer is used by other, creating a new
# one would save us fromt the error.
class ArticleRetrieverSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()#Add this a new field, to handle comments. Thies will help
    #retrieve comments tied to their articles.It's a field that was not there initially.This is the way to include it.
    #Note when hitting any getting endpoint,
    #====>The fields are those not in models(custom fields/special),


    #In this case we are retrieving comment for each article post.
    #Comments are in a foreign model, for us to attach this comments to our article, we need to create an instance
    #of comment like this: comments = serializers.SerializerMethodField(), this is always followed by a
    #@staticmethod like below and now our retrieved comments are joined to our article.
    @staticmethod
    def get_comments(obj):
        comments =  Comment.objects.filter(article_id=obj.id)#This object stands for the current object/instance
        serializer = CommentRetrieveSerializer(comments, many=True)#many=true means all comments for an article are retrieved.
        return serializer.data

    #All the fields below should be in this class, if the fields are missing, they should be models
    #eg= status, author. Fields found in models
    class Meta:
        model =  Article#this refers to model class
        fields = ('title','content','author','status', 'slug','comments')
