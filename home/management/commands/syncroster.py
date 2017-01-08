from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            guild_url = EndpointUrl.objects.all().get(name="Guild Url").value
            realm_name = EndpointUrl.objects.all().get(name="Realm Name").value
            guild_name = EndpointUrl.objects.all().get(name="Guild Name").value
            guild_field = EndpointUrl.objects.all().get(name="Guild Fields").value
            api_key = EndpointUrl.objects.all().get(name="Blizzard Api Key").value

            url = guild_url + "/" + realm_name + "/" + guild_name + guild_field + api_key
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.update_roster(data)
