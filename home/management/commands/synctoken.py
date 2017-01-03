from django.core.management.base import BaseCommand
from home.models import EndpointUrl
from home import utils


class Command(BaseCommand):
        def handle(self, *args, **options):
            status = EndpointUrl.objects.all().get(name="WoW Token").url
            client = utils.EndpointsClient()
            data = client.fetch(status)
            utils.create_wowtoken(data)
