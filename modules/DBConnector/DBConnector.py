class DBConnector():
    import cx_Oracle
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.connection = None
        self.cursor = None
        self.username = None
        self.password = None
        self.url = None
        self.dbname = None
        
    def connect(self):
#        connection_string = self.username + '/' + self.password + '@' + self.url + ":1523" + '/' + self.dbname
        connection_string = self.username + '/' + self.password + '@' + self.url + '/' + self.dbname
        if self.verbose == True:
            print(connection_string)
        self.connection = self.cx_Oracle.connect(connection_string)

        if self.verbose == True:
            print('Connected to ver.', self.connection.version)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
        if self.verbose == True:
            print('Disconnected')

    def execute(self, query):
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)

        return result

    def setCredentials(self, username, password, url, dbname):
        self.username = username
        self.password = password
        self.url = url
        self.dbname = dbname
