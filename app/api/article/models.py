from django.db import models
from ..authentication.models import User
from app.api.models import BaseModel


# Create your models here.
STATUS = (
    (0, "Draft"),
    (1, "Publish"))

class Article(BaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug =  models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    content =  models.TextField()
    status =  models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
