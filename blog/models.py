from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Blog(models.Model):
    title=models.CharField( max_length=50)
    body=models.TextField(max_length=5000)
    picture=models.ImageField(upload_to='blogpicture/')
    created_on=models.DateTimeField( auto_now_add=True)
    updated_on=models.DateTimeField( auto_now=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment_by=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.TextField(max_length=100)
    def __str__(self):
        return self.blog.title
    
class Like(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,default="")
    liked_by=models.OneToOneField(User, on_delete=models.CASCADE)
    like=models.BooleanField(default=True)

    def __str__(self):
        return self.blog.title
    

class Tag(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag_content=models.CharField(max_length=100)

    def __str__(self):
        return self.blog.title


