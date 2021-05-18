from celery import shared_task
import os

from django.conf import settings

from utilsapp import services
from utilsapp.models import File


@shared_task
def clear_db(all=False):
    if all:
        File.objects.all().delete()
        clear_files.delay()
    files = File.objects.all().order_by('-created')
    if not len(files) < 5:
        for file in files[5:]:
            file.delete()


@shared_task
def check_csv(psp_file_name, db_file_name, is_deposit):
    checkcsv = services.CheckCsv()
    checkcsv.check_neteller(psp_file_name, db_file_name, is_deposit=is_deposit)
    checkcsv.insert_file()
    
    clear_db.delay()


@shared_task
def clear_files(all=False):
    if all:
        pass
    files_names = [file['file'] for file in File.objects.all().order_by('-created')[:5].values('file')]
    dir_files = os.listdir(settings.MEDIA_ROOT)
    while dir_files:
        entry = dir_files.pop()
        if entry in files_names:
            continue
        os.remove(settings.MEDIA_ROOT / entry)