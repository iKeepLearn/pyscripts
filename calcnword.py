#!/usr/bin/env python
import jieba
import os
def getText(text):
    txt = open(text,'r',encoding='utf-8').read()
    txt = txt.lower()
    for ch in '!~@#$%^&*()_-{}|:"?><[]\';.,/\\':
        txt = txt.replace(ch," ")
    return txt


filepath = input('please input the file path:')
wordtxt = getText(filepath)
words = jieba.lcut(wordtxt)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word,0) + 1

items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
for i in range(15):
    word,count = items[i]
    print('{0:<10}{1:>5}'.format(word,count))
