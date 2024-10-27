from django.db import connection
from django.urls import reverse

from .monthSummary import MonthSummary
from .summaryRecord import SummaryRecord
from .monthTranslator import MonthTranslator

class MonthSummaryCalculator:
    def calculate(self, dateFrom, dateTo, currency):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    SUM(record.money) AS sum, 
                    SUM(necessity_record.money) AS necessity_sum, 
                    SUM(nice_record.money) AS nice_sum, 
                    SUM(saving_record.money) AS saving_sum, 
                    currency.code, 
                    type.id, 
                    type.name 
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id 
				LEFT JOIN reports_record AS necessity_record ON record.id = necessity_record.id AND necessity_record.category_id = 1
				LEFT JOIN reports_record AS nice_record ON record.id = nice_record.id AND nice_record.category_id = 2
				LEFT JOIN reports_record AS saving_record ON record.id = saving_record.id AND saving_record.category_id = 3
                WHERE record.date >= %s AND record.date <= %s AND currency.code = %s
                GROUP BY currency.code, type.id, type.name 
                ORDER BY type.name
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S'),
                    currency
                )
            )
            rows = cursor.fetchall()
        
        summary = MonthSummary(currency)
        for row in rows:
            record = SummaryRecord(row[5], row[6], row[0], row[1], row[2], row[3], row[4])
            if record.amount > 0:
                summary.addRevenue(record)
            elif record.amount < 0:
                summary.addExpense(record)
        summary.sort()
        
        return summary

    def listOfAvailable(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT substr(date, 0, 5) AS year, substr(date, 6, 2) AS month 
                FROM reports_record 
                ORDER BY year DESC, month DESC
            """
            )
            rows = cursor.fetchall()
        translator = MonthTranslator()
        months = []
        for row in rows:
            months.append({
                'month' : row[1],
                'year' : row[0],
                'url' : reverse('record:month_summary', kwargs={'month': row[1], 'year' : row[0]}),
                'label' : translator.translate(int(row[1])) + ' ' + row[0]
            })
        
        return months