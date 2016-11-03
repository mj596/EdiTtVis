import sqlite3

class LocalDBConnector():
	
    def __init__(self, verbose=False):
		self.verbose = verbose
        self.connection = None
        self.cursor = None
        self.dbfilename = None
		self.dbname = None
		self.username = None
		self.password = None

    def connect(self):
        self.connection = sqlite3.connect(self.dbfilename)
		if self.verbose = True:
			print('Connected to', self.dbfilename)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
		if self.verbose = True:
			print('Disconnected')

    def execute(self, query):
		if self.verbose:
			print('Execute query: ', query)
        self.cursor.execute(query)
        result = []
        for row in self.cursor:
            result.append(row)
        if self.verbose:
            print('Query got: ', str(len(result)), ' rows')
        return result

    def commit(self):
        self.connection.commit()
		
	def setCredentials(self, username, password, dbfilename, dbname):
        self.username = username
        self.password = password
        self.url = url
        self.dbname = dbname
		
		"PrEDIction_STATS.db"