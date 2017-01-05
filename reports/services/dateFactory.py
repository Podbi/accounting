import calendar
from datetime import datetime
from _datetime import date

class DateFactory:
    def createFirstDayOfMonth(self, month, year):
        date = self._createDate('01', month, year)
        date = date.replace(hour=0, minute=0, second=0)
        
        return date
    
    def createLastDayOfMonth(self, month, year):
        date = self._createDate(calendar.monthrange(year, month)[1], month, year)
        date = date.replace(hour=23, minute=59, second=59)
        
        return date
        
    def _createDate(self, day, month, year):
        return datetime.strptime(str(day) + str(month) + str(year), '%d%m%Y')