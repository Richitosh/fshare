# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from dj.fshare.models import *
from datetime import *
from django.conf import settings
import os

'''
python manage.py shell
from fshare.models import *
from datetime import *
fileset = FileSet.objects.filter(end_date__lte = datetime.now())[0]
'''

class Command(BaseCommand):
    #args = '<file_id file_id ...>'
    help = 'Remove old files from file_storage'

    def handle(self, *args, **options):
        for fileset in FileSet.objects.filter(end_date__lte = datetime.now()):
            self.stdout.write('fileset_id: ' + str(fileset.id) + '\n')
            self.stdout.write('end_date: ' + str(fileset.end_date) + '\n')
            self.stdout.write('now:      ' + str(datetime.now()) + '\n')
            files = File.objects.filter(fileset=fileset.id)

            error = 0
            # удаление файлов из каталога fileset
            for file in files:
                self.stdout.write('[file: ' + str(file.file_name) + ']\n')
                file_path = os.path.normpath(settings.MEDIA_ROOT + str(file.file))

                try:
                    os.remove(file_path)
                    self.stdout.write('       - file successfully removed' + '\n')
                except OSError:
                    self.stdout.write('       - file not found' + '\n')
                    error += 1

            # удаление каталога fileset
            try:
                os.rmdir(os.path.dirname(file_path))
                self.stdout.write('       - fileset directory successfully removed' + '\n')
            except OSError:
                self.stdout.write('       - fileset directory not found' + '\n')
                error += 1

            if not error:
                fileset.delete()
                self.stdout.write('       - fileset successfully removed' + '\n\n')

        self.stdout.write('End of removing files command\n')



