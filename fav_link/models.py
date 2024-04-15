from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "name",
            "owner",
        )


class Tag(models.Model):
    name = models.SlugField(db_index=True, max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "name",
            "owner",
        )


# Create your models here.
class FavoriteUrl(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="models"
    )
    tags = models.ManyToManyField(Tag)
    create_at = models.DateTimeField(auto_now_add=True)
