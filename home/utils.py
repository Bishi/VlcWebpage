from home.models import WarcraftlogsAPI, RealmStatusAPI, WowTokenApi, Member, EndpointUrl
from django.utils import timezone
from urllib.error import HTTPError
import time
import urllib.request
import json
import datetime
import http.client
import logging
import ssl


class EndpointsClient(object):
    interval = 0

    def fetch(self, url):
        delta = time.time() - EndpointsClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        return self.fetch_json(url)

    def fetch_json(self, url):
        context = ssl._create_unverified_context()
        data = urllib.request.urlopen(url, context=context)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


class SpecClient(object):
    interval = 0

    def fetch(self, name):
        delta = time.time() - SpecClient.interval
        if delta < 2:
            time.sleep(2 - delta)
        SpecClient.interval = time.time()
        character_url = EndpointUrl.objects.all().get(name="Character Url").value
        realm = EndpointUrl.objects.all().get(name="Realm Name").value
        character_fields = EndpointUrl.objects.all().get(name="Character Fields").value
        api_key = EndpointUrl.objects.all().get(name="Blizzard Api Key").value
        url = character_url + "/" + realm + "/" + name + character_fields + api_key

        # http://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-python-urlopen
        url = urllib.parse.urlsplit(url)
        url = list(url)
        url[2] = urllib.parse.quote(url[2])
        url = urllib.parse.urlunsplit(url)
        fetch = EndpointsClient()
        return fetch.fetch_json(url)


def create_logs(data):
    WarcraftlogsAPI.objects.all().delete()

    for log in data:
        log = WarcraftlogsAPI(name=log["id"], title=log["title"], owner=log["owner"],
                              start=log["start"], end=log["end"], zone=log["zone"])
        log.save(force_insert=True)


def create_status(data):
    RealmStatusAPI.objects.all().delete()
    current_realm = EndpointUrl.objects.all().get(name="Realm Name").value

    for realm in data['realms']:
        if realm['name'] == current_realm:
            status = RealmStatusAPI(name=realm['name'], queue=realm['queue'],
                                    status=realm['status'])
            status.save(force_insert=True)


def create_wowtoken(data):
    WowTokenApi.objects.all().delete()
    updated = data['update']['EU']['raw']['updated']
    updated_time = timezone.now()

    token_price = WowTokenApi(price=data['update']['EU']['formatted']['buy'],
                              timestamp=datetime.datetime.fromtimestamp(updated).strftime("%d. %b. %Y %H:%M"),
                              pub_date=updated_time)
    token_price.save(force_insert=True)


def update_roster(data):
    log = logging.getLogger("utils")
    log.info("_______________")
    log.info("Logging started")
    current_roster = Member.objects.all()
    curr_timestamp = datetime.datetime.fromtimestamp(int(data['lastModified'] / 1000))

    for member in data['members']:
        # ò -> &#242 etc;
        char_name = member['character']['name'].encode('ascii', 'xmlcharrefreplace').decode('utf-8')
        tmp_char_name = member['character']['name']
        # print(char_name)

        char_spec = 'Unknown'
        char_item_level = 'Unknown'

        # spec and item level
        try:
            spec_client = SpecClient()
            spec_data = spec_client.fetch(tmp_char_name)
            char_spec = member['character']['spec']['name']
            char_item_level = str(spec_data['items']['averageItemLevel']) + \
                              "(" + str(spec_data['items']['averageItemLevelEquipped']) + ")"
        except KeyboardInterrupt:
            log.info("Logging interrupted by user.")
            raise
        except HTTPError:
            log.info("Could not find character %s" % tmp_char_name)
            print("Could not find character %s" % tmp_char_name)
        except KeyError as e:
            log.info("Could not find some info for character %s : %s" % (tmp_char_name, e))
            print("Could not find some info for character %s : %s" % (tmp_char_name, e))
        except Exception as e:
            log.error("%s : %s" % (e, tmp_char_name))
            print("ERROR %s %s" % (tmp_char_name.encode("UTF-8"), e))
        char_level = member['character']['level']
        char_class = member['character']['class']
        char_rank = member['rank']
        curr_thumbnail = member['character']['thumbnail']

        #  check if thumbnail is valid
        curr_thumbnail = "http://render-api-eu.worldofwarcraft.com/static-render/eu/" + curr_thumbnail
        url = curr_thumbnail[40:]
        status = check_thumbnail(url)
        if 400 <= status <= 505:
            curr_thumbnail = "/media/class_thumbnails/question.jpg"

        #  save new guild member
        if not Member.objects.filter(name=char_name):
            new_member = Member(name=char_name,
                                spec=char_spec,
                                rank=char_rank,
                                player_class=char_class,
                                level=char_level,
                                item_level=char_item_level,
                                timestamp=curr_timestamp,
                                pub_date=timezone.now(),
                                thumbnail=curr_thumbnail)
            new_member.save(force_insert=True)
            print("NEW ENTRY: ", char_name, char_spec, char_class, char_rank, char_level)
            log.info("NEW ENTRY: %s %s %s %s %s" % (char_name, char_spec, char_class, char_rank, char_level))

        #  update guild member if level or rank or spec or thumbnail changed
        guildie = Member.objects.get(name=char_name)
        if guildie.level != char_level or guildie.rank != char_rank or guildie.spec != char_spec \
                or guildie.thumbnail != curr_thumbnail or guildie.item_level != char_item_level:
            guildie.level = char_level
            guildie.item_level = char_item_level
            guildie.spec = char_spec
            guildie.rank = char_rank
            guildie.timestamp = curr_timestamp
            guildie.pub_date = timezone.now()
            guildie.thumbnail = curr_thumbnail
            guildie.save()
            print("UPDATED:", guildie.name)
            log.info("UPDATED: %s" % guildie.name)

    # if the guild member is no longer in the guild -> delete
    for member in current_roster:
        if str(member) not in str(data['members']).encode('ascii', 'xmlcharrefreplace').decode('utf-8'):
            print("DELETED: ", member)
            log.info("DELETED: %s" % member)
            member.delete()

    print("Last updated: ", curr_timestamp)
    log.info("Last updated: %s" % curr_timestamp)


def check_thumbnail(url):
    conn = http.client.HTTPConnection("render-api-eu.worldofwarcraft.com", 80, timeout=5)
    conn.request("HEAD", url)
    r1 = conn.getresponse()
    return r1.status