from django.core.management.base import BaseCommand
from django.core.management import call_command
import time


class Command(BaseCommand):
        def handle(self, *args, **options):
            timestamp = str(int(time.time()))
            file_name = 'e:\\VLCpage\\DBBackup\\backup_'+timestamp+'.json'
            output = open(file_name, 'w')
            call_command('dumpdata', format='json', indent=3, stdout=output)
            output.close()
