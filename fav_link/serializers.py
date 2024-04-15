from django.forms import ValidationError
from rest_framework import serializers

from fav_link.models import FavoriteUrl, Tag, Category


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


class UrlCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        return super().validate(attrs)


class FavoriteUrlSerializer(serializers.ModelSerializer):

    url = serializers.URLField()
    tags = ListTagSerializer(many=True)
    category = UrlCategorySerializer()

    class Meta:
        model = FavoriteUrl
        fields = ["id", "url", "title", "owner", "tags", "category", "create_at"]
        read_only_fields = ["id", "create_at", "owner"]

    def validate_category(self, category: dict):
        name = category.get("name")
        if not name:
            raise ValidationError("not found category name")

        return category

    def validate(self, attrs):
        from fav_link.processes import validity_check

        request = self.context.get("request")

        url = attrs["url"]
        category = attrs["category"]

        # validity check
        try:
            validity_check(url)
        except Exception as error:
            return ValidationError(str(error))

        # validate category
        instance = Category.objects.filter(
            name=category["name"], owner=request.user
        ).last()
        if not instance:
            raise ValidationError("not found category name")

        print("  category instance", instance)
        attrs["category"] = instance

        # raise ValidationError("error")

        return attrs

    def create(self, validated_data):  # create method
        from fav_link.processes import get_tag_instances

        request = self.context.get("request")
        user = request.user

        # get or create tag
        tags = validated_data.pop("tags")
        tag_instances = get_tag_instances(tags, user)

        # create favorite url instance
        instance = FavoriteUrl.objects.create(**validated_data, owner=user)
        instance.tags.set(tag_instances)

        return instance

    def update(self, instance, validated_data):
        from fav_link.processes import get_tag_instances

        request = self.context.get("request")
        user = request.user

        # get or create tag
        tags = validated_data.pop("tags")
        tag_instances = get_tag_instances(tags, user)

        # set updating value
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.tags.set(tag_instances)

        return instance
