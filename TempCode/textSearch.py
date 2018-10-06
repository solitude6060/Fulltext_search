import re
import os
from nltk.tokenize import word_tokenize
#from keras.preprocessing.text import Tokenizer
import string

def remove_tag(text):
	re_tag = re.compile(r'(<[^>]+>|"|-|<|>|\,)')
	return re_tag.sub('',text)
  #return re_tag

def sp(text):
	SPLIT_RE = re.compile(r'[^a-zA-Z0-9]')
	return SPLIT_RE.sub(' ', text)

def dot(text):
	dot_re = re.compile(r'[^a-zA-Z0-9.]')
	return dot_re.sub(' ', text)

def read_files():
	file_list =[]
	all_texts =[]
	path = "./data/"

	for f in os.listdir(path):
		file_list +=[path+f]

	for fi in file_list:
		with open(fi , encoding='utf-8') as file_input:
			all_texts += [remove_tag(" ".join(file_input.readlines()))]

	return all_texts

all_text_dot =[]
all_text_str = []
file_list =[]
path = "./data/"
for f in os.listdir(path):
	file_list +=[path+f]

print("file_list : ",file_list)

for fi in file_list:
		with open(fi , encoding='utf-8') as file_input:
			all_text_str += [sp(" ".join(file_input.read(300).splitlines())).split()]
			all_text_dot += [dot(" ".join(file_input.read(300).splitlines())).split('.')]

print("DOT : ", all_text_dot)
print(all_text_str)

#tokenized_sents = [word_tokenize(i) for i in all_texts]
#for i in tokenized_sents:
#	print(i)
print("DOT : ", all_text_dot[0][0], len(all_text_dot[0]))
print(all_text_str[0][0], len(all_text_str[0]))
'''
dic = {}
key = range(len(tokenized_sents[0]))
for i in key:
	dic[i] = tokenized_sents[0][i]
'''
#print(dic)
key = range(len(all_text_str[0]))
textset = tuple(zip(all_text_str[0], key))

emptylist = []
textWhere = {}

for (word,index) in textset :
	if word in textWhere:
		textWhere[word].append(index)
	else:
		textWhere[word] = [index]

#print(textset)

#print(textWhere['the'],len(textWhere['the']))



#token = Tokenizer(num_words = 200)
#token.fit_on_texts(all_texts)
#print(token.word_index)









