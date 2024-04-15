from django.contrib import admin

from fav_link.models import Tag, Category, FavoriteUrl

# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(FavoriteUrl)
