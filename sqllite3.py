import os
import sqlite3

class SqlCon():
    def __init__(self):
        self.db_path = r"path"
        self.setup()
		
    def ConnOpen(self):
        self.coon = sqlite3.connect(self.db_path)
        self.cursor = self.coon.cursor()
	
    def ConnClose(self):
        self.cursor.close()
        self.coon.close()
	  
    def setup(self):
        # Ścieżka do pliku bazy na zasobie sieciowym        
        # lub np. "Z:\\folder_współdzielony\moja_baza.db"

        if not os.path.exists(self.db_path):
            print("Tworzenie bazy danych...")
			# Tworzenie tabeli, jeśli jeszcze nie istnieje
            
            #conn = sqlite3.connect(self.db_path)
            #cursor = conn.cursor()
            self.ConnOpen()
			
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS przypadki (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa TEXT NOT NULL,
 
                sztuki INTEGER NOT NULL
                )
            """)
			
			self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa TEXT NOT NULL, 
                sztuki INTEGER NOT NULL
                )
            """)
            print("Tabela została utworzona (jeśli nie istniała).")
            self.ConnClose()


    def ReadRecords(self,name="przypadki"):
        print('Read records:')
        self.ConnOpen()
        # Pobieranie danych
        self.cursor.execute(f"SELECT * FROM {name}")
        rows = self.cursor.fetchall()
        print("Zawartość tabeli:")
        for row in rows:
            print(row)
        # Zamknięcie połączenia
        self.ConnClose()
		
    def addPrzypadek(self,nazwa="test",sztuk=2):
        print('Add przydadek')
        # Połączenie z bazą
        self.ConnOpen()
      
	    # Dodawanie danych
        self.cursor.execute("""
           INSERT INTO przypadki (nazwa, sztuki) VALUES (?, ?)
           """, (nazwa,sztuk))
		 
        # Zatwierdzanie zmian
        self.conn.commit()
        print("Rekord został dodany.")
        self.ConnClose()
        