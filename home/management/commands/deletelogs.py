from django.core.management.base import BaseCommand
from home.models import WarcraftlogsAPI
from home import utils

class Command(BaseCommand):
        def handle(self, *args, **options):
                WarcraftlogsAPI.objects.all().delete()