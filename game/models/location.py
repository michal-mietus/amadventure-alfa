from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField(max_length=20) # range(3-7)
    
    def __str__(self):
        return "Location " + self.name