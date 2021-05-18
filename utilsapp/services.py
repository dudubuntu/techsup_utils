import csv
import json
from io import StringIO
import datetime
import shutil
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core import files

from utilsapp.models import File


def handle_uploaded_file(fh, name:str):
    fh_name = name if '.csv' in name else f'{name}.csv'
    with open(f"{settings.MEDIA_ROOT / fh_name}", 'wb+') as destination:
        for chunk in fh.chunks():
            destination.write(chunk)


def clear_files():
    pass


def clear_db():
    pass


class CheckCsv():
    def check_neteller(self, psp_file_name, db_file_name, is_deposit=True):
        """
        return File objects

        is_deposit=True   >   check deposits
        is_deposit=False   >   check payouts
        """

        # if not (isinstance(neteller_fh, InMemoryUploadedFile) and isinstance(db_fh, InMemoryUploadedFile) and isinstance(is_deposit, bool)):
        #     raise TypeError('Неверные типы переданных файлов!')


        ids = []
        

        with open(settings.MEDIA_ROOT / psp_file_name, newline='') as fh:
            spamreader = csv.reader(fh)
            for row in spamreader:
                try:
                    reference = row[8].split('-')
                    if (reference[0] == 'deposit' and is_deposit) or (reference[0] == 'payout' and not is_deposit):
                        ids.append(reference[1])
                except (ValueError, AttributeError, IndexError):
                    print(row)

        if len(ids) == 0:
            print('Неверный файл')   #TODO добавить нормальное отображение ошибок
            return None


        with open(settings.MEDIA_ROOT / db_file_name, newline='') as fh:
            spamreader = csv.reader(fh)
            self.final_fh = StringIO()
            counter = 0
            try:
                spamwriter = csv.writer(self.final_fh, dialect='excel')
                for row in spamreader:
                    if str(row[0]) in ids:
                        if is_deposit:
                            spamwriter.writerow([row[0], json.loads(row[-7])['netellerEmail']])
                        elif not is_deposit:
                            spamwriter.writerow([row[0]])
                        counter += 1
            except IOError as exc:
                print(exc)  #TODO добавить отображение ошибки
            else:
                if counter == 0:
                    #нет расхождений статусов
                    print('нет разхождения статусов')
                else:
                    pass

        self.name = f'neteller{str(datetime.datetime.now().timestamp())}.csv'
        fh_name = settings.MEDIA_ROOT / self.name
        with open(settings.MEDIA_ROOT / self.name, 'w') as fh:
            self.final_fh.seek(0)
            shutil.copyfileobj(self.final_fh, fh)


    def insert_file(self):
        with open(settings.MEDIA_ROOT / self.name, 'rb+') as fh:
            dj_file = files.File(fh, name=self.name)
            fh = File.objects.create(name=self.name, created=datetime.datetime.now(), file=dj_file)
        os.remove(settings.MEDIA_ROOT / self.name)
        return fh