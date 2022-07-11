import copy

class Node:
    val=None
    type=None
    childs=None

    def __init__(self, type='', val=''):
        self.val=val
        self.type=type
        self.childs=[]

    def setVal(self, val):
        self.val = val
    
    def setType(self, type):
        self.type = type
    
    def addChilds(self, new_node):
        self.childs += new_node

    def generalize(self, type1, type2):
        type = ''
        if type1 == 'float' or type2 == 'float':
            type = 'float'
        else: type = 'int'
        return type

    def convert(self, node, type):
        if node.type == 'float' and type == 'int':
            print("ERROR: ILLEGAL TYPE CONVERSION")
            exit()
        elif node.type == 'int' and type == 'float':
            # create int2float node and id child node
            tmp = copy.deepcopy(node)
            node.type = 'int2float'
            node.val = ''
            node.childs = []
            node.addChilds([tmp])
            return 'float'
        return type

    def consistent(self, node1, node2):
        # m -> type
        type = self.generalize(node1.type, node2.type)
        self.convert(node1, type)
        self.convert(node2, type)
        return type

    def codeGen(self):
        operations = []
        for child in self.childs:
            _, _, subOperations = child.subCodeGen()
            operations += subOperations
        return operations
    
    def subCodeGen(self, op_num=0):
        op_level = "n" + str(op_num)
        current = op_num
        operations = []
        subOperations = []
        if self.type in ['intdcl', 'floatdcl', 'print']:
            op_level = self.val
            operations.append(self.type + " " + self.val)
            current -= 1
        elif self.type in ['inum','fnum','id']:
            op_level = self.val
            current -= 1
        elif self.type == 'int2float':
            op_level = "n" + str(current)
            r_op, current, subOperations = self.childs[0].subCodeGen(current+1)
            operations.append(op_level + "=" + self.type + " " + r_op)
        elif self.type == 'plus' or self.type == 'minus':
            op_level = "n" + str(current)
            l_op, current, l_subOperations = self.childs[0].subCodeGen(current+1)
            r_op, current, r_subOperations = self.childs[1].subCodeGen(current+1)
            subOperations = subOperations + l_subOperations + r_subOperations
            if self.type == 'plus':
                operations.append(op_level + "=" + l_subOperations + "+" + r_subOperations)
            else:
                operations.append(op_level + "=" + l_subOperations + "-" + r_subOperations)
        elif self.type == 'assign':
            prev_op, current, subOperations = self.childs[1].subCodeGen(current+1)
            operations.append(self.type[0].val + "=" + prev_op)
        
        return op_level, current, subOperations + operations
    
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.type)+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret