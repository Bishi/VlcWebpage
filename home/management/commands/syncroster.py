from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            roster = EndpointUrl.objects.all().get(name="Guild").url
            api_key = EndpointUrl.objects.all().get(name="Blizzard Api Key").url
            roster += api_key
            client = utils.EndpointsClient()
            data = client.fetch(roster)
            utils.update_roster(data)
