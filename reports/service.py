import calendar
from datetime import datetime
from django.db import connection

class MonthSummaryCalculator:
    def calculate(self, dateFrom, dateTo):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(record.money), currency.code, type.name 
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id 
                WHERE record.date >= %s AND record.date <= %s 
                GROUP BY currency.code, type.name 
                ORDER BY type.name
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S')
                )
            )
            rows = cursor.fetchall()
        return rows
        
class DateFactory:
    def createFirstDayOfMonth(self, month, year):
        date = self._createDate(calendar.monthrange(year, month)[0], month, year)
        date = date.replace(hour=0, minute=0, second=0)
        
        return date
    
    def createLastDayOfMonth(self, month, year):
        date = self._createDate(calendar.monthrange(year, month)[1], month, year)
        date = date.replace(hour=23, minute=59, second=59)
        
        return date
        
    def _createDate(self, day, month, year):
        return datetime.strptime(str(day) + str(month) + str(year), '%d%m%Y')