import sqlite3

class FileManager:

    def __init__(self,databaseName): #class constructor
        self.connect(databaseName) #connect to database
        self.cursor = self.conn.cursor() #creating cursor to modify the database
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS gameSaves (username text, health long, attack long, level int, xp int, x int, y int)''') #create table if it doesn't exist
        #self.disconnect()

    def connect(self,databaseName): #function to connect to the database
        self.conn = sqlite3.connect(databaseName) #connecting to desired database

    def disconnect(self): #function to disconnect from database
        self.conn.close() #closing the database connection

    def saveGame(self,user,health,attack,level,xp,x,y):
        try:
            self.cursor.execute("INSERT INTO gameSaves VALUES (?, ?, ?, ?, ?, ?, ?)", (user, health, attack, level, xp, x, y))
            self.conn.commit()
            #self.disconnect()
        except:
            print("could not save game")

    def loadGame(self,user):
        try:
            self.cursor.execute("SELECT * FROM gameSaves WHERE username = '"+user+"'")
            self.conn.commit()
            self.data = self.cursor.fetchone()
            #self.disconnect()
        except:
            print("could not load game")
