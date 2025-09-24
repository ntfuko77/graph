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

    def search_path(self,source:str,target:str,ignore=profile.search_ignore.value):
        check=self.db.classical_search_edge(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        keys=check[1]
        output_weight=numpy.ones(len(keys)-1) #exclude target column

        def recursive_search(node:str,target,acc_weight,ignore:list):
            if node==target:
                return [(node,acc_weight)]
            check=self.db.classical_search_edge(node)
            if len(check[0])==0:
                return [(node,acc_weight)] if node==target else []
            paths=[]
            for i in check[0]:
                if i[0] in ignore:
                    continue
                weight=numpy.array(i[2:])
                new_acc_weight=acc_weight*weight
                # print(f'current node: {node} weight : {weight}, next node: {i[0]}, acc_weight: {new_acc_weight}')
                paths+=recursive_search(i[0],target,new_acc_weight,ignore)
            return paths
        paths=recursive_search(source,target,output_weight,ignore)
        return paths+[('summation',sum([i[1] for i in paths]))]
    

if __name__=='__main__':
    c=compute()
    o=c.search_path('cookie','wheat')
    print(o)

    