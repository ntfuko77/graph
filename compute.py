from graph import vertex
from sql import database
from enum import Enum
import numpy

class profile(Enum):
    db_name='ceo.sqlite'
    search_ignore=['machine']
class compute():
    def __init__(self):
        self.db=database(profile.db_name.value)

    def search_path(self,source:str,target:str=None,ignore=profile.search_ignore.value):
        check=self.db.classical_search_edge(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        keys=check[1]
        print(keys)
        output_weight=numpy.ones(len(keys)-1) #exclude target column
        context=[i for i in check[0] if i[0] not in ignore]
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
            context=[i for i in context if i[0] not in ignore]
            output=output+context
        if target:
            return [(x,y) for x,y in zip(keys[1:],output_weight)]
        return output
    

if __name__=='__main__':
    c=compute()
    o=c.search_path('cookie')
    print(o)

    