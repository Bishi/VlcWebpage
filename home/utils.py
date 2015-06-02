from home.models import WarcraftlogsAPI, WarcraftlogsURL, RealmStatusAPI, WowTokenApi, Member
from django.utils import timezone
import time
import urllib.request
import json
import datetime


class WarcraftlogsClient(object):
    interval = 0

    def fetch(self, **params):
        delta = time.time() - WarcraftlogsClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        WarcraftlogsClient.interval = time.time()
        #url = "https://www.warcraftlogs.com/v1/reports/guild/Vin%20la%20Cvicek/Mazrigos/EU?api_key=38f09f38b5243079de0c15cb5eded39a"
        url = WarcraftlogsURL.objects.all()
        url = url.values_list('url')[0][0]
        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def create_logs(data):
    log_list = WarcraftlogsAPI.objects.all()

    for log in data:
        log_id = log["id"]
        tmp = log_list.values_list('id').filter(id=log_id)
        if not tmp:
            log = WarcraftlogsAPI(id=log["id"], title=log["title"], owner=log["owner"],
                                  start=log["start"], end=log["end"], zone=log["zone"])
            log.save(force_insert=True)


class RealmStatusClient(object):
    interval = 0

    def fetch(self, **params):
        delta = time.time() - RealmStatusClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        RealmStatusClient.interval = time.time()
        url = 'http://eu.battle.net/api/wow/realm/status?realms=Draenor'
        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def create_status(data):
    RealmStatusAPI.objects.all().delete()

    maz_status = RealmStatusAPI(id=data['realms'][0]['name'], queue=data['realms'][0]['queue'],
                                status=data['realms'][0]['status'])
    maz_status.save(force_insert=True)


class WowTokenApiClient(object):
    interval = 0

    def fetch(self, **params):
        delta = time.time() - RealmStatusClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        RealmStatusClient.interval = time.time()
        url = 'https://wowtoken.info/wowtoken.json'
        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def create_wowtoken(data):
    WowTokenApi.objects.all().delete()
    updated = data['update']['EU']['raw']['updated']
    updated_time = timezone.now()

    token_price = WowTokenApi(price=data['update']['EU']['formatted']['buy'],
                              timestamp=datetime.datetime.fromtimestamp(updated).strftime("%b %d. %Y %H:%M"),
                              pub_date=updated_time)
    token_price.save(force_insert=True)


class RosterClient(object):
    interval = 0

    def fetch(self, **params):
        delta = time.time() - RealmStatusClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        RealmStatusClient.interval = time.time()
        url = 'https://eu.api.battle.net/wow/guild/Draenor/Vin%20la%20Cvicek?fields=members&locale=en_GB&api' \
              'key=83e6zvj6pxysg9cnr6euybwk4wfkm76r'
        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def update_roster(data):
    current_roster = Member.objects.all()
    curr_timestamp = datetime.datetime.fromtimestamp(int(data['lastModified']/1000))

    for member in data['members']:
        #ò -> &#242 etc;
        char_name = member['character']['name'].encode('ascii', 'xmlcharrefreplace').decode('utf-8')
        char_level = member['character']['level']
        char_class = member['character']['class']
        char_rank = member['rank']
        curr_thumbnail = member['character']['thumbnail']
        try:
            char_spec = member['character']['spec']['name']
        except:
            char_spec = 'Unknown'

        #save new guild member
        if not Member.objects.filter(name=char_name):
            new_member = Member(name=char_name,
                                spec=char_spec,
                                rank=char_rank,
                                player_class=char_class,
                                level=char_level,
                                timestamp=curr_timestamp,
                                pub_date=timezone.now(),
                                thumbnail=curr_thumbnail)
            new_member.save(force_insert=True)
            print("NEW ENTRY: ", char_name, char_spec, char_class, char_rank, char_level)

        #update guild member if level or rank or spec or thumbnail changed
        guildie = Member.objects.get(name=char_name)
        if guildie.level != char_level or guildie.rank != char_rank or guildie.spec != char_spec \
                or guildie.thumbnail != curr_thumbnail:
            guildie.level = char_level
            guildie.spec = char_spec
            guildie.rank = char_rank
            guildie.timestamp = curr_timestamp
            guildie.pub_date = timezone.now()
            guildie.thumbnail = curr_thumbnail
            guildie.save()
            print("UPDATED:", guildie.name)

    #if the guild member is no longer in the guild -> delete
    for member in current_roster:
        if str(member) not in str(data['members']).encode('ascii', 'xmlcharrefreplace').decode('utf-8'):
            print('DELETED: ', member)
            member.delete()

    print("Last updated: ", curr_timestamp)