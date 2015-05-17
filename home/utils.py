from home.models import WarcraftlogsAPI, WarcraftlogsURL, RealmStatusAPI
import time
import urllib.request, json
from pprint import pprint


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
