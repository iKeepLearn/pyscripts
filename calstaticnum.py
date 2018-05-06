#!/usr/bin/env python

def getNum():
    nums = []
    iNumStr = input('please inpurt a number(Enter for exit):')
    while iNumStr != "":
            nums.append(eval(iNumStr))
            iNumStr = input('please inpurt a number(Enter for exit):')
    return nums

def mean(numbers):
    s = 0.0
    for num in numbers:
        s = s + num
    return s / len(numbers)

def dev(numbers,mean):
    sdev = 0.0
    for num in numbers:
        sdev = sdev + (num - mean)**2
    return pow(sdev / (len(numbers)-1), 0.5)

def median(numbers):
    sorted(numbers)
    size = len(numbers)
    if size % 2 == 0:
        med = (numbers[size//2-1] + numbers[size//2])/2
    else:
        med = numbers[size//2]
    return med

n = getNum()
m = mean(n)
print('average:{},variance:{:.2},median:{}.'.format(m,dev(n,m),median(n)))
