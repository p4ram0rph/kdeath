class sqlCmd:
	getHostID	= "SELECT HOST,PORT,USERNAME,PASSWORD FROM hosts WHERE ID=?"
	getHost 	= "SELECT HOST,PORT,USERNAME,PASSWORD FROM hosts"
	getAll		= "SELECT * FROM hosts"
	insert		= "INSERT INTO hosts(HOST,PORT,USERNAME, PASSWORD) VALUES(?,?, ?, ?)"
	count 		= "SELECT count(ID) FROM hosts"
	deleteID    = 'DELETE FROM database_bot WHERE id= {}'
	TableCreate =	("""CREATE TABLE hosts(
						ID INTEGER PRIMARY KEY AUTOINCREMENT, 
						HOST VARCHAR UNIQUE NOT NULL,
						PORT INTEGER NOT NULL, 
						USERNAME VARCHAR,
						PASSWORD VARCHAR )
					""")