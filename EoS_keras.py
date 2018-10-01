# -*- coding: utf-8 -*-
#P76071200
#Chung-Yao Ma
#Course IR HW1

#from keras.preprocessing import sequence
#from keras.preprocessing.text import Tokenizer
import re
import os
import spacy
word_dic = spacy.load('en')

def change(text):
    result = []
    doc = word_dic(text)
    for i in range(len(doc)):
        result += [doc[i].pos_]
    return result

file = open('eos_x_train.txt','r', encoding='utf-8')
text = file.read().splitlines()

sentence = str(text[0]).split('.')
#x_train
train_sentence = []

count = 0
for item in sentence:
    count += 1
    print(count)
    print(item)

    train_sentence.append(item)
    
#y_train    
label = []
for i in range(len(train_sentence)):
    label.append(1)
neg = [0,1,4,5,30,31,32,33,34,50,51,52,53,54,55,56,57,58,59,60,61,62,100,101,103,104,129,130,131,132,133,161,162,163,165,166,174,175
               ,187,188,189,190,201,202,209,210,216,217,266,267,290,294,297,383,384,463,464,466,467,468,469,470,471,472,542,544,546,548,550
               ,622,623,680,681,682,731,732,733,734,735,736,737,738,740,741,828,829,830,831,833,834,856,857]
for i in neg:
    label[i] = 0

x_train = []
print("Start for changing")
for s in range(len(train_sentence)):
    x_train += [change(train_sentence[s])]
#x_train = [change(train_sentence[0])]


print("Wait for changing")
print(x_train)

word_index = {'SPACE': 0, 'ADP':1, 'ADV':2, 'AUX':3, 'CONJ':4, 'CCONJ':5, 'DET':6, 'INTJ':7, 'NUM':8, 'PART':9, 'PRON':10,
              'PROPN':11, 'PUNCT':12, 'SCONJ':13, 'SYM':14, 'VERB':15, 'NOUN':16, 'X':17, 'ADJ': 18 }

num_x_train = []
all_text = []
for text in x_train:
    for word in text:
        all_text.append(word_index[word])
    num_x_train.append(all_text)
    all_text = []

print(num_x_train)

