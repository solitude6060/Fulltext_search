from django.shortcuts import render
from .models import Word
import re
import os
import string
import xml.etree.cElementTree as ET
import json
import ast
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings#PROJECT_ROOT
#from keras.preprocessing import sequence
import spacy
#from keras.models import load_model
word_dic = spacy.load('en')
word_index = {'SPACE': 19, 'ADP':1, 'ADV':2, 'AUX':3, 'CONJ':4, 'CCONJ':5, 'DET':6, 'INTJ':7, 'NUM':8, 'PART':9, 'PRON':10,
              'PROPN':11, 'PUNCT':12, 'SCONJ':13, 'SYM':14, 'VERB':15, 'NOUN':16, 'X':17, 'ADJ': 18 }

def change(text):
    result = []
    doc = word_dic(text)
    for i in range(len(doc)):
        result += [doc[i].pos_]
    return result
'''
def predict(xlist):
	model = load_model(settings.PROJECT_ROOT+'/data/eos_model.h5')
	num_x_train = []
	all_text = []

	for text in xlist:
		for word in text:
			all_text.append(word_index[str(word)])

		num_x_train.append(all_text)
		all_text = []

	input_x_train = sequence.pad_sequences(num_x_train , maxlen=50)
    
	predict = model.predict_classes(input_x_train)
	count = 0
	for i in predict:
		if i[0] == 1:
			count += 1
	return int(count*0.9)
'''
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
	jfile = open(path,'r',encoding='ISO-8859-1')
	jstr = jfile.read()

	jdata = json.loads(jstr)

	jtext = ''
	for text in jdata:
		jtext += text['Text']

	return jtext

def countChar(t):
	return len(t)

def countWord(tList):
	return len(tList)

def tokenize(text):
	text = str(text)
	SPLIT_RE = re.compile(r'[^a-zA-Z0-9]')
	return SPLIT_RE.split(text)

def split_s(s):
	s = str(s)
	s_list = []
	s_list = s.split('.')
	return s_list

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

def read_all():
	file_list =[]
	path = settings.PROJECT_ROOT+"/data/"
	fname = []
	ftype = []
	xtitle = ""
	xtext = ""
	jtext = ""

	xti = []
	xte = []
	jte = []

	for f in os.listdir(path):
		file_list +=[path+f]
		fname.append(f)
	for fi in file_list:
		#fi = str(fi)
		n, t = os.path.splitext(fi)
		#fname.append(n)
		ftype.append(t)
		
		if t == '.xml':
			xtitle, xtext =  XmlParser(fi)
			xtext = xtext.encode('ISO-8859-1',"ignore")
			
			xti = w_to_s(xtitle)
			for w,s in xti.items():
				if not Word.objects.filter(word=w, sentence=s, style="ArticleTitle", type=t, name=n).exists():
					word_db_xti = Word.objects.create(word=w, sentence=s, style="ArticleTitle", type=t, name=n)
					word_db_xti.save()

			xte = w_to_s(xtext)
			for w,s in xte.items():
				if not Word.objects.filter(word=w, sentence=s, style="ArticleText", type=t, name=n).exists():
					word_db_xte = Word.objects.create(word=w, sentence=s, style="ArticleText", type=t, name=n)
					word_db_xte.save()
		elif t == '.json':
			jtext = jsonParser(fi)
			jtext = jtext.encode('ISO-8859-1',"ignore")
			jte = w_to_s(jtext)

			for w,s in jte.items():
				if not Word.objects.filter(word=w, sentence=s, style="Text", type=t, name=n).exists():
					word_db_jte = Word.objects.create(word=w, sentence=s, style="Text", type=t, name=n)
					word_db_jte.save()


def index(request):
	if 'parse' in request.POST:
		read_all()
	if 'search' in request.POST:
		target = request.POST.get('input')
		path = settings.PROJECT_ROOT+"/data/"
		file_list = []
		file = []
		fname = []
		ftype = []
		xtitle = ""
		xtext = ""
		jtext = ""

		xti = []
		xte = []
		jte = []
		ch = []
		wo = []
		se = []
		se_m = []
		for f in os.listdir(path):
			file += [f]

		for f in os.listdir(path):
			file_list +=[path+f]
			fname.append(f)

		for fi in file_list:
			n, t = os.path.splitext(fi)
			ftype.append(t)

			if t == '.xml':
				xtitle, xtext =  XmlParser(fi)
				xtext = xtext.encode('ISO-8859-1',"ignore")
				ch.append(countChar(xtitle)+countChar(xtext))
				wo.append(countWord(tokenize(xtitle))+countWord(tokenize(xtext)))
				se.append(int(countWord(split_s(xtitle))+countWord(split_s(xtext))*0.9))
				#se_m.append(predict(split_s(xtitle))+predict(split_s(xtext)))
			elif t == '.json':
				jtext = jsonParser(fi)
				jtext = jtext.encode('ISO-8859-1',"ignore")
				ch.append(countChar(jtext))
				wo.append(countWord(tokenize(jtext)))
				se.append(int(countWord(split_s(jtext))*0.9))
				#se_m.append(predict(split_s(jtext)))

		#n, ty, front, word, back in tupList
		#tupList = [("n","ty",[("s","ss","sss"),("s","ss","sss"),("s","ss","sss")])]
		sen_obj = Word.objects.filter(word=target)
		#sen_obj_get = Word.objects.get(word=target)
		#sen_list = ast.literal_eval(sen_obj.values('sentence'))
		tupList = []
		tupLi_tu = ()
		tupLi = []
		tup = ()
		name_list = []
		type_list = []
		for i in sen_obj:
			sen_list = ast.literal_eval(i.sentence)
			name_list.append(i.name)
			type_list.append(i.type)
			tupLi_tu += (i.name,)
			tupLi_tu += (i.type,)  
			if i.type == '.xml':
				xti, xte = XmlParser(i.name+i.type)
				xte = xte.encode('ISO-8859-1',"ignore")
				sp_list = split_s(xte)
				for i in sen_list:
					'''
					s_w_sp = sp_list[i].split(target)
					for i in range(len(s_w_sp)):
						tup += (s_w_sp[i],)
						if i != len(s_w_sp)-1:
							tup += (target,)
					tupLi.append(tup)
					'''
					tt = ""
					if str(sp_list[i]) not in tupLi:
						s_w_sp = sp_list[i].split(target)
						for i in range(len(s_w_sp)):
							tt += s_w_sp[i]
							if i != len(s_w_sp)-1:
								tt+= "###"+target+"###"
						tupLi.append(tt)
			#elif i.type == '.DS_Store':
				#a = 'a'
			elif i.type == '.json':
				jt = jsonParser(i.name+i.type)
				jt = jt.encode('ISO-8859-1',"ignore")
				sp_list = split_s(jt)
				for i in sen_list:
					'''
					s_w_sp = sp_list[i].split(target)
					for i in range(len(s_w_sp)):
						tup += (s_w_sp[i],)
						if i != len(s_w_sp)-1:
							tup += (target,)
					tupLi.append(tup)
					<!--{% for front, word, back in sen %}
        <div>Text : {{front}}<font color="blue"> {{word}} </font>{{back}}</div><br>
        {% endfor %}
        -->
					'''
					tt = ""
					if str(sp_list[i]) not in tupLi:
						s_w_sp = sp_list[i].split(target)
						for i in range(len(s_w_sp)):
							tt += s_w_sp[i]
							if i != len(s_w_sp)-1:
								tt+= "###"+target+"###"
						tupLi.append(tt)

			tupLi_tu += (tupLi,)
			tupList.append(tupLi_tu)
			tupLi_tu = ()
			tupLi = []
			tup = ()


	return render(request, 'fulltextSearch/index.html', locals())








