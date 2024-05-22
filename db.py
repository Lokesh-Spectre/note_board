import sqlite3
from PySide6.QtWidgets import *
class DataBase():
    def __init__(self):
        # super().__init__()
        self.conn = sqlite3.connect("noteBoard.sqlite")
        self.cur = self.conn.cursor()
        self.tables = self.pages()
        self.set_page("mainPage")
        self.table = "mainPage"
        self.tables.append(self.table)
        # return self.cur

    def read(self,pageName=None):
        table = pageName or self.table
        self.cur.execute(f"SELECT * FROM {table}")
        return self._t2j(self.cur.fetchall())

    def create(self,obj):
        self.cur.execute(f"INSERT INTO {self.table}(blob,type) Values(\"{obj['blob']}\", \"{obj['type']}\")")
        self.conn.commit()
        self.cur.execute(f"SELECT COUNT(*) from {self.table}")
        obj["id"] = self.cur.fetchall()[0][0]-1
        return obj
        
    def update(self,obj):
        try:
            self.cur.execute(f"UPDATE {self.table} SET blob=\"{obj['blob']}\",type=\"{obj['type']}\" WHERE id={obj['id']}")
            self.conn.commit()
            return True
        except:
            return False

    def delete(self,id):
        try:
            self.cur.execute(f"DELETE FROM {self.table} WHERE id={id}")
            self.conn.commit()
            return True
        except:
            return False
    
    def add_page(self, pageName):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {pageName}(id INTEGER PRIMARY KEY AUTOINCREMENT, blob TEXT , type TEXT )")
        self.conn.commit()

    def set_page(self, pageName):
        if pageName not in self.tables:
            self.add_page(pageName)
        self.table=pageName

    def del_page(self, pageName=None):
        table = pageName or self.table
        self.cur.execute(f"DROP TABLE {table}")
        self.conn.commit()
    def clear(self,pageName=None):
        table = pageName or self.table
        self.cur.execute(f"DELETE FROM {table}")
    
    def reset(self,pageName=None):
        table = pageName or self.table
        qry = f'''
UPDATE sqlite_sequence
SET seq = (SELECT MAX(id) FROM {table})
WHERE name= '{table}';
'''
        self.cur.execute(qry)
        self.conn.commit()
    

    def pages(self):
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type=\"table\"")
        return self.cur.fetchall()
    
    def _t2j(self,tuples):
        return [{"id":t[0],"blob":t[1],"type":t[2]} for t in tuples]
