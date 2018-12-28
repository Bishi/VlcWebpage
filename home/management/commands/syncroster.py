from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            realm_name = EndpointUrl.objects.all().get(name="Realm Name").value
            guild_name = EndpointUrl.objects.all().get(name="Guild Name").value
            guild_field = EndpointUrl.objects.all().get(name="Guild Fields").value
            base_url = EndpointUrl.objects.all().get(name="Base Url").value
            api_key_new = utils.get_access_token()

            url = base_url + "guild/" + realm_name + "/" + guild_name + guild_field + "&access_token=" + api_key_new
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.update_roster(data)
