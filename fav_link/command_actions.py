from cli.decorators import class_register_commands, register_command
from fav_link.models import FavoriteUrl
from fav_link.serializers import FavoriteUrlSerializer

from django.db import transaction


class DummyRequest:
    def __init__(self, user):
        self.user = user


@class_register_commands
class CommandActions:

    _commands: dict[str, callable] = {}
    _help_commands: dict[str, str] = {}

    def __init__(self, user) -> None:
        self.user = user
        self.request = DummyRequest(user=self.user)

        pass

    @staticmethod
    def get_category_for_serializer(category: str):
        if category:
            return dict(name=category.strip())
        if category is None:
            return None
        else:
            return False

    @staticmethod
    def get_tags_for_serializer(tags: str):
        if not tags:
            return []

        if "," in tags:
            return [dict(name=tag.strip()) for tag in tags.strip().split(",")]
        elif tags:
            return [dict(name=tags.strip())]
        else:
            return []

    @register_command(
        command_keyword="add",
        params="[url (*required)] [title (option)] [category (option)] [tags (option)]",
        description="Add favorite url",
    )
    def add_favorite_url(self, url="", title="", category=None, tags=[], *args):
        if not url:
            print("Required url")
            return

        tags = self.get_tags_for_serializer(tags)
        category = self.get_category_for_serializer(category)
        with transaction.atomic():

            data = dict(url=url, title=title, tags=tags, category=category)

            serializer = FavoriteUrlSerializer(data=data)
            serializer.context["request"] = self.request
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            print("Success")
            self.display_favorite_url_detail(instance)

    @register_command(
        command_keyword="list",
        params="[url (option)] [title (option)] [category (option)] [tags (option)]",
        description="List all favorite url filter by parsed parameters (optional)",
    )
    def list(self, url="", title="", category="", tags="", *args):
        filter_params = dict(owner=self.user)
        if url:
            filter_params["url__icontains"] = url
        if title:
            filter_params["title__icontains"] = title
        if category:
            filter_params["category__name__icontains"] = category
        elif category is None:
            filter_params["category"] = None

        queryset = (
            FavoriteUrl.objects.prefetch_related("tags")
            .select_related("category")
            .filter(**filter_params)
        )
        if tags:
            tags = [tag.strip() for tag in tags.split(",")]
            queryset = queryset.filter(tags__name__in=tags)

        queryset = queryset.order_by("id")

        for item in queryset:
            self.display_favorite_url_detail(item)
            print()

        print(f"Found {queryset.count()} urls")

    @register_command(
        command_keyword="edit",
        params="[id (*required)], [url (option)] [title (option)] [category (option)] [tags (option)]",
        description="Edit url, title, category, tags",
    )
    def edit(self, _id="", url=False, title=False, category=False, tags=[], *args):
        # parameter = False means keeping old value
        # category is None means set category to None

        if not _id:
            print("Required instance id.")
            return

        # validate
        tags = self.get_tags_for_serializer(tags)
        category = self.get_category_for_serializer(category)

        data = dict(url=url)
        if tags:
            data["tags"] = tags
        if category is None or category:
            data["category"] = category

        with transaction.atomic():
            instance = FavoriteUrl.objects.select_for_update().filter(id=_id).last()
            if not instance:
                print(f"Not found instance id {_id}")
                return

            if not url:
                data["url"] = instance.url
            if title:
                data["title"] = title

            print("updating data", data)

            serializer = FavoriteUrlSerializer(instance, data=data, partial=False)
            serializer.context["request"] = self.request
            serializer.is_valid(raise_exception=True)

            serializer.save()
            print("Success")
            self.display_favorite_url_detail(instance)

    @register_command(
        command_keyword="delete",
        params="[id (*required)]",
        description="Delete favorite url by id",
    )
    def delete(self, _id="", *args):
        if not _id:
            print("Required instance id.")
            return

        with transaction.atomic():
            instance = FavoriteUrl.objects.select_for_update().filter(id=_id).last()
            if not instance:
                print(f"Not found instance id {_id}")
                return

            # confirmation
            print("Do you want to delete favorite url?")
            self.display_favorite_url_detail(instance)
            confirm = input("Enter 'y' to confirm: ")
            if confirm.lower() == "y":
                instance.delete()
                print("Deleted")
            else:
                print("Cancel")

    @register_command(
        command_keyword="get",
        params="[id (*required)]",
        description="Get favorite url by id",
    )
    def get_single(self, _id="", *args):
        if not _id:
            print("Required instance id.")
            return

        with transaction.atomic():
            instance = FavoriteUrl.objects.select_for_update().filter(id=_id).last()
            if not instance:
                print(f"Not found instance id {_id}")
                return

            self.display_favorite_url_detail(instance)

    def display_favorite_url_detail(self, favorite_url: FavoriteUrl):

        tags = [tag.name for tag in favorite_url.tags.all()]
        print(f"\tid: {favorite_url.id}")
        print(f"\t   Title: {favorite_url.title}")
        print(f"\t   URL: {favorite_url.url}")
        print(f"\t   Category: {favorite_url.category}")
        print(f"\t   Tags: {', '.join(tags)}")
