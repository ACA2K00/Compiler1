from Tokens import Tokens
from Node import Node

#-------------------------------- Scanner Code
# ans = token JSYK
global content_index
global content
content_index = 0

def peek():
    global content_index
    global content
    return content[content_index]

def advance():
    global content_index
    val = peek()
    content_index = content_index + 1
    return val

def eof():
    global content
    global content_index
    return content_index >= len(content)

def scan_digits():
    ans = {
        'val': '',
        'type': ''
    }
    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else:
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()
    return ans

def scanner():
    global content_index
    global content
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n'):
        advance()
    if eof():
        ans['type'] = '$'
    else:
        if peek() in "0123456789":
            ans = scan_digits()
        else:
            ch = advance()
            if (ch in "abcdeghjklmnoqrstuvwxyz"):
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('LEXICAL ERROR')
                exit()
    return ans

#------------------------------------------- Parser Code
def val():
    val_token = None
    current = tokens.peek()
    if current == "id" or current == "inum" or current == "fnum":
      val_token = tokens.match(current)
    else:
        print("ERROR: PARSING ERROR")
        exit()
    return [Node(val_token["type"], val_token["val"])]

def expr(val_node):
    child_node = None
    current = tokens.peek()
    if current == "plus" or current == "minus": 
      child_node = Node(current)
      child_node.addChilds(val_node)
      tokens.match(current)
      next_val = val()
      child_node.addChilds(expr(next_val))
      return val_node
    else:
      return []

def stmt():
    child_token = None
    child_node = Node()
    if tokens.peek() == 'id':
      child_token = tokens.match('id')
      tokens.match('assign')
      child_node.setType('assign')
      child_node.addChilds([Node(child_token['type'], child_token['val'])])
      val_node = val()
      child_node.addChilds(expr(val_node))
    else:
      if tokens.peek() == 'print':
        tokens.match('print')
        child_token = tokens.match('id')
        child_node.setType('print')
        child_node.setVal(child_token['val'])
      else:
        print("ERROR: PARSING ERROR")
        exit()
    return [child_node]

def stmts():
    childNodes = []
    if tokens.peek() == 'id' or tokens.peek() == 'print':
        childNodes += stmt()
        childNodes += stmts()
        return childNodes
    else: 
        if tokens.peek() != '$':
            print("ERROR: PARSING ERROR")
            exit()
    return childNodes

def dcl():
    type = ''
    val = ''
    current = tokens.peek()
    if current == 'intdcl' or current == 'floatdcl':
        type = tokens.match(current)['type']
        val = tokens.match("id")['val']
    else:
        print("ERROR: PARSING ERROR")
        exit()
    return [Node(type, val)]

def dcls():
    childNodes = []
    if tokens.peek() == 'intdcl' or tokens.peek() == 'floatdcl':
        childNodes += dcl()
        childNodes += dcls()
        return childNodes
    else:
        return childNodes

def prog():
    root = Node("prog")
    root.addChilds(dcls())
    root.addChilds(stmts())
    return root

#------------------------------------------Compiler Code
# Open & Read input File
with open('input.txt') as f:
    content = f.read()

# Call Scanner
tokens = Tokens()
while not eof():
    tokens.append(scanner())
tokens.append(scanner())

# Call Parser
treeRoot = prog()

print(treeRoot, "\n")

# Code Gen
operations = treeRoot.codeGen()

with open('output.txt', 'w') as f:
    for line in operations:
        f.write(line+'\n')

print("TAC written to output.txt")