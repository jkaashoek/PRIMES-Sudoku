from sklearn import svm
import json
import random


#X = [[0, 0], [1, 1]]
#y = [0, 1]

inFile = open('vectors.txt', 'r')
vectors = []

for line in inFile:
    vectors.append(json.loads(line))

def test():

    div = 37

    clf = svm.SVC()

    x1 = []
    y1 = []
    
    for i in range(div):
        x1.append(vectors[i][1:])
        y1.append(vectors[i][0])

    clf.fit(x1, y1)
    #x = clf.predict(vectors[1][1:])

    #print(x)
    #print(vectors[1][0])

    p1 = []
    c1 = []
    for i in range(div + 1, len(vectors)):
        p1.append(int(clf.predict(vectors[i][1:])))
        c1.append(vectors[i][0])
        
    print(p1)
    print(c1)

    count = 0

    for k in range(len(p1)):
        if (p1[k] == c1[k]):
            count+=1

    print(str(count) + " out of " + str(len(p1)))

def same_values(vec):
    i = 0
    while (i < len(vec) - 1):
        if vec[i] != vec[i + 1]: return False
        i += 1
    return True


def learn(n):
    indices = [i for i in range(0, len(vectors))]
    learnSample = random.sample(indices, n)
    learnSample.sort()

    x = []
    y = []
    for j in learnSample:
        x.append(vectors[j][1:])
        y.append(vectors[j][0])
    
    while (same_values(y)):
        learnSample = random.sample(indices, n)
        learnSample.sort()
    
        x = []
        y = []
        for j in learnSample:
            x.append(vectors[j][1:])
            y.append(vectors[j][0])


    print(x)
    print(y)
    clf = svm.SVC()
    
    clf.fit(x, y)

    predicted = []
    actual = []
    
    for k in range(0, len(vectors)):
        if (k not in learnSample):
            predicted.append(int(clf.predict(vectors[k][1:])))
            actual.append(vectors[k][0])

    count = 0
    for i in range(len(predicted)):
        if(predicted[i] == actual[i]):
            count += 1

    return count

def average(n, times_to_test):

    s = 0
    learned = []
    for i in range(times_to_test):
        num = learn(n)
        learned.append(num)
        print("Trial " + str(i) + ": " + str(num) + " out of " + str(len(vectors) - n))
        s+= num
    average = s/float(times_to_test)
    print("Average: " + str(average) + " out of " + str(len(vectors) - n) + " (" + str(len(vectors)) + " puzzles total)")
    percent = average/(len(vectors) - n)*100
    print("Result: " + str(percent))

    '''
    standard_dev = 0
    for n in learned:
        standard_dev += (average - n)**2
        print("Added " + str((average - n)**2))
    standard_dev = standard_dev/float(len(learned))

    print("Standard deviation: " + str(standard_dev))
    '''

    return percent


def choose_n(percentage):
    n = percentage*len(vectors)/100
    return n

def main():
    type = input("Percentage or number? Enter p for percentage and n for number " )
    if type == 'p':
        percentage = int(input("What percentage to learn? "))
        average(choose_n(percentage), 200)
    else:
        n = int(input("How many to learn? "))
        average(n, 200)

def save():
    outFile = open('results.txt', 'w')
    for p in range(1, 20):
        percentage = p*5
        percent_success = average(choose_n(percentage), 500)
        outFile.write(str(percentage) + "% of puzzles used in learning set: ")
        outFile.write('\t')
        outFile.write(str(percent_success))
        outFile.write('\n')
    outFile.close()


save()