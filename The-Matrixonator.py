import Tkinter
import json
import math
from string import *

global library
with open('database.txt','r') as f:
    library = json.load(f)


def getMatrix():
    end = False
    matrix = []
    while end == False:
        A = raw_input("""Enter "end" to stop, or enter your row of numbers, seperated by spaces: """)
        if A == "end":
            end = True
        else:
            if any(b.isalpha() for b in A):
                print "Error: You cannot enter letters."
            else:
                A = A.split()
                matrix.append(A)
    ##Check length of rows are equal
    for x in range(1, len(matrix)-1):
        if len(matrix[0]) != len(matrix[x]):
            print "Error: Matrix rows are not all equal length."
            ##Repeat until user gets it right
            getMatrix()
            return
    return matrix
    
    
def setValue(A, v):
    ##Adds matrix to dictionary, denoted by a letter
    global library
    library[v] = A


def getValue(v):
    ##Returns the matrix with assignment v
    return library[v]


def checkMultCompatibility(A,B):
    ##Check that the row length of A is the same as the column depth of B
    ##This is a check if you can multiply matrices A and B together.
    ##Assumes that all rows and columns are the same length
    if type(B) == int:
        return True
    if len(A) != len(B[0]):
        return False
    return True
    

def multiply(A,B):
    ##Return the matrix of the product of AB
    ##First: Check if the multiplication method is scalar
    C = [[0 for _ in range(len(A))] for i in range(len(A[0]))]
    if type(B) == int:
        for x in range(0,len(A)):
            for y in range(0,len(A[0])):
                C[x][y] = B*int(A[x][y])
    ##Else check if B is a matrix
    ##NOTE: IT IS ASSUMED THE MATRICES ARE COMPATIBLE
    elif type(B) == list:
        m = len(A)
        i,j,k = 0,0,0
        while i < m:
            while j < m:
                while k < m:
                    C[i][j] = int(C[i][j]) + int(A[i][k]) * int(B[k][j])
                    k += 1
                j += 1
                k = 0
            i += 1
            j = 0

    ##Translate elements from integers BACK to string!
    for x in range(0,len(C)):
        for y in range(0,len(C[0])):
            C[x][y] = str(C[x][y])
    return C


def checkAddCompatibility(A,B):
    ##Check that the dimensions of A is the same as the dimensions of B
    ##This is a check if you can add/subtract matrices A and B.
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    return True


def add(A,B):
    #Return the matrix of A+B
    C = [[0 for _ in range(0,len(A[0]))] for i in range(0,len(A))]
    for x in range(0,len(A)):
        for y in range(0,len(A[0])):
            C[x][y] = int(A[x][y]) + int(B[x][y])

    ##Translate elements from integers BACK to string!
    for x in range(0,len(C)):
        for y in range(0,len(C[0])):
            C[x][y] = str(C[x][y])
    return C
    

def solveMatrix(A):
    #Return the solutions of augmented matrix A
    ##i,j are the Row/Column currently being dealt with. "x,y" used as placeholder for searching etc
    global i,j
    i,j = 0,0 #Start at first (top-left) position
    
    def ERO1(A, r1, r2):
        #Swaps row r1 and row r2 and returns the matrix A
        A[r2], A[r1] = A[r1],A[r2]
        return A
        

    def ERO2(A, r, c):
        #Multiply row r of matrix A by scalar c, return new matrix
        A[r] = [n*c for n in A[r]]
        return A
        

    def ERO3(A, r1, r2, c):
        #Add a multiple c of row r2 to row r1 and return matrix A
        A[r1] = map((lambda x,y: x+y), [n*c for n in A[r2]], A[r1])
        return A

    #http://www.csun.edu/~panferov/math262/262_rref.pdf
    # i,j     i,j+1     i,j+2
    # i+1,j   i+1,j+1   i+1,j+2
    # i+2,j   i+2,j+2   i+2,j+2 etc
    
    def stepOne(A):
        global i,j ##Current pivot coords
        #If A[i][j] = 0 swap the ith row with some other row (A[i+b]) below to make A[i][j] not 0.
        #This A[i][j], non-zero entry is called a pivot.
        #If all entries in the column are zero, increase j by 1
        
        x,b = 0,0
        while A[i][j] == 0 and i+b < len(A):
            if A[i+b][j] == 0:
                    b += 1
            else:
                A = ERO1(A, i, (i+b))
        if A[i][j] == 0:
            j += 1
            stepOne(A,i,j)
        return A


    def stepTwo(A): #Matrix A
        global i,j ##Current pivot coords
        #Divide the ith row by A[i][j] to make the pivot entry = 1
                   
        A = ERO2(A,i,(1/A[i][j]))
        return A


    def stepThree(A):
        global i,j ##Current pivot coords
        #Eliminate all other entries in the
        #jth column by subtracting suitable multiples of the
        #ith row from the other rows
        x,y = 0,0
        while x < len(A):
            if A[x][j] != 0 and x != i:
                #If this entry in the jth column isn't zero
                #and it's not the ith row make it zero
                A = ERO3(A,x,i,(A[x][j]*-1))
            x += 1
        return A


    for x in range(0,len(A)):
        for y in range(0,len(A[0])):
            A[x][y] = float(A[x][y])
            
    while i < len(A) and j < len(A[0]):
        A = stepOne(A)
        A = stepTwo(A)
        A = stepThree(A)
        i += 1
        j += 1
            
    return A

##End of functions!

top = Tkinter.Tk()
top.geometry("500x700")




Tkinter.mainloop()
