from django.db import connection

from .record import Record

class RecordSummaryRepository:
    def findAllByDates(self, dateFrom, dateTo, currency):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    record.id,
                    record.date,
                    record.description,
                    record.place,
                    type.name AS type,
                    record.money,
                    currency.code AS currency,
                    source.name AS source
                FROM reports_record AS record 
                JOIN reports_currency AS currency ON record.currency_id = currency.id 
                JOIN reports_recordtype AS type ON record.type_id = type.id
                JOIN reports_moneysource AS source ON record.source_id = source.id 
                WHERE record.date >= %s AND record.date <= %s AND currency.code = %s
                ORDER BY record.date DESC
                """,
                (
                    dateFrom.strftime('%Y-%m-%d %H:%M:%S'),
                    dateTo.strftime('%Y-%m-%d %H:%M:%S'),
                    currency
                )
            )
            rows = cursor.fetchall()
        
        records = []
        for row in rows:
            records.append(
                Record(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
           )
        
        return records