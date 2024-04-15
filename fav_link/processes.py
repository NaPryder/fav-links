from fav_link.models import FavoriteUrl, Tag, Category
from rest_framework import status
import requests


def get_tag_instances(tags: list[dict], user):

    tag_instances = []
    for tag in tags:
        tag_name = tag.get("name")
        if not tag_name:
            continue
        tag, _ = Tag.objects.get_or_create(name=tag_name, owner=user)
        tag_instances.append(tag)

    return tag_instances


def validity_check(url):

    try:
        res = requests.get(url, timeout=200)
    except Exception as error:
        raise error

    if res.status_code not in [
        status.HTTP_200_OK,
        status.HTTP_206_PARTIAL_CONTENT,
        status.HTTP_301_MOVED_PERMANENTLY,
        status.HTTP_302_FOUND,
    ]:
        raise Exception(f"Invalid URL: {url}")
