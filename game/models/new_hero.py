from django.db import models
from django.contrib.auth.models import User


class NewHero(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    
    def __str__(self):
        repr = "Hero " + self.name
        return repr
