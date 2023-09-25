import sqlite3

class database:
    def __init__(self):
        self.DBname = 'SQL practice.db'

    def connect (self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)
        return conn

    def queryDB(self,command, params=[]):
        conn = self.connect()
        cur = conn.cursor() #creates new cursor object by executing SQL treatments
        cur.execute(command,params) #executes the update based on provided parameters

        #fetchall()- it fetches all the rows on a result set. If some rows have already been extracted 
        # form the result set, then it retrieves the remaining rows from the result set
        result = cur.fetchall()
        self.disconnect(conn)
        return result

    def updateDB(self,command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command,params)


        conn.commit()
        result = cur.fetchall() # commits the transaction
        self.disconnect(conn) # gets all the results 
        return result 
#################################################
#This closes the database
    def disconnect(self,conn):
        conn.close()
