from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . models import Article
from .models import Article
from ..helpers.serialization_errors import error_dict


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True,
    allow_null=False,# the box for email field should not be empty
        validators=[
            UniqueValidator(
                queryset=Article.objects.all(),
                message=error_dict['already_exist'].format("Article"),
            )
        ],
        error_messages={
            'required': error_dict['required'],
        })#serializers have no variable max_length
    author =  serializers.SerializerMethodField()
    content = serializers.CharField(required=True)
    slug = serializers.CharField(required=True)
    allow_null=False,# the box for email field should not be empty
    validators=[
        UniqueValidator(
                queryset=Article.objects.all(),
                message=error_dict['already_exist'].format("Slug"),
            )
        ],
    @staticmethod#This class is created by def get_author(author)is one of the fields like author above
    def get_author(obj):#method get must bear author.
        return obj.id

    class Meta:
        model = Article#this refers to model class
        fields = ('title','content','author','status', 'slug')
