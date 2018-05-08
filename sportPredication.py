#!/usr/bin/env python
from random import random
def printIntro():
    print('This program simulate some sort of athletic\
    competition between two athletes')
    print('Program running requires A and B capabilities\
    (Decimal between 0 and 1)')

def getInputs():
    a = eval(input('please input athlete A\'s capabilites(Decimal between 0 and 1):'))
    b = eval(input('please input athlete B\'s capabilites(Decimal between 0 and 1):'))
    n = eval(input('simulate games number:'))
    return a,b,n

def printSummary(winsA,winsB):
    n = winsA + winsB
    print('Athletic analyze begin... simulate {} games'.format(n))
    print('athlete A wins {} games,accounting {:0.1%}'.format(winsA,winsA/n))
    print('athlete B wins {} games,accounting {:0.1%}'.format(winsB,winsB/n))

def gameOver(a,b):
    return a==15 or b==15


def simOneGame(probA,probB):
    scoreA,scoreB = 0,0
    serving = 'A'
    while not gameOver(scoreA,scoreB):
        if serving == 'A':
            if random() < probA:
                scoreA += 1
            else:
                serving = 'B'
        else:
            if random() < probB:
                scoreB += 1
            else:
                serving = 'A'
    return scoreA,scoreB

def simNGames(n,probA,probB):
    winsA,winsB = 0,0
    for i in range(n):
        scoreA,scoreB = simOneGame(probA,probB)
        if scoreA > scoreB:
            winsA += 1
        else:
            winsB += 1
    return winsA,winsB



def main():
    printIntro()
    probA,probB,n = getInputs()
    winsA,winsB = simNGames(n,probA,probB)
    printSummary(winsA,winsB)

main()
