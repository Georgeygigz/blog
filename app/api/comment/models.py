from django.db import models
from ..authentication.models import User
from ..article.models import Article
from app.api.models import BaseModel

# Create your models here.

class Comment(BaseModel):#author ids the one currently logged-in.
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')#the author here already has an account
    #and ID is used(remember you don't register 1st to comment, your ID links your registaration details)
    comment = models.CharField(max_length=200)#here the field is charfield() without min/max. to let the author space of the space they want.
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name='article')#here again, the article id used to relate.

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.comment
