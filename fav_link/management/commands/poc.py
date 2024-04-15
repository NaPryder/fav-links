from django.core.management import BaseCommand
import requests
from fav_link.models import FavoriteUrl
from django.core.validators import URLValidator
from fav_link.processes import validity_check


class Command(BaseCommand):
    def handle(self, *args, **options):

        print("---args", *args)
        validate = URLValidator()

        url = r"https:/s/stackoverflow.com"
        validate(url)

        print("---valid url")
        validity_check(url)
