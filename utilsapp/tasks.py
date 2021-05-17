from celery import shared_task

from utilsapp import services


@shared_task
def check_csv(psp_file_name, db_file_name, is_deposit):
    checkcsv = services.CheckCsv()
    checkcsv.check_neteller(psp_file_name, db_file_name, is_deposit=is_deposit)
    checkcsv.insert_file()