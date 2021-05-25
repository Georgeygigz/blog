from rest_framework import serializers
from  .models import Social


class SocialSerializer(serializers.ModelSerializer):

    followee = serializers.CharField()# the box for email field should not be empty by default it true

    follower = serializers.CharField(required=False)#This means not a must to be included.

    class Meta:
        model = Social#this refers to model class
        fields = ('followee','follower')



class FollowerSerializerRetriever(serializers.ModelSerializer):

    # followee = serializers.CharField()# the box for email field should not be empty

    follower = serializers.CharField(required=False)
    # follower = serializers.SerializerMethodField()

    # @staticmethod
    # def get_follower(obj):
    #     from ..authentication.serializers import RegistrationSerializer
    #     user = User.objects.get(email=obj.email)
    #     serializer = RegistrationSerializer(user)
    #     import pdb;pdb.set_trace()


    class Meta:
        model = Social#this refers to model class
        fields = ('follower',)
