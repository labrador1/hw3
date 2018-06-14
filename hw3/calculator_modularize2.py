def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1 

def readOpen(line, index):
    token = {'type': 'OPEN'}
    return token, index + 1  

def readClose(line, index):
    token = {'type': 'CLOSE'}
    return token, index + 1    

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readOpen(line, index)
        elif line[index] == ')':
            (token, index) = readClose(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def evaluate(tokens): #evaluate plus and minus
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer

def evaluate2(tokens): #evaluate multiply and divide
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    number = flag = close = 0
    token = {'type': 'PLUS'}
    tokens = parenthesis(tokens)
    tokens2 = []
    while index < len(tokens):
        if tokens[index]['type'] == 'PLUS':
            token = {'type': 'PLUS'}
        elif tokens[index]['type'] == 'MINUS':
            token = {'type': 'MINUS'}
        elif tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
                token = {'type': 'NUMBER', 'number': tokens[index]['number'] }
            elif tokens[index - 1]['type'] == 'MULTIPLY':
                token = {'type': 'NUMBER', 'number':  tokens2[-1]['number'] * tokens[index]['number']}
                tokens2.pop(-1)
                tokens2.pop(-1)
            elif tokens[index - 1]['type'] == 'DIVIDE':
                token = {'type': 'NUMBER', 'number':  tokens2[-1]['number'] / tokens[index]['number']}
                tokens2.pop(-1)
                tokens2.pop(-1)
            else:
                print 'Invalid syntax'
                print(tokens[index - 1]['type'])
        index += 1
        tokens2.append(token)
    return tokens2

def parenthesis(tokens): #evaluate parenthesis
    flag = index = close = 0
    tokens2 = []
    tokens3 = []
    while index < len(tokens):
        flag = close = 0
        if tokens[index]['type'] == 'PLUS':
            token = {'type': 'PLUS'}
        elif tokens[index]['type'] == 'MINUS':
            token = {'type': 'MINUS'}
        elif tokens[index]['type'] == 'MULTIPLY':
            token = {'type': 'MULTIPLY'}
        elif tokens[index]['type'] == 'DIVIDE':
            token = {'type': 'DIVIDE'}
        elif tokens[index]['type'] == 'NUMBER':
            token = {'type': 'NUMBER', 'number': tokens[index]['number'] }
        elif tokens[index]['type'] == 'OPEN':
            index += 1
            flag = 1
            tokens2 = []
            while tokens[index]['type'] != 'CLOSE' or flag != close + 1:  
                if(tokens[index]['type'] == 'OPEN'):
                    flag += 1
                    cacco = tokens[index] 
                elif(tokens[index]['type'] == 'CLOSE'):
                    close += 1
                    cacco = tokens[index]
                else:
                    cacco = tokens[index]
                index += 1
                tokens2.append(cacco) 
            test = evaluate2(tokens2)
            test = evaluate(test)
            token = {'type': 'NUMBER', 'number': test}
        index += 1
        tokens3.append(token) 
    return tokens3

def test(line, expectedAnswer):
    tokens = tokenize(line)
    tokens2 = evaluate2(tokens)
    actualAnswer = evaluate(tokens2)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)

# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1", 1)
    test("1+2", 3)
    test("1.0+2", 3)
    test("1.0+2.0", 3)
    test("1-2", -1)
    test("1.0-2", -1)
    test("1.0-2.0", -1)
    test("1.0+2.1-3", 0.1)
    test("1*2", 2)
    test("1*2+1", 3)
    test("1*2-1", 1)
    test("1.0*2", 2)
    test("1.0*2.0", 2)
    test("1/2", 0.5)
    test("1/2+1", 1.5)
    test("1/2-1", -0.5)
    test("1*2/2", 1)
    test("1*2+1/2", 2.5)
    test("1*2-1/2", 1.5)
    test("1.0*2/2", 1)
    test("1.0*2.0/2", 1)
    test("3.0+4*2-10/5", 9)
    test("(2+3)*2",10)
    test("2*(2+3)*(2+4)",60)
    test("(3.0+4*(2-1))/5",1.4)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    tokens2 = parenthesis(tokens)
    tokens3 = evaluate2(tokens2)
    answer = evaluate(tokens3)
    print "answer = %f\n" % answer
