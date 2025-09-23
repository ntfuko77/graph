class edge():
    def __init__(self,data:'vertex',weight={}):
        self.pointer=data
        self.weight=weight
    def set_weight(self,data):
        self.weight.update(data)
class vertex():
    def __init__(self,data,edges=[]):
        self.data=data
        if False in [isinstance(i,edges) for i in edges]:
            raise TypeError("vertex.edges only Vertex ")
        self.edges=edges
    def get_weight(self,name:str):
        output=[i.weight for i in self.edges if (name in i.weight.keys())]
        return output

if __name__=='__main__':
    x=vertex('a')
    y=edge(x,{'b':1})
    x.edges.append(y)
    
    print(x.get_weight('b'))
