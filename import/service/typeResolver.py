class TypeResolver:
    def __init__(self, database):
        self.database = database
        self.cursor = database.cursor()
        self.types = {}
        
    def resolve(self, name):
        types = self._getTypes()
        name = self._formatTypeName(name)
        
        if name in types:
            return types[name]
        else:
            raise Exception('Typ "{0}" není v databázi.'.format(name))
    
    def _getTypes(self):
        if len(self.types) > 0:
            return self.types
        
        self.cursor.execute('SELECT id, name FROM reports_recordtype ORDER BY id')
        for type in self.cursor.fetchall():
            self.types[self._formatTypeName(type[1])] = type[0]
        
        return self.types
    
    def _formatTypeName(self, name):
        replacements = {
            'ě' : 'e',
            'š' : 's',
            'č' : 'c',
            'ř' : 'r',
            'ž' : 'z',
            'ý' : 'y',
            'á' : 'a',
            'í' : 'i',
            'é' : 'e',
            'ú' : 'u',
            'ů' : 'u',
        }
        
        name = name.lower()
        for replace, replacement in replacements.items():
            name = name.replace(replace, replacement)

        return name