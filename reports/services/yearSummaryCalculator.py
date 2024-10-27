from django.db import connection
from django.urls import reverse

class YearSummaryCalculator:

    def listOfAvailable(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT substr(date, 0, 5) AS year
                FROM reports_record 
                ORDER BY year DESC
            """
            )
            rows = cursor.fetchall()
        years = []
        for row in rows:
            years.append({
                'year' : row[0],
                'url' : reverse('record:year_summary', kwargs={'year' : row[0]}),
                'label' : row[0]
            })
        
        return years