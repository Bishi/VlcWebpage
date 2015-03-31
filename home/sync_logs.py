import sys, os

sys.path.append('/path/to/django')

sys.path.append('/path/to/djangoblog')

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoblog.settings'

from home import utils
client = utils.WarcraftlogsClient()
data = client.fetch()
utils.create_logs(data)