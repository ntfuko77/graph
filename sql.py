import sqlite3


# Database functions
def connect(name='ceo.slite'):
    c=sqlite3.connect(name)
    c.execute("PRAGMA foreign_keys = ON")
    return c
def add_vertex(c,name:str,type:str=''):
    c.execute("INSERT OR IGNORE INTO vertex (name,type) VALUES (?,?)",(name,type))
    c.commit()
def add_edge(c,source:str,target:str,weight:int):
    c.execute("INSERT OR IGNORE INTO edge (source,target,weight) VALUES (?,?,?)",(source,target,weight))
    c.commit()
def add_weight(c,weight:dict):
    keys=','.join(weight.keys())
    question_marks=','.join(['?']*len(weight))
    values=tuple(weight.values())
    c.execute(f"INSERT INTO weight ({keys}) VALUES ({question_marks})",values)
    c.commit()
def load_data(c):
    c.execute("SELECT * FROM vertex")
    vertexes=c.fetchall()
    c.execute("SELECT * FROM edge")
    edges=c.fetchall()
    return vertexes,edges
def reset_db(c):
    c.execute("DROP TABLE IF EXISTS edge")
    c.execute("DROP TABLE IF EXISTS vertex")
    c.commit()
def create_tables(file_path:str,weight_table_code:str):
    c=connect(file_path)
    c.execute('''CREATE TABLE IF NOT EXISTS vertex
                (name TEXT PRIMARY KEY,
                type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS edge
                (source TEXT,
                target TEXT,
                weight_id INT UNIQUE,
                PRIMARY KEY (source, target),
                FOREIGN KEY (source) REFERENCES vertex(name),
                FOREIGN KEY (target) REFERENCES vertex(name))''')
    c.execute(weight_table_code)
    c.commit()
    c.close()



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
    create_tables('ceo.slite',weight_table_code)