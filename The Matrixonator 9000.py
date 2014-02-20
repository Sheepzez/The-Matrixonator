##AUTHOR: Isaac M Jordan (2080466)
##Copyright (C) 2013 Isaac M Jordan
from Canvas import *
from string import *
import json
import math

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
        print "Solving..."
        A = stepTwo(A)
        print "Solving..."
        A = stepThree(A)
        print "Solving..."
        i += 1
        j += 1

    print
            
    for row in A:
        for element in row:
            print rjust((repr(str(int(round((element)))))).strip('"\''),5),
        print
    print
    print
    
        


##Everything onwards is GUI and/or logic of program.


def printMatrix(A):
    ##Print out matrix A in a formatted (read: pretty) way
    print
    if type(A[0][0]) == float:
        for row in A:
            for element in row:
                print rjust((repr(str(int(round((element)))))).strip('"\''),5),
            print
    else:
        for row in A:
            for element in row:
                print rjust((repr(str(element))).strip('"\''),5),
            print
    print
    print
    

def mouseClickFront( mx, my, num ):
    if mx > 100 and mx < 245 and my > 50 and my < 100:
        inputPage()
    elif mx > 255 and mx < 400 and my > 50 and my < 100:
        deletePage()
    elif mx > 100 and mx < 245 and my > 125 and my < 175:
        listPage()
    elif mx > 255 and mx < 400 and my > 125 and my < 175:
        viewPage()
    elif mx > 100 and mx < 400 and my > 200 and my < 250:
        addPage()
    elif mx > 100 and mx < 400 and my > 275 and my < 325:
        multiplyPage()
    elif mx > 100 and mx < 400 and my > 350 and my < 400:
        solvePage()
    elif mx > 470 and mx < 498 and my > 5 and my < 30:
        with open('database.txt','w') as f:
            f.write(json.dumps(library))
        quitCanvas()
        print "Program closed. Thank you for using Matrixanator 9000!"


def mouseClickInput( mx, my, num ):
    if mx > 100 and mx < 400 and my > 50 and my < 100:
        print "This doesn't appear to do anything."
    elif mx > 470 and mx < 498 and my > 5 and my < 30:
        frontPage()


def mouseClickView( mx, my, num ):
    if mx > 100 and mx < 400 and my > 50 and my < 100:
        print "This doesn't appear to do anything."
    elif mx > 470 and mx < 498 and my > 5 and my < 30:
        frontPage()


def frontPage():
    set_mousedown_handler( mouseClickFront )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(100, 50, 245, 100, fill = "white") #Top Row Button
    create_text( 170, 75, text="Add matrix to library" )
    create_rectangle(255, 50, 400, 100, fill = "white") #Top Row Button
    create_text( 330, 75, text="Delete from library" )
    
    create_rectangle(100, 125, 245, 175, fill = "white") #Second Row Button
    create_text( 170, 150, text="List matrices in library" )
    create_rectangle(255, 125, 400, 175, fill = "white") #Second Row Button
    create_text( 330, 150, text="View contents of a matrix" )
    
    create_rectangle(100, 200, 400, 250, fill = "white") #Third Button
    create_text( 250, 225, text="Add two matrices" )
    
    create_rectangle(100, 275, 400, 325, fill = "white") #Fourth Button
    create_text( 250, 300, text="Multiply a matrix" )
    
    create_rectangle(100, 350, 400, 400, fill = "white") #Fifth Button
    create_text( 250, 375, text="Solve a matrix" )
    
    create_rectangle(470, 5, 498, 30, fill="red")
    create_text(412 ,15, text="Click X to save library")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)


def inputPage():
    set_mousedown_handler( mouseClickInput )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the matrix in the Python shell." )
    x = raw_input("Please enter a letter to assign the matrix to: ")
    setValue(getMatrix(), x)
    print "Matrix added!"
    frontPage()


def deletePage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the name of the matrix you want to delete, in the Shell." )
    x = raw_input("Please enter the name of a matrix: ")
    if x in library.keys():
        del library[x]
        print "Matrix deleted"
    else:
        print "Error, ",x,"is not a matrix that is in the library, please try again."
    frontPage()


def viewPage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the name of the matrix you want to view, in the Shell." )
    x = raw_input("Please enter the name of a matrix: ")
    if x in library.keys():
        printMatrix(getValue(x))
    else:
        print "Error, ",x,"is not a matrix that is in the library, please try again."
    frontPage()


def listPage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="""Please see the Shell for a printout of matrix names in the library.\n
If you want to see the contents of a matrix, use "View Matrix" from the main menu.""" )
    if len(library.keys()) != 0:
        for row in library.keys():
            if ','.join(row) != None:
                print ''.join(row)
    else:
        print "There are no matrices in the library. Please add some."

    


def addPage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the names of the matrices you want to add, in the Shell." )
    x = raw_input("Please enter the name of the first matrix: ")
    if x in library.keys():
        print "Chosen matrix:"
        printMatrix(getValue(x))
    else:
        print "Error, ",x,"is not a matrix that is in the library, please try again."
    y = raw_input("Please enter the name of the second matrix: ")
    if y in library.keys():
        print "Chosen matrix:"
        printMatrix(getValue(y))
    else:
        print "Error, ",y,"is not a matrix that is in the library, please try again."
    if checkAddCompatibility(getValue(x),getValue(y)) == True:
        i = raw_input("Do you want to add the resultant matrix to the library? (Y/N)")
        if i == "Y":
            z = raw_input("Please enter a name for the new resultant matrix: ")
            setValue(add(getValue(x),getValue(y)),z)
            print "Result:"
            printMatrix(getValue(z))
        else:
            print "Result:"
            printMatrix(add(getValue(x),getValue(y)))
        frontPage()
    else:
        print "These matrices are not compatible. Please choose compatible matrices."
        frontPage()


def multiplyPage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the name(s) of the matrice(s) you want to multiply, in the Shell." )
    x = raw_input("Please enter the name of the first matrix: ")
    if x in library.keys():
        print "Chosen matrix:"
        printMatrix(getValue(x))
        a = raw_input("Do you want to multiply this by a scalar, or another matix? (S/M)")
        if a == "M":             
            y = raw_input("Please enter the name of the second matrix: ")
            if y in library.keys():
                print "Chosen matrix:"
                printMatrix(getValue(y))
            
                if checkMultCompatibility(getValue(x),getValue(y)) == True:
                    i = raw_input("Do you want to add the resultant matrix to the library? (Y/N)")
                    if i == "Y":
                        z = raw_input("Please enter a name for the new resultant matrix: ")
                        print "Result:"
                        printMatrix(multiply(getValue(x),getValue(y)))
                        setValue(multiply(getValue(x),getValue(y)),z)
                    else:
                        print "Result:"
                        printMatrix(multiply(getValue(x),getValue(y)))
                    frontPage()
                else:
                    print "These matrices are not compatible. Please choose compatible matrices."
                    frontPage()
            else:
                print "Error, ",y,"is not a matrix that is in the library, please try again."
                frontPage()
        else:
            y = raw_input("Please enter a scalar integer to multiply the first matrix by: ")
            printMatrix(multiply(getValue(x),int(y)))
            frontPage()
    else:
        print "Error, ",x,"is not a matrix that is in the library, please try again."
        frontPage()


def solvePage():
    set_mousedown_handler( mouseClickView )
    create_rectangle(2,2, 500, 500, width = 5, outline = "blue", fill = "SkyBlue")
    create_rectangle(470, 5, 498, 30, fill="red")
    create_line(475,10,493,25, fill = "white", width = 4)
    create_line(493,10,475,25, fill = "white", width = 4)
    create_text( 250, 75, text="Please enter the name of the matrix you want to solve, in the Shell." )
    x = raw_input("Please enter the name of the first matrix: ")
    if x in library.keys():
        print "Chosen matrix:"
        printMatrix(getValue(x))
        print "Solving..."
        solveMatrix(getValue(x))
    else:
        print "Error, ",x,"is not a matrix that is in the library, please try again."
    frontPage()

set_size( 500, 500 )
frontPage()
run()







