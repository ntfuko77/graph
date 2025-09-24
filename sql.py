import sqlite3
from graph import vertex


# Database functions
class database():
    def __init__(self,name):
        self.conn=sqlite3.connect(name)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cur=self.conn.cursor()

    def add_vertex(self,name:str,type:str=''):
        self.cur.execute("INSERT OR IGNORE INTO vertex (name,type) VALUES (?,?)",(name,type))
        self.conn.commit()
    def add_edge(self, source: str, target: str, weight: int):
        self.cur.execute("INSERT OR IGNORE INTO edge (source, target, weight_id) VALUES (?, ?, ?)", (source, target, weight))
        self.conn.commit()
    def add_weight(self,weight:dict):
        keys=','.join(weight.keys())
        question_marks=','.join(['?']*len(weight))
        values=tuple(weight.values())
        self.cur.execute(f"INSERT INTO weight ({keys}) VALUES ({question_marks})",values)
        self.conn.commit()
    def load_data(self):
        self.cur.execute("SELECT * FROM vertex")
        vertexes=self.cur.fetchall()
        self.cur.execute("SELECT * FROM edge")
        edges=self.cur.fetchall()
        return vertexes,edges
    def reset_db(self):
        self.cur.execute("DROP TABLE IF EXISTS edge")
        self.cur.execute("DROP TABLE IF EXISTS vertex")
        self.conn.commit()
    def create_tables(self, weight_table_code: str):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS vertex
                        (name TEXT PRIMARY KEY,
                        type TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS edge
                        (source TEXT,
                        target TEXT,
                        weight_id INT UNIQUE,
                        PRIMARY KEY (source, target),
                        FOREIGN KEY (source) REFERENCES vertex(name),
                        FOREIGN KEY (target) REFERENCES vertex(name))''')
        self.cur.execute(weight_table_code)
        self.conn.commit()
    def weight_update(self,source:str,target:str,data:dict):
        self.db.cur.execute("SELECT weight_id FROM edge WHERE source=? AND target=?", (source,target))
        weight_id=self.db.cur.fetchone()[0]
        keys=','.join([f"{k}=?" for k in data.keys()])
        values=(weight_id,)
        self.db.cur.execute(f"UPDATE weight SET {keys} WHERE id=?",values)
        self.db.conn.commit()
    def search_edge(self,source:str):
        self.db.cur.execute("SELECT * FROM edge_with_short_weight WHERE source=?", (source,))
        context=list(self.db.cur.fetchall())
        return context
    def search_vertex(self,name:str)->list:
        self.db.cur.execute("SELECT * FROM vertex WHERE name=?", (name,))
        return self.db.cur.fetchall()
    def add_weight(self,weight:dict)->int:
        self.db.add_weight(weight)
        return self.db.cur.lastrowid
    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()
    def add_unit_data(self,source:vertex,target:vertex,weight:dict):
        self.add_vertex(source.name,source.type)
        self.add_vertex(target.name,target.type)
        weight_id=self.add_weight(weight)
        self.add_edge(source.name,target.name,weight_id)
        #display
        context=self.search_edge(source.name)
        print('input data success:')
        print(f'product name: {source.name}')
        print(f'component name: {target.name}')
        print(weight)



#CODE TO me
if __name__=='__main__':
    weight_table_code='''
    CREATE TABLE IF NOT EXISTS weight
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    quality REAL,
    requirement REAL,
    labor_hour INT,
    manager_hour INT,
    production_hour INT,
    CHECK (quality >= 0 AND requirement >= 0 AND labor_hour >= 0 AND manager_hour >= 0 AND production_hour >= 0)
    )'''

