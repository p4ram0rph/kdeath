import os
import sqlite3
from sqlCmd import *

class Exec:
	def __init__(self):
		pass
	def createDB(self,db):
		if os.path.isfile(db):
			self.db = sqlite3.connect(db)
			print "Loading database %s " % db
		else:
			print "Creating database %s " % db
			self.db = sqlite3.connect(db)
			self.db.execute(sqlCmd.TableCreate)
			self.db.commit()
			return self.db
	def insert(self,data):
		self.db.execute(sqlCmd.insert, data)
		self.db.commit()

	def selectALL(self,ids=0):
		if ids == 0:
			row = self.db.execute(sqlCmd.getHost)
			return row
		else:
			row = self.db.execute(sqlCmd.getAll)
			return row
	def  getHost(self, ID):
		for i in self.db.execute(sqlCmd.getHostID, (ID,)):
			return i