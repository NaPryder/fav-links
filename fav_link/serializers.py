from django.forms import ValidationError
from rest_framework import serializers, exceptions

from fav_link.models import FavoriteUrl, Tag, Category

from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "owner", "create_at", "url"]
        read_only_fields = ["id", "owner", "create_at", "url"]

    def validate_name(self, name):
        request = self.context.get("request")
        existing_name = self.Meta.model.objects.filter(
            owner=request.user, name=name
        ).last()
        if existing_name:
            raise ValidationError(f"Existing category name: {existing_name}")

        return name


class TagSerializer(serializers.ModelSerializer):
    name = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ["id", "name", "owner", "create_at"]
        read_only_fields = ["id", "owner", "create_at"]

    def validate_name(self, name):
        print("---validate tag name in se")
        request = self.context.get("request")
        existing_name = self.Meta.model.objects.filter(
            owner=request.user, name=name
        ).last()
        if existing_name:
            raise ValidationError(f"Existing tag name: {existing_name}")

        return name


class ListTagSerializer(serializers.ModelSerializer):
    name = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ["name"]


class FavoriteUrlSerializer(serializers.ModelSerializer):

    # tags = TagSerializer(many=True)
    tags = ListTagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = FavoriteUrl
        fields = ["url", "title", "owner", "tags", "category", "create_at"]
        read_only_fields = ["create_at", "owner"]

    def validate(self, attrs):

        tags = attrs["tags"]
        print("---tags", tags)
        # validate tags

        # raise ValidationError("error")

        return attrs

    def create(self, validated_data):  # create method
        # tags = self.initial_data["tags"]
        tags = validated_data.pop("tags")
        request = self.context.get("request")
        user = request.user

        # get or create tag
        tag_instances = []
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(name=tag["name"], owner=user)
            tag_instances.append(tag)

        # create favorite url instance
        fav_url = FavoriteUrl.objects.create(**validated_data, owner=user)
        fav_url.tags.set(tag_instances)
        return fav_url
