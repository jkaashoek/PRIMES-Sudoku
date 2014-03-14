import random
import string

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

def removePlaces(l, num_places):
    location = len(l)
    copy = l[0:]
    locations = []
    blanks = []
    while num_places > 0:
        while location >= len(l) or l[location] == "_":
            location = random.randint(0, len(l)-1)
        locations.append(location)
        l[location] = "_"
        num_places -= 1
    locations = Order(locations)
    for i in locations:
        blanks.append(copy[i])
    return l, blanks

def Order(blanks):
    length = len(blanks)
    organized = []
    while len(organized) < length:
        least = blanks[0]
        for i in range(len(blanks)):
            if blanks[i] < least:
                least = blanks[i]
        organized.append(least)
        blanks.remove(least)
    return organized

def makeGuessesList(user_guesses, right_length):
    guesses = []
    location = 0
    listofstrings = user_guesses.split()
    for i in listofstrings:
            i = int(i)
            guesses.append(i)
    if len(guesses) != right_length:
        return "Incorrect number of blanks!" 
    return guesses

def evalUser(guesses, blanks, myList):
    num_wrong = 0
    pos_incorrect = []
    right = True
    for i in range(len(blanks)):
        if guesses[i] != blanks[i]:
            right = False
            pos_incorrect.append(i)
            num_wrong += 1
    if right:
        print "All of your guesses were correct! Nice job!"
        return
    else:
        print "You had", num_wrong, "incorect guess(es)."
        for i in pos_incorrect:
            print "Blank", i+1, "was incorrect."
        return

def printList(l):
    for i in range(len(l)):
        print l[i],

def getInput():
    listlength = raw_input("How long would you like the list to be? ")
    num_places = raw_input("How many places would you like to remove? ")
    num_places = int(num_places)
    listlength = int(listlength)
    l1 = [0, 4, 6, 7, 3, 9, 2, 4]
    l2 = [3, 43, 22, 0, -1, -7, 8, 83]
    myList = makeList(listlength, l1, l2)
    myList, blanks = removePlaces(myList, num_places)
    printList(myList)
    user_guesses = raw_input("What do you think the blanks are? ")
    user_guesses = makeGuessesList(user_guesses, len(blanks))
    if type(user_guesses) == str:
        print user_guesses
        return
    evalUser(user_guesses, blanks, myList)

getInput()
