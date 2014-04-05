from z3 import *

def toSSA(function):
    lines = function.split("\n")
    variables = []
    locations = []
    for i in range(len(lines)):
        line = lines[i]
        if line != "":
            match_string = " = "
            try:
                location = line.index(match_string)
                variable = line[0:location]
                variable = removeSpace(variable)
                variables.append((variable, i))
                locations.append(i)
            except ValueError:
                continue
    variables = changeVars(variables) 
    for l in locations:
        for var in variables:  
            if len(var) > 2 and var[2] <= l:
                if lines[l].index(" = ") > lines[l].index(var[0]):
                    lines[l] = lines[l].replace(var[0], var[1], 1)
                else:
                    lines[l] = lines[l].replace(var[0], var[1])
    for line in lines:
        print line

def changeVars(variables):
    for i in range(len(variables)):
        count = countVar(variables, variables[i][0])
        if count > 1:
          sub = 1
          new_var = ""
          for j in range(i+1, len(variables)):
              if variables[j][0] == variables[i][0]:
                  old_var = variables[j][0]
                  location = variables[j][1]
                  new_var = variables[j][0] + str(sub)
                  variables[j] = (old_var, new_var, location)
                  sub += 1
    return variables

def removeSpace(variable):
    variable = variable.lstrip()
    return variable
            

def countVar(variables, var):
    count = 0
    for i in variables:
        if i[0] == var:
            count += 1
    return count

function =  """
def series(t, d, n):
   sum = 2 * t
   sum = sum + d*(n-1)
   final = sum * n/2
"""

toSSA(function)

## In z3:
## def series(t, d, n):
##     summ = Int('summ')
##     p 2*t
##     Int(sum1) = summ + d*(n-1)
##     Int(final) = sum1 * n / 2
##     s = Solver()
##     s.add(summ, sum1, final)
    
