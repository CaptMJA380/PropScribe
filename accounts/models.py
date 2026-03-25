from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, default='free')
    listing_count = models.IntegerField(default=0)
    provider = models.CharField(max_length=50, default='email')

    def __str__(self):
        return f"{self.user.username} Profile"
