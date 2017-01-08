from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            warcraft_logs = EndpointUrl.objects.all().get(name="Warcraftlogs").value
            guild_name = EndpointUrl.objects.all().get(name="Guild Name").value
            realm_name = EndpointUrl.objects.all().get(name="Realm Name").value
            logs_api = EndpointUrl.objects.all().get(name="Warcraftlogs Api Key").value

            url = warcraft_logs + "/" + guild_name + "/" + realm_name + "/" + logs_api
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.create_logs(data)
