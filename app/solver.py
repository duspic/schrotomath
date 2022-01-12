## Here layeth the functions for parsing and solving simple equations
## The main functions are (in order in which they should be used):
#   predictionsToEquation() - which takes in a list of predicted characters classes and returns a mathematical equation
#   unaryMinuses() - which takes in the prepared equation and deals with minuses, separating them into operational and unary ones
#   shuntingYard() - which takes the finally-processed equation and turns it into one of postfix notation
#   solvePostFix() - which solves the equation.

## The other functions help them along the way, and are pretty self-explainatory.

def classToSymbol(label):
    # Simply decypher what math symbol represents the given label

    pairs = {
        "minus":"-",
        "plus":"+",
        "multi":"*",
        "div":"/",
        "(":"(",
        ")":")"
        }

    return pairs[label]
        
def groupDigits(equation):
    # Each character is parsed separately, but numbers aren't always single characters
    # Group all consecutive digits in a list

    output = []
    number = ""

    for char in equation:
        if char.isdigit():
            number += char
        else:
            if number:
                output.append(number)
                number = ""
            output += char

    if number:
        output.append(number)

    return output

def predictionsToEquation(predictions):
    # Takes list of predicted characters and processes them
    # meanwhile cleaning up the eventual messy predictions

    # A simple rule is that [')','multi','plus','div'] must come after a digit or a right parenthesis
    # If they don't follow the rule, just ^rule^ them out as a mistake by a predictor

    # It would be wiser to try to intelligently assume what was mispredicted...

    rule_condition = False
    output = []

    for char in predictions:
        if char.isdigit():
            output += char
            rule_condition = True
        
        elif char in ['(','minus']:
            char = classToSymbol(char)
            output += char
            rule_condition = False

        elif char in [')','multi','plus','div']:
            if rule_condition:
                char = classToSymbol(char)
                output += char
                rule_condition = True if char == ')' else False
            else:
                continue
    
    return groupDigits(output)

def unaryMinuses(equation):
    # If a minus appears after a digit or a right parenthesis, it's safe to asume it is a regular operator
    # If it appears after operators (except a right parenthesis), it's an unary minus
    # And if it appears as the first character, it is unary

    output = []
    previous = ''

    for char in equation:

        if char == '-':
            if previous.isdigit() or previous == ')':
                output.append(char)
                previous = '-'
            
            elif previous in ['+','-','*','/','(','']:
                previous = 'unary'
        
        else:
            if previous == 'unary':

                if char == '(':
                    output.append("-1")
                    output.append("*")
                    output.append(char)
                else:
                    output.append('-'+char)

            else:
                output.append(char)

            previous = char

    return output

def checkPrecedence(op1, op2):
    # Returns True if op2 is of greater precedence
    if op1 in ["+","-"] and op2 in ["*","/"]:
        return True

    return False

def shuntingYard(equation):
    # There's a thorough explanation on wikipedia on which this code is based
    # Check it out if something isn't clear https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    # I've tweaked it a bit, to cover cases with unary minuses

    output = []
    operators = []
    
    for element in equation:
       
       # .isdigit() will return False for negative numbers
       # a workaround is to take the first char from behind ;)
        if element[-1].isdigit():
            output.append(element)


        # Currently, the only supported operators are the basic ones
        elif element in ["+",'-','*','/']:
            
            if operators:
                op2 = operators[-1]
                # No need to check for associativity since all of them are left-associative
                if op2 != '(' and checkPrecedence(element,op2):
                    output.append(operators.pop())
            operators += element

        elif element == '(':
            operators += element
        
        # If there's a right parenthesis, pop everything since the left one.
        # But discard the parenthesis themselves
        elif element == ')':
            if "(" in operators:
                op = operators.pop()
                
                while op != "(":
                    output.append(op)
                    op = operators.pop()

    while operators:
        op = operators.pop()
        if op == '(':
            raise TypeError("Parenthesis mismatch!")
        output.append(op)
    
    return output

def solvePostfix(equation):

    output = []

    for element in equation:
        if element[-1].isdigit():
            output.append(element)
        
        else:
            try:
                second = int(output.pop())
                first = int(output.pop())
            except:
                return "SOMETHING'S MISSING"
            
            if element == '/':
                output.append(first/second)
            elif element == '*':
                output.append(first*second)
            elif element == '+':
                output.append(first+second)
            elif element == '-':
                output.append(first-second)
            
    return output

def preparePrint(list):

    output = ""

    for element in list:
        output += str(element)
    
    return output