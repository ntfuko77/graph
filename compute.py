from graph import vertex
from sql import database
from enum import Enum
import numpy
class weight():
    def __init__(self,keys:list):
        self.keys=keys
        self.weight=numpy.zeros(len(keys))
    def _np_truncate(self,x,digits=3):
        factor=10**digits
        return numpy.trunc(x*factor)/factor
    def set_weight(self,data:numpy.array):
        data=self._np_truncate(data)
        try:
            data=[float(i) for i in data]
            self.weight=data
        except:
            raise ValueError('data must be list of float')
    def __repr__(self):
        return f"weight({dict(zip(self.keys,self.weight))})"
class profile(Enum):
    db_name='ceo.sqlite'
    search_ignore=['machine']
class compute():
    def __init__(self):
        self.db=database(profile.db_name.value)
    


    def search_path(self,source:str,target:str,ignore=profile.search_ignore.value):
        check=self.db.search_vertex(source)
        if len(check)==0:
            raise ValueError(f'{source} not in vertex table')
        check=self.db.search_vertex(target)
        if len(check)==0:
            raise ValueError(f'{target} not in vertex table')
        keys=self.db.classical_search_edge(source)[1]
        output_weight=numpy.ones(len(keys)-1) #exclude target column
        def recursive_search(node:str,target,acc_weight,ignore:list):
            if node in ignore:
                return []
            if node==target:
                return [(node,acc_weight)]
            check=self.db.classical_search_edge(node)
            if len(check[0])==0:
                return [(node,acc_weight)] if node==target else [(node,numpy.zeros(len(acc_weight)))]
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

        sumation=weight(keys[1:])
        if len(paths)>1:
            sumation.set_weight(numpy.sum([x[1] for x in paths if x[0]==target],axis=0))
            return paths+[sumation]
        else:
            return self.db.zero_weight


if __name__=='__main__':
    c=compute()
    o=c.search_path('car','steel')
    print(o)


    