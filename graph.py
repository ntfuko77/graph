class edge():
    def __init__(self,source:'vertex',target:'vertex',weight={}):
        self.source=source
        self.target=target
        self.weight=weight
    def set_weight(self,data):
        self.weight.update(data)
    def __repr__(self):
        return f"edge({self.source.name}->{self.target.name},{self.weight})"
class vertex():
    def __init__(self,name,type=[]):
        self.name=name
        self.type=[]
        self.edges=[]
class graph():
    def __init__(self):
        #多存一次vertexe name作為key，方便查找
        self.vertexes={}
        self.edges=[]
    @property
    def namespace(self):
        return list(self.vertexes.keys())
    def add_vertex(self,name:str,type=[]):
        if name not in self.namespace:
            self.vertexes[name]=vertex(name,type)
    def add_edge(self,source:str,target:str,weight={}):
        if source in self.namespace and target in self.namespace:
            e=edge(self.vertexes[source],self.vertexes[target],weight)
            self.edges.append(e)
            self.vertexes[source].edges.append(e)
        else:
            raise ValueError('source or target not in vertexes')
    def get_edge_by_source(self,sourse:str):
        return [e for e in self.edges if e.source.name==sourse]


    
if __name__=='__main__':
    g=graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A','B',{'price':5})
    print(g.get_edge_by_source("A"))
    
