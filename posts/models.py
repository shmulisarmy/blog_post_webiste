from django.db import models

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=30)
    text = models.TextField(max_length=280, null=False)

    def __str__(self):
        return f"id: {self.id}, author: {self.author}, text  {self.text},"

class Comment(models.Model):
    author = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    on_post = models.IntegerField()

    def __str__(self):
        on_post = Post.objects.filter(id=self.on_post).first()
        return f"author: {self.author}, content: {self.content} on_post: {on_post}"
