from home.models import WarcraftlogsAPI, WarcraftlogsURL, RealmStatusAPI, WowTokenApi, Member
from django.utils import timezone
import time
import urllib.request
import json
import datetime
import http.client
import logging


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


class SpecClient(object):
    interval = 0

    def fetch(self, name, **params):
        delta = time.time() - RealmStatusClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        RealmStatusClient.interval = time.time()
        url = 'https://eu.api.battle.net/wow/character/Draenor/'+name+'?fields=talents&locale=en_GB&' \
              'apikey=83e6zvj6pxysg9cnr6euybwk4wfkm76r'

        # http://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-python-urlopen
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        url = urllib.parse.urlunsplit(url)

        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def update_roster(data):
    current_roster = Member.objects.all()
    curr_timestamp = datetime.datetime.fromtimestamp(int(data['lastModified']/1000))
    #logging.basicConfig(filename='C:/Users/i7-2600k/Desktop/sync.log', level=logging.DEBUG)

    for member in data['members']:
        #ò -> &#242 etc;
        char_name = member['character']['name'].encode('ascii', 'xmlcharrefreplace').decode('utf-8')
        tmp_char_name = member['character']['name']
        #SPECS
        # print(char_name)
        try:
            spec_client = SpecClient()
            spec_data = spec_client.fetch(tmp_char_name)
            char_spec = ""
            try:
                for spec in spec_data['talents']:
                    char_spec = char_spec + "/" + spec['spec']['name']
            except:
                char_spec = spec_data['talents'][0]['spec']['name']

            if char_spec.startswith("/"):
                    char_spec = char_spec[1:]

            # print(char_spec)
        except:
            char_spec = 'Unknown'

        char_level = member['character']['level']
        char_class = member['character']['class']
        char_rank = member['rank']
        curr_thumbnail = member['character']['thumbnail']

        #check if thumbnail is valid
        curr_thumbnail = "http://eu.battle.net/static-render/eu/"+curr_thumbnail
        url = curr_thumbnail[20:]
        status = check_thumbnail(url)
        if status == 404:
            curr_thumbnail = "http://media.blizzard.com/wow/icons/36/inv_misc_questionmark.jpg"

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
            #logging.debug("NEW ENTRY: %s %s %s %s %s %s", char_name, char_spec, char_class, char_rank, char_level, curr_timestamp )
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
            #logging.debug("UPDATED: %s %s", guildie.name, guildie.timestamp)
            print("UPDATED:", guildie.name)

    #if the guild member is no longer in the guild -> delete
    for member in current_roster:
        if str(member) not in str(data['members']).encode('ascii', 'xmlcharrefreplace').decode('utf-8'):
            #logging.debug("DELETED: %s", str(member) )
            print('DELETED: ', member)
            member.delete()

    print("Last updated: ", curr_timestamp)


def check_thumbnail(url):
    conn = http.client.HTTPConnection("eu.battle.net", 80, timeout=5)
    conn.request("HEAD", url)
    r1 = conn.getresponse()
    return r1.status