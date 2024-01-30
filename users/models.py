from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=16, blank=True)  #
    email = models.EmailField()


    def __str__(self):
        return f"username: {self.username}\n password: {self.password}\n email: {self.email}"
    

class Profile(models.Model):
    username = models.CharField(max_length=30)
    bio = models.TextField()
    following = models.ManyToManyField("self", blank=True, related_name="followers")
    followers = models.ManyToManyField("self", blank=True, related_name="following")
    followers_amount = models.IntegerField(default=0)
    following_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"username: {self.username}\n following_amount: {self.following_amount}\n followers_amount: {self.followers_amount}"
    