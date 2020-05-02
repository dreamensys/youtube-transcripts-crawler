
from datetime import date
from datetime import datetime

class Log:
    def write_message(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        today = date.today()
        print(str(today) + ',' + str(now) + ' = ' + message)
    
    def write_title(self, message):
        print('')
        print('===============================' + message)
        print('')
    
    def write_error(self, message):
        self.write_message( 'ERROR =>' + message)