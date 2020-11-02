from django.db import connection

class BalanceCalculator:
    def calculate(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    source.name,
                    SUM(record.money)
                FROM reports_record AS record 
                JOIN reports_moneysource AS source ON record.source_id = source.id 
                GROUP BY source.name
                ORDER BY source.name DESC
                """,
            )
            rows = cursor.fetchall()
        
        balance = []
        for row in rows:
            balance.append({
                'name' : row[0],
                'balance' : round(row[1], 0)
            })
        
        return balance