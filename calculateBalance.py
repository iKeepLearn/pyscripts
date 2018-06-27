# -*- coding:utf-8 -*-
def calculateBalance(balance,annualInterestRate,monthlyPaymentRate,month=12):
    for i in range(1,month+1):
        balance = balance - (balance * (annualInterestRate/12) * monthlyPaymentRate)
        print("Month {} Remaining balance: {:.2f}".format(i,balance))
    print("Remainning balance:{:.2f}".format(balance))

balance = 42
annualInterestRate = 0.2
monthlyPaymentRate = 0.04
calculateBalance(balance,annualInterestRate,monthlyPaymentRate)
