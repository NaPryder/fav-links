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
    title = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    tags = ListTagSerializer(many=True, allow_null=True, required=False)
    category = UrlCategorySerializer(allow_null=True, required=False)

    class Meta:
        model = FavoriteUrl
        fields = ["id", "url", "title", "owner", "tags", "category", "create_at"]
        read_only_fields = ["id", "create_at", "owner"]

    def validate_category(self, category: dict):
        if category is None:
            return category

        name = category.get("name")
        if not name:
            raise ValidationError("not found category name")

        return category

    def validate_url(self, url):
        from fav_link.processes import validity_check

        # validity check
        if url:
            try:
                validity_check(url)
            except Exception as error:
                raise ValidationError(str(error))

            if str(url).endswith("\\") or str(url).endswith("/"):
                url = url[:-1]

        return url

    def validate(self, attrs):

        request = self.context.get("request")

        category = attrs.get("category")

        # validate category
        if isinstance(category, dict) and (name := category.get("name")):
            instance, _ = Category.objects.get_or_create(name=name, owner=request.user)
            attrs["category"] = instance

        return attrs

    def create(self, validated_data):  # create method
        from fav_link.processes import get_tag_instances

        request = self.context.get("request")
        user = request.user

        # get or create tag
        tag_instances = []
        if "tags" in validated_data:
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
        if "tags" in validated_data:
            tags = validated_data.pop("tags")
            tag_instances = get_tag_instances(tags, user)
            instance.tags.set(tag_instances)

        # set updating value
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance
