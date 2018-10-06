import re
import os
import string
import xml.etree.cElementTree as ET
import json

data_path = 'data/pubmed_result_brain.xml'
json_path = 'data/tweets.json'

def XmlParser(path):
	tree = ET.ElementTree(file=path)
	title = ''
	text = ''

	for elem in tree.iter(tag='ArticleTitle'):
		title += elem.text

	for elem in tree.iter(tag='AbstractText'):
		text += elem.text

	return title, text

def jsonParser(path):
	jfile = open(path,'r')
	jstr = jfile.read()

	jdata = json.loads(str(jstr))

	jtext = ''
	for text in jdata:
		jtext += text['Text']

	return jtext

def countChar(t):
	return len(t)

def countWord(tList):
	return len(tList)

def tokenize(text):
	SPLIT_RE = re.compile(r'[^a-zA-Z0-9]')
	return SPLIT_RE.split(text)

def split_s(s):
	s_list = []
	s_list = s.split('.')
	return s_list


#t = "keep in mind that this matches a sequence of characters, not necessarily a whole word - for Example,"
#st = "example"
#print(t.lower().find(st))

addpath = 'data/'
name_str = 'pubmed_result_brain.xml'
fname, ftype = os.path.splitext(name_str)
print(ftype)
#if xml >> title, text
style = 'ArticleTitle'
xtitle, xtext = XmlParser(data_path)
xtext = xtext.encode('utf-8')

print(xtitle)
print(split_s(xtitle))
def w_to_s(t):
	spList = split_s(t)
	tList = []
	w2s = {}
	for i in range(len(spList)):
		tList = tokenize(spList[i])
		for w in tList:
			if w not in w2s.keys():
				w2s[w] = [i]
			else:
				w2s[w].append(i)
	#print(w2s)
	return(w2s)

#print(w_to_s(xtext))

print(jsonParser('data/tweets.json'))


