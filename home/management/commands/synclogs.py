from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            warcraft_logs = EndpointUrl.objects.all().get(name="Warcraftlogs").url
            client = utils.EndpointsClient()
            data = client.fetch(warcraft_logs)
            utils.create_logs(data)
