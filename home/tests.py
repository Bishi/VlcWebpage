from django.test import TestCase
from home.models import Member
from home import utils
import json
from VLCwebsite.settings import BASE_DIR

# Create your tests here.


class UpdateRosterTestCase(TestCase):
    fixtures = ['endpoint.json', 'member.json']

    guild_json_data = open(BASE_DIR + "/home/fixtures/guild_data.json")
    data = json.load(guild_json_data)

    def test_update_roster(self):
        # "Testing utils.update_roster"

        utils.update_roster(UpdateRosterTestCase.data)
        self.assertEqual(5, Member.objects.all().count())
