from django.core.management.base import BaseCommand
from home import utils

class Command(BaseCommand):
        def handle(self, *args, **options):
                client = utils.RealmStatusClient()
                data = client.fetch()
                utils.create_status(data)