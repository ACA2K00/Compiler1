from Tokens import Tokens
from Node import Node

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
        'val': ''
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

#------------------------------------------- Parser

def stmt(tokens):
    if tokens.peek()['type'] == 'id':
        match(tokens, 'id')
        match(tokens, 'assign')
        val(tokens)
        expr(tokens)
    elif tokens.peek()['type'] == 'print':
        match(tokens, 'print')
        match(tokens, 'id')
    else:
        print('ERROR')

def stmts(tokens):
    if tokens.peek()['type'] == 'id' or tokens.peek()['type'] == 'print':
        node = Node(stmt(tokens))
        return node + stmts(tokens)
    elif tokens.peek()['type'] == '$':
        return []
    else:
        print('ERROR')


def dcl(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        node = Node(tokens.advance()['type'])
        if tokens.peek()['type'] == 'id':
            node.setVal(tokens.advance()['val'])
            return [node]
        else:
            print('ERROR')
            exit()
    return []

def dcls(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        nodes = dcl(tokens)
        return nodes + dcls(tokens)
    return []

def prog(tokens):
    root = Node("prog")
    root.addChilds(dcls(tokens))
    # stmts(tokens)
    return root

with open('input.txt') as f:
    content = f.read()
tokens = Tokens()
while not eof():
    tokens.append(scanner())
tokens.append(scanner())

prog(tokens)
#print(tokens.tokens)