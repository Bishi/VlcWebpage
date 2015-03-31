from home.models import WarcraftlogsAPI
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
        url = "https://www.warcraftlogs.com/v1/reports/guild/Vin%20la%20Cvicek/Mazrigos/EU?api_key=38f09f38b5243079de0c15cb5eded39a"
        return self.fetch_json(url)

    def fetch_json(self, url):
        data = urllib.request.urlopen(url)
        str_response = data.readall().decode('utf-8')
        data = json.loads(str_response)
        return data


def create_logs(data):
    log_list = WarcraftlogsAPI.objects.all()
    #log_list.values_list('id').filter(id="4P2C7yghj1HdwXzr")[0][0]

    for log in data:
        log_id = log["id"]
        tmp = log_list.values_list('id').filter(id=log_id)
        #if not log["id"] == log_list.filter(id=log_id):
        if not tmp:
            log = WarcraftlogsAPI(id=log["id"], title=log["title"], owner=log["owner"],
                                  start=log["start"], end=log["end"], zone=log["zone"])
            log.save(force_insert=True)
            #print(log_id)