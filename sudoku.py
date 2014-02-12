from z3 import *
import fileinput

## boxes = []
## i = 0
## for row in fileinput.input():
##     i += 1
##     split_row = row.split(" ")
##     for j in split_row:
##         print j
##         if j != ".":
##             box = "x" + str(i) + str(split_row.index(j)+1)
##             print box
##             box = Int(box)
##             s.add(box == j)
##             print s


# Creates all sudoku squares
boxes = [[Int("x%d%d" % (i,j)) for i in range(1,10)] for j in range(1,10)]

# Sets the condition that the value of each square must be between 1 and 9
valid = [And(boxes[i][j] <= 9, boxes[i][j] >= 1) for i in range(9) for j in range(9)]

# Sets the condition that the value of each box in every row must be distinct
row_dist = [Distinct(boxes[i]) for i in range(9)]

# Sets the condition that the value of each box in every column must be distinct
col_dist = [Distinct([boxes[i][j] for i in range(9)]) for j in range(9)]

# Sets the condition that the values in each 3 x 3 square must be different
def getThreebyThrees():
    three_by_threes = [] # this will be a list of all three by three squares
    # the next piece of code makes every 3 x 3 square and appends to the list of all three by three squares
    for k in range(3):
        for l in range(3):
            three_by_three = []
            for i in range(3):
                for j in range(3):
                    three_by_three.append(boxes[3*k + i][3*l + j])
            three_by_threes.append(three_by_three)
    return three_by_threes

all_squares = getThreebyThrees()
for three_by_three in all_squares:
    position = 0
    for box1 in three_by_three[position:]:
        for box2 in three_by_three[position + 1:]:
            s.add(box1 != box2)
        position += 1

            
s = Solver()

s.add(valid + row_dist + col_dist)

# Prints the sudoku board
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(boxes[i][j]) for j in range(9) ] 
          for i in range(9) ]
    print_matrix(r)
else:
    print "failed to solve"


        
        
        
