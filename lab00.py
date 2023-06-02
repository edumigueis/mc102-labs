sequenceIndex = int(input())

def getFibonacciByIndex(number):
    prev = 1
    cur = 1
    index = 2
    nxt = 1
    while index < number:
        nxt = cur + prev
        prev = cur
        cur = nxt
        index += 1
    return nxt

if sequenceIndex < 1:
    print("Por favor selecione um número positivo.")
else:
    print('O termo na posição %i da sequência de Fibonacci é: %i.' % (sequenceIndex, getFibonacciByIndex(sequenceIndex))) 
