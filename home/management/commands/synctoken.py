from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            token = EndpointUrl.objects.all().get(name="WoW Token").value

            url = token
            client = utils.EndpointsClient()
            data = client.fetch(url)
            utils.create_wowtoken(data)
