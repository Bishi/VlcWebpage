from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            status = EndpointUrl.objects.all().get(name="Realm Status").value
            api_key = EndpointUrl.objects.all().get(name="Blizzard Api Key").value

            url = status + api_key
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.create_status(data)
