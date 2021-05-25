from django.db import models
from ..authentication.models import User
from app.api.models import BaseModel


class Social(BaseModel):
    #Here to be a followee/r you must be in the user table ie you have an account
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')