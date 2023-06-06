from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(BarCategory)
admin.site.register(BarSubCategory)
admin.site.register(Beverage)
admin.site.register(Cocktail)
admin.site.register(CocktailBeverage)
admin.site.register(CocktailStep)
admin.site.register(BarArchive)
admin.site.register(BarTab)
admin.site.register(BarTabItem)
admin.site.register(Thread)
admin.site.register(Comment)
