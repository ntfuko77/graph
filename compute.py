from graph import vertex
from sql import database
from enum import Enum
import numpy

class profile(Enum):
    db_name='ceo.sqlite'
class compute():
    def __init__(self,weight_name_list:list=[]):
        self.db=database(profile.db_name.value)
        self.weight_name_space=weight_name_list
    def search_path(self,source:str,target:str=None):
        check=self.db.classical_search_edge(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        keys=check[1]
        print(keys)
        output_weight=numpy.ones(len(keys)-1) #exclude target column
        context=check[0]
        output=context
        stack=[]
        if context==[]:
            return []
        sub=[numpy.array(i[2:]) for i in context]
        number=0
        while context!=[] or stack!=[]:
            stack=stack+[i[0] for i in context]
            next=stack.pop()
            context=self.db.classical_search_edge(next)[0]
            output=output+context
        if target:
            return [(x,y) for x,y in zip(keys[1:],output_weight)]
        return output
    

if __name__=='__main__':
    c=compute()
    o=c.search_path('cookie')
    print(o)

    