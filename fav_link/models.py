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

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.SlugField(db_index=True, max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "name",
            "owner",
        )

    def __str__(self) -> str:
        return self.name


# Create your models here.
class FavoriteUrl(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="models",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    create_at = models.DateTimeField(auto_now_add=True)
