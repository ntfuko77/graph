from sql import database
from enum import Enum
class profile(Enum):
    db_name='ceo.slite'
class sql():
    def __init__(self):
        self.db=database(profile.db_name.value)
        self.db.create_tables('''CREATE TABLE IF NOT EXISTS weight
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        quality REAL,
        requirement REAL,
        labor_hour INT,
        manager_hour INT,
        production_hour INT,
        CHECK (quality >= 0 AND requirement >= 0 AND labor_hour >= 0 AND manager_hour >= 0 AND production_hour >= 0)
        )''')
    def add_weight(self,weight:dict)->int:
        self.db.add_weight(weight)
        return self.db.cur.lastrowid
    
    

class ceo():
    class vertex():
        def __init__(self,name,quality_weight_list=None):...
    fertilizer=[0.3,0.3,0.4]
    rubber=[0.1,0.7,0.2]
    engine=[0.5,0.1,0.4]
    def quality(name,data:list=None):
        target=vars(ceo)[name]
        if data:
            return [x*y for x,y in zip(target,data)]
        else:
            return target
    def qquality(name,data=None)->int:
        output=ceo.quality(name,data)
        return f"product name: {name}\n weight: {output}\n quality: {int(sum(output))}"
    def __init__(self,bom:list=None,wholesale:list=None,name:str=None):
       self.bom=bom
       self.wholesale=wholesale
       self.name=name
    def set_bom(self,data:list):
        self.bom=data
    def set_wholesale(self,data:list):
        self.wholesale=data
    def set_name(self,data:str):
        self.name=data
    def cost(self):
        return [x*y for x,y in zip(self.bom,self.wholesale)]
    def qcost(self):
        return f"product name: {self.name}\n cost: {self.cost()}\n sum: {sum(self.cost())}"
    
# x=ceo([0.1,0.1,0.1],[100,200,300],'fertilizer')
# print(x.qcost())
# print(ceo.qquality('fertilizer',[98,60,100]))

if __name__=='__main__':
    db=sql()

