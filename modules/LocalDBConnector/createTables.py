import LocaDBConnector


if __name__ == "__main__":
	db = LocalDBConnector()
	
	# create tables for PrEDIction stats
	createTable = """
			CREATE TABLE alerter (
			UUID VARCHAR2(100) PRIMARY KEY,
            LEVEL VARCHAR2(10),
            TIMESTAMP VARCHAR2(100),
			BODY VARCHAR2(512));
            """

