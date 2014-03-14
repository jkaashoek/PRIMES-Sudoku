import random



def makeList(listlength, l1, l2):
    # This is a simple program that randomly chooses a segment from l1 and l2 and appends them.
    # I am not sure if this is what this program is supposed to do...
    frombeglist1 = random.randint(1, listlength-1)
    toendlist1 = len(l1) - frombeglist1
    frombeglist2 = abs(listlength - frombeglist1)
    toendlist2 = len(l2) - frombeglist2
    #x = l1[toendlist1:] # takes last elements from list1
    #y = l2[toendlist2:] # takes last elements from list2
    x = l1[0:frombeglist1] # takes elements from the beginning of list1
    y = l2[0:frombeglist2] # takes elements from the beginning of list2
    x += y
    return x

def getInput():
    listlength = raw_input("How long would you like the list to be? ")
    listlength = int(listlength)
    l1 = [0, 4, 6, 7, 3, 9, 2, 4]
    l2 = [3, 43, 22, 0, -1, -7, 8, 83]
    myList = makeList(listlength, l1, l2)
    print myList

getInput()
