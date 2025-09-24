from graph import vertex
from sql import database
from enum import Enum

class profile(Enum):
    db_name='ceo.sqlite'
class compute():
    def __init__(self,weight_name_list=list):
        self.db=database(profile.db_name.value)
        self.weight_name_space=weight_name_list
    def search_path(self,source:str):
        check=self.db.search_vertex(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        check=self.db.search_edge(source)
        if len(check)==0:
            raise ValueError(f'no edge with source {source}')
        print(check)

if __name__=='__main__':
    c=compute()
    c.search_path('cookie')