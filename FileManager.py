import sqlite3

class FileManager:

    def __init__(self,databaseName): #class constructor
        self.connect(databaseName) #connect to database
        self.cursor = self.conn.cursor() #creating cursor to modify the database
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS gameSaves (username text, died bool, health long)''') #create table if it doesn't exist

    def connect(self,databaseName): #function to connect to the database
        self.conn = sqlite3.connect(databaseName) #connecting to desired database

    def disconnect(self): #function to disconnect from database
        self.conn.close() #closing the database connection

    def saveGame(self,user,health,done):
        self.cursor.execute("INSERT INTO gameSaves VALUES (?, ?, ?)", (user, done, health))
        self.conn.commit()
        self.disconnect()

    def loadGame(self,username):
        print()