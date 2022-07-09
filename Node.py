class Node:
    val=None
    type=None
    childs=None

    def __init__(self, type=None, val=None):
        self.val=val
        self.type=type
        self.childs=[]

    def setVal(self, val):
        self.val = val
    
    def setType(self, type):
        self.type = type
    
    def addChilds(self, nodes):
        for node in nodes:
            self.childs.append(node)
    
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.type)+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret