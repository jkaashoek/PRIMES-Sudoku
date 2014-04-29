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
    lines = changessa(lines, variables)
    for line in lines:
        print line
        print "\n"

def changessa(lines, variables):
    oldtonew = {}
    for line in lines:
        try:
            equalloc = line.index("=")
            for var in variables:
                if var in line[equalloc:]:
                    if var in oldtonew.keys():
                        line[equalloc:].replace(var, oldtonew[var])
                if var in line[0:equalloc]:
                    isin, loc, var = varinline(variables, line)
                    count = countBefore(loc, variables, var)
                    if count > 0:
                        oldtonew[var] = var + str(count)
        except:
            for var in variables:
                if var in line and var in oldtonew.keys():
                    line[equalloc:].replace(var, oldtonew[var])
        return lines
            
            
            

def varinline(variables, line):
    for i in range(len(variables)):
        if variables[i] in line:
            return True, i, variables[i]
    return False

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
            

def countBefore(loc, variables, var):
    count = 0
    for i in range(loc):
        if variables[i] == var:
            count += 1
    return count

function =  """
def series(t, d, n):
   s = s
   s = s
   s = s
   s = s
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


We have: all variables and lines
Go through each line. If a variable that has shown up before is set equal to something, this variable will become the var + the # of time that var appears before that.
We will add to a dict the old value of the variable, mapping to the new one. Ev=
