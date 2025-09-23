class edge():
    def __init__(self,source:'vertex',target:'vertex',weight={}):
        self.source=source
        self.target=target
        self.weight=weight
    def set_weight(self,data):
        self.weight.update(data)
class vertex():
    def __init__(self,name,type=[]):
        self.name=name
        self.type=[]
class graph():
    def __init__(self):
        self.vertexes={}
        self.edges=[]

    
if __name__=='__main__':
    x=vertex('a')
    y=edge(x,{'b':1})
    x.edges.append(y)
    
    print(x.get_weight('b'))
