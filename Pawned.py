from copy import deepcopy
import sys

#sys.stdout = open('out2.txt', 'w')
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 17:05:40 2016

@author: Colby & Wyatt
"""
class TreeNode(object):
    board = [[],[],[],[],[],[]]
    childBoards = list()
    path = list()
    
    
def makeNode(b):
    tn = TreeNode()
    tn.board = b
    tn.childBoards = list()
    tn.path = list()
    return tn
    
#loops through and prints formatted the board
def printBoard(board):
    x = 0;
    y = 0;
    print("  Pawned!")
    string = ""
    while x < 6:
        while y < 6:
            string += str(board[x][y]) + " "
            y+=1
        string += '\n'
        y=0
        x+=1
    print(string+"\n")
    
#returns a list of all legal moves in an array
#list contains 0(s), 1(s),and/or 2(s)
#0: move up/down from currebt position
#1: move left and up/down from current position
#2: move right and up/down the current position
#parameters:
#board: a 2d array of 0's, 1's, and 2's representing the board
#x: x position of peice
#y: y position of peice
#color: which color is using
def getLegalMoves(board, x, y, color):
    moves = list()
    if (color == 1 and x >= 5):
        return moves
        
    if (color == 2 and x <= 0):
        return moves
        
    if (color == 1):
        if (board[x+1][y] == 0):
            moves.append(0)
        if (y != 0 and x != 5 and board[x+1][y-1] == 2):
            moves.append(1)
        if (y != 5 and x != 5 and board[x+1][y+1] == 2):
            moves.append(2)
    if (color == 2):
        if (board[x-1][y] == 0):
            moves.append(0)
        if (x != 0 and y != 0 and board[x-1][y-1] == 1):
            moves.append(1)
        if (x != 0 and y != 5 and board[x-1][y+1] == 1):
            moves.append(2)
    return moves



def terminalPosition(board, color):
    x = 0;
    y = 0;
    count1 = 0
    count2 = 0
    while x < 6:
        while y < 6:
            if (board[x][y] == 1):
                count1 += 1
                if(board[x][y] == 1 and x >= 5):
                    return True
            if (board[x][y] == 2):
                count2 += 1
                if(board[x][y] == 2 and x <= 0):
                    return True
            y+=1
        y=0
        x+=1
        
    if (count1 == 0 and color == 2):
        return True
            
    if (count2 == 0 and color == 1):
        return True
        
    if (len(getAllMoves(board, 1)) == 0 and color == 2):
        return True
        
    if (len(getAllMoves(board, 2)) == 0 and color == 1):
        return True
    else:
        return False
    return False
  
  #global found varible for minimax
found = False
def setFalse():
    found = False
def setTrue():
    found = True
def getFound():
    return found
    
#global currentpath to successsssss
bestPath = list()
def appendPath(p):
    bestPath.append(p)
def getPath():
    return bestPath
def clearPath():
    bestPath = []
    print("func: "+str(len(bestPath)))
    
#global currentpath to successsssss
bestNonTerminalNodes = list()
def appendNodes(p):
    bestNonTerminalNodes.append(p)
def getNodes():
    return bestNonTerminalNodes
        
        
def minimax(rootNode, color, depth):
    bestNonTerminalNodes.clear()
    setFalse()
    bestPath.clear()
    minimaxHelper(rootNode, color, depth, 0)
    bestPoints = -999
    bestNode = makeNode(rootNode.board)
    print(len(bestNonTerminalNodes))
    if (not getFound()):
        for n in bestNonTerminalNodes:
            curr = evaluateBoards(n)
            if (bestPoints < curr):
                #printBoard(n.path[2].board)
                bestPoints = curr
                bestNode = n.path[1]
    else:
        print("testing")
        bestNode = deepcopy(bestPath[1])
        
    return bestNode
                
                
#return node             
def evaluateBoards(node1):
    currentPoints = 0
    x = 0;
    y = 0;
    while x < 6:
        while y < 6:
            if (node1.board[x][y] == 2):
                currentPoints += (6-x)
                #print("2point +"+str(6-x))
            if ((node1.board[x][y] == 2 and x!=0 and y!=5 and node1.board[x-1][y+1] == 1) or (node1.board[x][y] == 2 and x!=0 and y!=0 and node1.board[x-1][y-1] == 1)):
                currentPoints -= (6-x)
                #print("cankill -"+str(6-x))
            if (node1.board[x][y] == 1):
                currentPoints -= (x + 1)
                #print("1point -"+str(x+1))
            y+=1
        y=0
        x+=1
    return currentPoints
        
        
def minimaxHelper(currentNode, color, maxDepth, currentDepth):
    bestPath.clear()
    if (maxDepth == currentDepth):
        appendNodes(currentNode)
        
    if(terminalPosition(currentNode.board, color)):
        currentNode.path.append(currentNode)
        if not getFound():
            setTrue()
            bestNonTerminalNodes.clear()
            print("found terminal")
            for n in currentNode.path:
                appendPath(n)
        return currentNode.path
        
    if (currentDepth == maxDepth):
        appendNodes(currentNode)
        
    elif not getFound():
        for child in currentNode.childBoards:
            if(color == 1): 
                color = 2 
            else: 
                color = 1
            
            #children.path.append(currentNode)
            #for n in children.path:
            #   children.path.append(n) #idk if we want node or board
            for p in currentNode.path:
                child.path.append(p)
            child.path.append(currentNode)
            if not getFound():
                minimaxHelper(child, color, maxDepth, currentDepth + 1)
        

def movePieces(board, x, y, color, move):
    if (color == 1):
        if (move == 0):
            board[x][y] = 0
            board[x+1][y] = 1
        if (x != 5 and y!=0 and move == 1):
            board[x][y] = 0
            board[x+1][y-1] = 1
        if (x!=5 and y!=5 and move == 2):
            board[x][y] = 0
            board[x+1][y+1] = 1
    if (color == 2):
        if (move == 0):
            board[x][y] = 0
            board[x-1][y] = 2
        if (x != 0 and y!=0 and move == 1):
            board[x][y] = 0
            board[x-1][y-1] = 2
        if (x != 0 and y!=5 and move == 2):
            board[x][y] = 0
            board[x-1][y+1] = 2
    return board
            
            
def getAllMoves(board, color):
    allMoves = list()
    x = 0
    y = 0
    string = ""
    temp = list()
    while x < 6:
        while y < 6:
            if (board[x][y] == color):
                t = 0
                for t in getLegalMoves(board, x, y, color):
                    temp.append(t)
            y+=1
            if (len(temp) > 0):
                allMoves.append(deepcopy(temp))
                temp.clear()
                if (len(string) > 0):
                    string = ""
        y=0
        x+=1
    return allMoves
    

def getMoveablePeice(board, color, index):
    x = 0
    y = 0
    count = -1
    toAdd = 0
    while x < 6:
        while y < 6:
            if (color == 1 and board[x][y] == 1):
                if (board[x+1][y] == 0):
                    toAdd = 1
                if (x != 5 and y!=0 and board[x+1][y-1] == 2):
                    toAdd=1
                if (x != 5 and y!=5 and board[x+1][y+1] == 2):
                    toAdd=1
                count+=toAdd
                if (count == index):
                    return (x,y)
            if (color == 2 and board[x][y] == 2):
                if (board[x-1][y] == 0):
                    toAdd = 1
                if (x != 0 and y!=0 and board[x-1][y-1] == 1):
                    toAdd = 1
                if (x != 0 and y!=5 and board[x-1][y+1] == 1):
                    toAdd = 1
                count+=toAdd
                if (count == index):
                    return (x,y)
            toAdd = 0
            y+=1
        y=0
        x+=1
            
def populatechildren(node, color):
    moves = getAllMoves(node.board, color)
    i = 0
    for move in moves:
        pos = getMoveablePeice(node.board, color, i)
        for submove in move:
            board_copy = deepcopy(node.board)
            movePieces(board_copy, pos[0], pos[1], color, submove)
            child = makeNode(board_copy)
            node.childBoards.append(child)
        i+=1
    #for b in node.childBoards:
        #printBoard(b.board)
    #print("\n==================\n")
    return node
    
def buildTree(currentNode, n):
    buildTreeHelper(currentNode, 0, n)

def buildTreeHelper(currentNode, start, end):
    c = (start%2)+1
    if (c < 1):
        c = 2
    for child in currentNode.childBoards:
        populatechildren(child, c)
        if (start < end):
            buildTreeHelper(child, start+1, end)
            
            
#2d Array representing the chess board in it's current state
#1's are the white pawns
#2's are the black pawns
#0's are open spaces on the board
board = [[1,1,1,1,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [2,2,2,2,2,2]]
         
         
         
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////////////////
rootNode = makeNode(board)

print("set of roots children")

#minimax(rootNode, 2, 4)
    
#for p in bestPath:
#    printBoard(p.board)
    
    
boar1 = [[1,1,1,1,1,1],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         [2,2,2,2,2,2]]
         
boar2 = [[1,1,0,0,0,1],
         [0,0,1,2,0,0],
         [2,2,0,1,0,0],
         [0,0,0,0,1,0],
         [0,0,2,0,0,0],
         [0,0,0,0,2,2]]
         
node1 = makeNode(boar1)
node2 = makeNode(boar2)

     

while(1):
    print("computer's move:")
    populatechildren(rootNode, 2)
    buildTree(rootNode, 4)
    rootNode = minimax(rootNode, 2, 4)
    rootNode = makeNode(rootNode.board)
    printBoard(rootNode.board)

    x2 = int(input("enter y of peice: "))
    y2 = int(input("enter x of piece: "))
    m = int(input("enter move number: "))
    #print(c + " " + x2 + " " + y2 + " " + m)
    rootNode.board = movePieces(rootNode.board, x2, y2, 1, m)
    print("player's mve:")
    printBoard(rootNode.board)





































