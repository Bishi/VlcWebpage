from django.core.management.base import BaseCommand
from home import utils

class Command(BaseCommand):
        def handle(self, *args, **options):
                client = utils.RosterClient()
                data = client.fetch()
                utils.update_roster(data)