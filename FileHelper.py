import csv
import os

class FileHelper:
    def file_exists(self, file_name):
        return os.path.exists('csv/' + file_name + '.csv')
            
    def create_cvs(self, list, name, headers):
        with open('csv/'+name+'.csv', 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(headers)
            for item in list:
                text = u''.join((item['text'])).encode('utf-8').strip()
                filewriter.writerow([item['time'], text])