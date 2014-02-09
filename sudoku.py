from z3 import *
import fileinput

s = Solver()
boxes = []
i = 0
for row in fileinput.input():
    i += 1
    split_row = row.split(" ")
    for j in split_row:
        print j
        if j != ".":
            box = "x" + str(i) + str(split_row.index(j)+1)
            print box
            box = Int(box)
            s.add(box == j)
            print s
    
## for i in range(1, 3):
##     split_row = []
##     boxes = []
##     row = raw_input("Please enter the " + str(i) + "th row of the sudoku puzzle. Empty spaces should be indicated by '.' " )
##     split_row = row.split(" ")
##     for j in split_row:
##         print j
##         if j != ".":
##             box = "x" + str(i) + str(split_row.index(j)+1)
##             print box
##             box = Int(box)
##             s.add(box == j)
##             print s


box = ""
for i in range(1, 10):
    for j in range(1, 10):
        box = "x" + str(i) + str(j)
        box = Int(box)
        s.add(And(box>=1, box<=9))
        boxes.append(box)
print "Boxes!!!!", boxes
position = 0

def getRow(boxes, rownum):
    row = []
    for box in boxes:
        box = str(box)
        if box[1] == str(rownum):
            row.append(box)
    return row
def getColumn(boxes, colnum):
    col = []
    for box in boxes:
        box = str(box)
        if box[2] == str(colnum):
            col.append(box)
    return col
def getBox(boxes, boxnum):
    box = []
    if boxnum == 1:
        for b in boxes:
            b = str(b)
            if 0 < int(b[1]) and 4 > int(b[1]) and 0 < int(b[2]) and 4 > int(b[2]):
                box.append(b)
    if boxnum == 2:
        for b in boxes:
            b = str(b)
            if 0 < int(b[1]) and 4 > int(b[1]) and 3 < int(b[2]) and 7 > int(b[2]):
                box.append(b)
    if boxnum == 3:
        for b in boxes:
            b = str(b)
            if 0 < int(b[1]) and 4 > int(b[1]) and 6 < int(b[2]) and 10 > int(b[2]):
                box.append(b)
    if boxnum == 4:
        for b in boxes:
            b = str(b)
            if 3 < int(b[1]) and 7 > int(b[1]) and 0 < int(b[2]) and 4 > int(b[2]):
                box.append(b)
    if boxnum == 5:
        for b in boxes:
            b = str(b)
            if 3 < int(b[1]) and 7 > int(b[1]) and 3 < int(b[2]) and 7 > int(b[2]):
                box.append(b)
    if boxnum == 6:
        for b in boxes:
            b = str(b)
            if 3 < int(b[1]) and 7 > int(b[1]) and 6 < int(b[2]) and 10 > int(b[2]):
                box.append(b)
    if boxnum == 7:
        for b in boxes:
            b = str(b)
            if 6 < int(b[1]) and 10 > int(b[1]) and 0 < int(b[2]) and 4 > int(b[2]):
                box.append(b)
    if boxnum == 8:
        for b in boxes:
            b = str(b)
            if 6 < int(b[1]) and 10 > int(b[1]) and 3 < int(b[2]) and 7 > int(b[2]):
                box.append(b)
    if boxnum == 9:
        for b in boxes:
            b = str(b)
            if 6 < int(b[1]) and 10 > int(b[1]) and 6 < int(b[2]) and 10 > int(b[2]):
                box.append(b)
    return box

for i in range(1, 10):
    row = getRow(boxes, i)
    print row
    position = 0
    for box1 in row[position:]:
        b1 = Int(box1)
        for box2 in row[position+1:]:
            b2 = Int(box2)
            s.add(b1 != b2)
        position += 1
        
for i in range(1, 10):
    box = getBox(boxes, i)
    print "Boxes are: ", box
    position = 0
    for box1 in box[position:]:
        b1 = Int(box1)
        for box2 in box[position+1:]:
            b2 = Int(box2)
            s.add(b1 != b2)
        position += 1


for i in range(1, 10):
    col = getColumn(boxes, i)
    position = 0
    for box1 in col[position:]:
        b1 = Int(box1)
        for box2 in col[position+1:]:
            b2 = Int(box2)
            s.add(b1 != b2)
        position += 1


for c in s.assertions():
    print c
s.check()
print s.statistics()

m = s.model()
sort = []
for d in m.decls():
    print "%s = %s" % (d.name(), m[d])
  ##   sort.append(d)
## isSorted = sortList(sort)
## count = 1
## for i in isSorted:
##     if count % 10 == 0:
##         print "\n"`
##     print m[i]
##     count += 1
## def sortList(notSorted):
##     isSorted = []
##     for box in notSorted:
##         for i in range(1, 10):
##             for j in range(1, 10):
##                 if str(box) == "x" + str(i) + str(j):
##                     isSorted.append(box)
##     return isSorted
        
