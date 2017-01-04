from django.test import TestCase
from home.models import Member
from home import utils
from VLCwebsite.settings import BASE_DIR
import json

# Create your tests here.


class UpdateRosterTestCase(TestCase):
    fixtures = ['member.json']

    guild_json_data = open(BASE_DIR + "/home/fixtures/guild_data.json")
    data = json.load(guild_json_data)

    def test_update_roster(self):
        # "Testing utils.update_roster"

        utils.update_roster(UpdateRosterTestCase.data)
        members = Member.objects.values_list('name', flat=True)
        self.assertListEqual(list(members), ['Test', 'Test3', 'Test4', 'Test5', 'Test6'])
