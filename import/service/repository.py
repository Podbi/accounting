class Repository:
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
    
    def hasRecord(self, date, description, money, currency, source):
        self.cursor.execute(
            'SELECT id FROM reports_record WHERE date = ? AND description = ? AND money = ? AND currency_id = ? AND source_id = ?',
            (
               date,
               description,
               money,
               currency,
               source
            )
        )
        
        return (self.cursor.fetchone() != None)
    
    def createRecord(self, date, description, place, money, currency, source, type, category):
        self.cursor.execute(
            'INSERT INTO reports_record(date, description, place, money, currency_id, source_id, type_id, category_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
            (
                date,
                description,
                place,
                money,
                currency,
                source,
                type,
                category
            )
        )
    
    def getType(self, type):
        self.cursor.execute(
            'SELECT id FROM reports_recordtype WHERE name = ?',
            (type,)
        )
        type = self.cursor.fetchone()
        if (type != None):
           return type[0]
        else:
            return None
        
    def createType(self, name):
        self.cursor.execute(
            'INSERT INTO reports_recordtype(name) VALUES(?)',
            (name,)
        )
        self.cursor.execute(
            'SELECT id FROM reports_recordtype WHERE name = ?',
            (name,)
        )
        type = self.cursor.fetchone()
        
        return type[0]
    
    def findAll(self):
        self.cursor.execute(
            'SELECT id, description, place FROM reports_record WHERE place IS NULL ORDER BY id ',
        )
        
        return self.cursor.fetchall()
    
    def findAllByType(self, type):
        self.cursor.execute(
            'SELECT date, description, money, source_id FROM reports_record WHERE type_id = ? ORDER BY date ',
            (type,)
        )
        
        return self.cursor.fetchall()
    
    def update(self, id, description, place):
        self.cursor.execute(
            'UPDATE reports_record SET description = ?, place = ? WHERE id = ?',
            (
                description,
                place,
                id
            )
        )
    
    def commit(self):
        self.database.commit()
        self.database.close()