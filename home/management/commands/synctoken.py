from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            token = EndpointUrl.objects.all().get(name="WoW Token").value
            api_key = utils.get_access_token()

            url = token + api_key
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.create_wowtoken(data)
