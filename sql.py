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
    def add_weight(self,weight:dict)->int:
        keys=','.join(weight.keys())
        question_marks=','.join(['?']*len(weight))
        values=tuple(weight.values())
        self.cur.execute(f"INSERT INTO weight ({keys}) VALUES ({question_marks})",values)
        self.conn.commit()
        return self.cur.lastrowid
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
        self.cur.execute("SELECT weight_id FROM edge WHERE source=? AND target=?", (source,target))
        weight_id=self.cur.fetchone()[0]
        keys=','.join([f"{k}=?" for k in data.keys()])
        values=tuple(list(data.values())+[weight_id])
        self.cur.execute(f"UPDATE weight SET {keys} WHERE id=?",values)
        self.conn.commit()
        #debug message
        print(f'weight_id {source} to {target} :id {weight_id} update success')
    def search_edge(self,source:str):
        self.cur.execute("SELECT * FROM edge_with_short_weight WHERE source=?", (source,))
        context=list(self.cur.fetchall())
        return context
    def search_vertex(self,name:str)->list:
        self.cur.execute("SELECT * FROM vertex WHERE name=?", (name,))
        return self.cur.fetchall()

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
    def quick_add_edge(self,source:vertex,target:list,weight:list):
        #type check
        if not all([isinstance(x,vertex) for x in target]):
            raise TypeError('target must be list of vertex')
        if not all([isinstance(x,dict) for x in weight]):
            raise TypeError('weight must be list of dict')
        if len(target)!=len(weight):
            raise ValueError('target and weight must be same length')
            #add data
        for t,w in zip(target,weight):
            self.add_unit_data(source,t,w)
    def classical_search_edge(self,source:str):
        # join edge and weight tables to get complete information
        output=self.cur.execute('''SELECT t.target, w.* FROM edge t
                                JOIN weight w ON t.weight_id = w.id
                                WHERE t.source = ?''', (source,)).fetchall()
        # format output
        d=self.cur.description
        keys=[x[0] for x in d][1:]  # exclude target which is the first column
        return (output,keys)

def debug():
    db_name='ceo.sqlite'
    d=database(db_name)
    return d
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

