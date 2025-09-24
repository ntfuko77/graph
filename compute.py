from graph import vertex
from sql import database
from enum import Enum

class profile(Enum):
    db_name='ceo.sqlite'
class compute():
    def __init__(self,weight_name_list:list=[]):
        self.db=database(profile.db_name.value)
        self.weight_name_space=weight_name_list
    def search_path(self,source:str):
        check=self.db.classical_search_edge(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        keys=check[1]
        context=check[0]
        output=context
        stack=[]
        while context!=[] or stack!=[]:
            stack=stack+[i[0] for i in context]
            next=stack.pop()

            context=self.db.classical_search_edge(next)[0]
            output=output+context
        return output

if __name__=='__main__':
    c=compute()
    o=c.search_path('cookie')
    print(o)

    