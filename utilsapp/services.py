import csv
import json
from io import StringIO


def clear_files():
    pass


def clear_db():
    pass


class CheckCsv():
    def check_neteller(self, neteller_file_name, db_file_name, is_deposit=True):
        """
        return File objects

        is_deposit=True   >   check deposits
        is_deposit=False   >   check payouts
        """

        check_type = is_deposit

        ids = []
        with open(neteller_file_name, newline='') as fh:
            spamreader = csv.reader(fh)
            for row in spamreader:
                try:
                    reference = row[8].split('-')
                    if (reference[0] == 'deposit' and is_deposit) or (reference[0] == 'payout' and not is_deposit):
                        ids.append(reference[1])
                except (ValueError, AttributeError, IndexError):
                    print(row)


        with open(db_file_name, newline='') as fh:
            spamreader = csv.reader(fh)
            
            fh = StringIO()
            counter = 0
            try:
                spamwriter = csv.writer(fh, dialect='excel')
                for row in spamreader:
                    if str(row[0]) in ids:
                        if is_deposit:
                            spamwriter.writerow([row[0], json.loads(row[-7])['netellerEmail']])
                        elif not is_deposit:
                            spamwriter.writerow([row[0]])
                        counter += 1
            except IOError:
                pass            #TODO добавить отображение ошибки
            else:
                if counter == 0:
                    #нет расхождений статусов
                    return None
                else:
                    return fh