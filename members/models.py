from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self) -> str:
        return str(self.user)