from django.db import models
from .location import Location


class Monster(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    def __str__(self):
        repr = self.name
        return repr

    def create_statistics(self):
        statistic_points = level * self.location.difficulty
        for i in range(statistic_points):
            pass
            

