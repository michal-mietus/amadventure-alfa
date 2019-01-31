from django.contrib import admin
from .models.hero import Hero
from .models.item import Item
from .models.location import Location
from .models.action import Action
from .models.statistic import Statistic
from .models.statistic import HeroStatistic
from .models.statistic import ItemStatistic


admin.site.register(Hero)
admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Action)
admin.site.register(Statistic)
admin.site.register(HeroStatistic)
admin.site.register(ItemStatistic)
