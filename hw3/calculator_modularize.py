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
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens): #evaluate plus and minus
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
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
    tokens2 = [] 
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    number = 0
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
                token = {'type': 'NUMBER', 'number':  float(tokens2[-1]['number']) / float(tokens[index]['number'])}
                tokens2.pop(-1)
                tokens2.pop(-1)
            else:
                print 'Invalid syntax'
        index += 1
        tokens2.append(token)
    return tokens2


def test(line, expectedAnswer):
    tokens2 = tokenize(line)
    tokens = evaluate2(tokens2)
    actualAnswer = evaluate(tokens)
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
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens2 = tokenize(line)
    tokens = evaluate2(tokens2)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer