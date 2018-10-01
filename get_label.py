#P76071200
#Chung-Yao Ma
#Course IR HW1

import os

file = open('eos_x_train.txt','r', encoding='utf-8')
text = file.read().splitlines()


sentence = str(text[0]).split('.')
train_sentence = ''

count = 0
for item in sentence:
    count += 1
    print(count)
    print(item)

    train_sentence += item
    
print(train_sentence)

print("write x")
f= open("x_train.txt","w+")
f.write(train_sentence)
f.close()
print("end write x")

label = ''
for i in range(len(train_sentence)):
    label.append(1)
neg = [0,1,4,5,30,31,32,33,34,50,51,52,53,54,55,56,57,58,59,60,61,62,100,101,103,104,129,130,131,132,133,161,162,163,165,166,174,175
               ,187,188,189,190,201,202,209,210,216,217,266,267,290,294,297,383,384,463,464,466,467,468,469,470,471,472,542,544,546,548,550
               ,622,623,680,681,682,731,732,733,734,735,736,737,738,740,741,828,829,830,831,833,834,856,857]
for i in neg:
    label[i] = 0

print("write y")
f= open("y_train.txt","w+")
f.write(str(label))
f.close()
print("end write y")

