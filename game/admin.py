from django.contrib import admin
from .models.hero import Hero
from .models.item import Item
from .models.location import Location
from .models.action import Action
from .models.statistic import Statistic


admin.site.register(Hero)
admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Action)
admin.site.register(Statistic)
