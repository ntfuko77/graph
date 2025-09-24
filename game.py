from sql import database
from enum import Enum
from graph import vertex
class profile(Enum):
    db_name='ceo.sqlite'

class sql():
    #database definition
    '''CREATE VIEW IF NOT EXISTS edge_with_short_weight AS
        SELECT e.source, e.target, w.quality, w.requirement
        FROM edge e
        JOIN weight w ON e.weight_id = w.id;'''
    '''CREATE TABLE IF NOT EXISTS weight
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        quality REAL,
        requirement REAL,
        labor_hour INT,
        manager_hour INT,
        production_hour INT,
        CHECK (quality >= 0 AND requirement >= 0 AND labor_hour >= 0 AND manager_hour >= 0 AND production_hour >= 0)
        )'''
    def __init__(self):
        self.db=database(profile.db_name.value)
    #the following methods cannot be moved downward because they are designed 
    # based on specific examples
    @staticmethod
    def zero_weight()->dict:
        return {'quality':0,'requirement':0,'labor_hour':0,'manager_hour':0,'production_hour':0}
    def search_edge(self,source:str):
        check=self.db.search_vertex(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        
        context=self.db.search_edge(source)
        print(f'product name: {source}')
        for i in context:
            print(i[1])
            print(f'quality {i[2]} requirement {i[3]}')

    


def debug():
    a=vertex('cookie','food')
    m=vertex('machine','')
    b=vertex('egg','food')
    c=vertex('flour','upstream manufacturing')
    
    d=sql()
    bw,mw,cw=d.zero_weight(),d.zero_weight(),d.zero_weight()
    bw['quality'],bw['requirement']=0.2,0.1
    cw['quality'],cw['requirement']=0.4,0.2
    mw['quality'],mw['requirement']=0.4,0
    w=[bw,mw,cw]
    target=[b,m,c]

    return lambda : d.db.quick_add_edge(a,target,w)
    

# class ceo():
#     class vertex():
#         def __init__(self,name,quality_weight_list=None):...
#     fertilizer=[0.3,0.3,0.4]
#     rubber=[0.1,0.7,0.2]
#     engine=[0.5,0.1,0.4]
#     def quality(name,data:list=None):
#         target=vars(ceo)[name]
#         if data:
#             return [x*y for x,y in zip(target,data)]
#         else:
#             return target
#     def qquality(name,data=None)->int:
#         output=ceo.quality(name,data)
#         return f"product name: {name}\n weight: {output}\n quality: {int(sum(output))}"
#     def __init__(self,bom:list=None,wholesale:list=None,name:str=None):
#        self.bom=bom
#        self.wholesale=wholesale
#        self.name=name
#     def set_bom(self,data:list):
#         self.bom=data
#     def set_wholesale(self,data:list):
#         self.wholesale=data
#     def set_name(self,data:str):
#         self.name=data
#     def cost(self):
#         return [x*y for x,y in zip(self.bom,self.wholesale)]
#     def qcost(self):
#         return f"product name: {self.name}\n cost: {self.cost()}\n sum: {sum(self.cost())}"
    
# x=ceo([0.1,0.1,0.1],[100,200,300],'fertilizer')
# print(x.qcost())
# print(ceo.qquality('fertilizer',[98,60,100]))

if __name__=='__main__':
    a=vertex('egg','food')
    m=vertex('machine','')
    b=vertex('feed','upstream manufacturing')
    
    d=sql()
    bw,mw=d.zero_weight(),d.zero_weight()
    bw['quality'],bw['requirement']=0.6,0.2
    mw['quality'],mw['requirement']=0.4,0
    w=[bw,mw]
    target=[b,m]
    d.db.quick_add_edge(a,target,w)

