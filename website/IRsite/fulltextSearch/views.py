from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import Word, Word_frequency
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings#PROJECT_ROOT
from django.urls import reverse
from django.utils.safestring import mark_safe
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from django.db.models import Q
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_extraction.text import CountVectorizer
import math


#from .upload_file import handle_uploaded_file

import re
import os
import string
import xml.etree.cElementTree as ET
import json
import ast

#import spacy
#from keras.preprocessing import sequence
#from keras.models import load_model

#word_dic = spacy.load('en')
word_index = {'SPACE': 19, 'ADP':1, 'ADV':2, 'AUX':3, 'CONJ':4, 'CCONJ':5, 'DET':6, 'INTJ':7, 'NUM':8, 'PART':9, 'PRON':10,
			'PROPN':11, 'PUNCT':12, 'SCONJ':13, 'SYM':14, 'VERB':15, 'NOUN':16, 'X':17, 'ADJ': 18 }

def handle_uploaded_file(f):
	p = '/Users/Solitude6060/Google_iir/Course/107_1/IR/HW1/website/IRsite/IRsite/data/'
	with open(p+'t.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def upload_file(request):
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		handle_uploaded_file(request.FILES['file'], request.FILES['filename'].name)
		return HttpResponse("OK!")
			#return HttpResponseRedirect('/success/url/')

	return render(request, 'index.html', {'form': form})


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

def apply(f, *args, **kw):
	return f(*args, **kw)


def minEditDist(sm,sn):
	m,n = len(sm),len(sn)
	D = list(map(lambda y: list(map(lambda x,y : y if x==0 else x if y==0 else 0,range(n+1),[y]*(n+1))), range(m+1)))
	for i in range(1,m+1):
		for j in range(1,n+1):
			D[i][j] = min( D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1] + apply(lambda: 0 if sm[i-1] == sn[j-1] else 2)) 
	for i in range(0,m+1):
		print(D[i])
	
	return D[m][n]

def XmlParser(path):
	tree = ET.ElementTree(file=path)
	title = ''
	text = ''
	for elem in tree.iter(tag='ArticleTitle'):
		if isinstance(elem.text, str):
			title += elem.text

	for elem in tree.iter(tag='AbstractText'):
		if isinstance(elem.text, str):
			text += elem.text

	return title, text

def jsonParser(path):
	jfile = open(path,'r',encoding='ISO-8859-1')
	jstr = jfile.read()
	jdata = json.loads(jstr)
	#jdata = str(jdata)

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
				w2s[w] = list(set(w2s[w]))
			else:
				w2s[w].append(i)
				w2s[w] = list(set(w2s[w]))
	
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
		file_name = n.replace(path,"")
		#fname.append(n)
		ftype.append(t)
		
		if t == '.xml':
			xtitle, xtext =  XmlParser(fi)
			xtext = xtext.encode('ISO-8859-1',"ignore")
			
			xti = w_to_s(xtitle)
			for w,s in xti.items():
				if not Word.objects.filter(word=w, sentence=s, style="ArticleTitle", type=t, name=file_name).exists():
					word_db_xti = Word.objects.create(word=w, sentence=s, style="ArticleTitle", type=t, name=file_name)
					word_db_xti.save()

			xte = w_to_s(xtext)
			for w,s in xte.items():
				if not Word.objects.filter(word=w, sentence=s, style="ArticleText", type=t, name=file_name).exists():
					word_db_xte = Word.objects.create(word=w, sentence=s, style="ArticleText", type=t, name=file_name)
					word_db_xte.save()
		elif t == '.json':
			jtext = jsonParser(fi)
			jtext = jtext.encode('ISO-8859-1',"ignore")
			jte = w_to_s(jtext)

			for w,s in jte.items():
				if not Word.objects.filter(word=w, sentence=s, style="Text", type=t, name=file_name).exists():
					word_db_jte = Word.objects.create(word=w, sentence=s, style="Text", type=t, name=file_name)
					word_db_jte.save()

def tfidf(art_num):
	text_list = []
	data_path = settings.PROJECT_ROOT+"/data/TFIDF/"
	for f in os.listdir(data_path):
		#print(f)
		fname, ftype = os.path.splitext(f)
		if ftype == ".txt":
			file_path = data_path+f
			text_file = open(file_path, "r")
			text = text_file.read()
			text_list.append(text)

	vectorizer=CountVectorizer()
	transformer=TfidfTransformer()
	tfidf=transformer.fit_transform(vectorizer.fit_transform(text_list))
	word=vectorizer.get_feature_names()
	weight=tfidf.toarray()

	article_list = []
	word_dict = {}
	word_count = 0
	word_total_length = 0

	new_article_list = []
	new_word_dict = {}

	#print(len(word))
	for w in word:
		word_total_length += len(w)
	avg_word_len = word_total_length/len(word)

	for i in range(len(weight)):
		#print("-------輸出第",i+1,"類文本tf-idf權重------")
			for j in range(len(word)):
				word_dict.update({word[j]: weight[i][j]})
				if weight[i][j] != 0:
					new_word_dict.update({word[j]: math.log(weight[i][j]**-1)})
				else:
					new_word_dict.update({word[j]: weight[i][j]})
			article_list.append(word_dict)
			new_article_list.append(new_word_dict)
			word_dict = {}
			new_word_dict = {}
	
	#print(article_list[0])
	count = 1
	return_list = []
	return_frq_list = []
	for art in article_list:
		#print("-------輸出第",count,"類文本前10個tf-idf權重------")
		sort_word = [(k, art[k]) for k in sorted(art, key=art.get, reverse=True)]
		if count == art_num:
			return_list = sort_word
		#print(sort_word[0][0])
		#for key, value in sort_word[0:10]:
			#print(key, value)
		#print("###############################################")
		#print("-------改良版第",count,"類文本前10個tf-idf權重------")
		new_art = new_article_list[count-1]
		new_sort_word = [(k, new_art[k]) for k in sorted(new_art, key=new_art.get, reverse=True)]
		if count == art_num:
			return_frq_list = new_sort_word
		#for new_key, new_value in new_sort_word[0:10]:
			#print(new_key, new_value)
		#print("###############################################")
		count += 1

	return text_list, return_list, return_frq_list

def index(request):
	if 'tfidf' in request.POST:
		print("TFIDF")
		article_num = request.POST.get('input')
		if article_num[0] != "#":
			article_num = "#20"
		if article_num[0] == "#":
			art_num = int(article_num.replace("#",""))
			print(art_num)
			article_list, word_list, shannon_list = tfidf(art_num)
			w_name_list = []
			w_frq_list = []
			s_name_list = []
			s_frq_list = []
			for key, value in word_list[0:20]:
				w_name_list.append(key)
				w_frq_list.append(value)
			for key, value in shannon_list[0:20]:
				s_name_list.append(key)
				s_frq_list.append(value)
			#print(w_name_list)
			#print(article_num)
			statistic_list = zip(w_name_list, w_frq_list, s_name_list, s_frq_list)
			title_list = []
			title_list.append(article_num)
			content_list = []
			content_list.append(article_list[art_num-1])
			return_list = zip(title_list, content_list)
			return render(request, 'fulltextSearch/index.html', locals())
	if 'upload' in request.POST:
		tttt = "upload success!"
		dirpath = settings.PROJECT_ROOT+"/data/"
		fname = request.FILES['myfile'].name
		filepath = dirpath+fname
		with open(filepath, 'wb+') as destination:
			for chunk in request.FILES['myfile'].chunks():
				destination.write(chunk)
		destination.close()
	if 'parse' in request.POST:
		read_all()

	if 'search' in request.POST:
		target = request.POST.get('input')
		path = settings.PROJECT_ROOT+"/data/"
		file_list = []
		file = []
		file_notemp = []
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
			splname, spltext = os.path.splitext(f)
			if spltext == '.xml' or spltext == '.json':
	 			file_notemp.append(f)

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
		statistic_list = zip(file_notemp, ch, wo, se)
		'''
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
		style_list = []
		for i in sen_obj:
			sen_list = ast.literal_eval(i.sentence)
			name_list.append(i.name)
			type_list.append(i.type)
			tupLi_tu += (i.name,)
			tupLi_tu += (i.type,)  
			if i.type == '.xml':
				xti, xte = XmlParser(path+i.name+i.type)
				xte = xte.encode('ISO-8859-1',"ignore")
				sp_list = split_s(xte)
				for i in sen_list:
					
					####################
					s_w_sp = sp_list[i].split(target)
					for i in range(len(s_w_sp)):
						tup += (s_w_sp[i],)
						if i != len(s_w_sp)-1:
							tup += (target,)
					tupLi.append(tup)
					####################
					
					tt = ""
					if str(sp_list[i]) not in tupLi:
						s_w_sp = sp_list[i].split(target)
						for i in range(len(s_w_sp)):
							tt += s_w_sp[i]
							if i != len(s_w_sp)-1:
								tt+= "<span style='background-color: #FFFF00'>"+target+"</span>"
						tupLi.append(mark_safe(tt))
			#elif i.type == '.DS_Store':
				#a = 'a'
			elif i.type == '.json':
				jt = jsonParser(path+i.name+i.type)
				jt = jt.encode('ISO-8859-1',"ignore")
				sp_list = split_s(jt)
				for i in sen_list:
					
					################
					s_w_sp = sp_list[i].split(target)
					for i in range(len(s_w_sp)):
						tup += (s_w_sp[i],)
						if i != len(s_w_sp)-1:
							tup += (target,)
					tupLi.append(tup)
					
					##################
					
					tt = ""
					if str(sp_list[i]) not in tupLi:
						s_w_sp = sp_list[i].split(target)
						for i in range(len(s_w_sp)):
							tt += s_w_sp[i]
							if i != len(s_w_sp)-1:
								tt+= "<span style='background-color: #FFFF00'>"+target+"</span>"
						tupLi.append(make_safe(tt))

			tupLi_tu += (tupLi,)
			tupList.append(tupLi_tu)
			tupLi_tu = ()
			tupLi = []
			tup = ()
			'''
	if 'search_all' in request.POST:
		target = request.POST.get('input')
		path = settings.PROJECT_ROOT+"/data/"
		key = request.POST.get('input')
		returnText_list = []
		return_list = {}
		minDis = 1000000000
		minWord = ""
		stemWord_list = []

		word_obj = Word.objects.filter(word__contains=target)
		if not word_obj.exists():
			print("no match")
			all_word_obj = Word.objects.all()
			for word in all_word_obj:
				tempDis = minEditDist(target, word.word)
				if tempDis < minDis:
					minDis = tempDis
					minWord = word.word
			target = minWord
			print("change to ",target)
			for word in all_word_obj:
				if PorterStemmer().stem(word.word.lower()) == PorterStemmer().stem(target.lower()):
					if word.word not in stemWord_list:
						stemWord_list.append(word.word)
						print(word.word)
			word_obj = Word.objects.filter(word=target)
			word_tuple_list = []
			word_in_file = []
			word_in_sentence = []
			word_type_list = []
			word_style_list = []
			word_all_list = []
			for word_item in word_obj:
				which_style = word_item.style
				word_style_list.append(which_style)
				which_art = word_item.name
				which_type = word_item.type
				word_type_list.append(which_type)
				which_sentence = word_item.sentence
				if which_art+which_type+which_style not in word_all_list:
					word_in_file.append(which_art+which_type)
					word_all_list.append(which_art+which_type+which_style)
				word_in_sentence.append(which_sentence)
				word_tuple_list.append((which_art, which_type, which_style, which_sentence))
		else:
			print("match")
			all_word_obj = Word.objects.all()
			for word in all_word_obj:
				if PorterStemmer().stem(word.word.lower()) == PorterStemmer().stem(target.lower()):
					if word.word not in stemWord_list:
						stemWord_list.append(word.word)
						print(word.word)

			word_obj = Word.objects.filter(word__in=stemWord_list)
			word_tuple_list = []
			word_in_file = []
			word_in_sentence = []
			word_type_list = []
			word_style_list = []
			word_all_list = []
			for word_item in word_obj:
				which_style = word_item.style
				word_style_list.append(which_style)
				which_art = word_item.name
				which_type = word_item.type
				word_type_list.append(which_type)
				which_sentence = word_item.sentence
				if which_art+which_type+which_style not in word_all_list:
					word_in_file.append(which_art+which_type)
					word_all_list.append(which_art+which_type+which_style)
				word_in_sentence.append(which_sentence)
				word_tuple_list.append((which_art, which_type, which_style, which_sentence))
		
		#word_all_file = list(set(word_all_file))
		for i in range(len(word_in_file)):
			print("split", target)
			returnText = ""
			file = word_in_file[i]
			t = word_type_list[i]
			if t == '.xml':
				w_in_title, w_in_text = XmlParser(path+file)
				if word_style_list[i] == 'ArticleTitle':
					atitle_text = w_in_title.split(target)
					for i in range(len(atitle_text)):
						returnText += atitle_text[i]
						if i != len(atitle_text)-1:
							returnText+= "<span style='background-color: #FFFF00'>"+target+"</span>"
					returnText_list.append(mark_safe(returnText))
				elif word_style_list[i] == 'ArticleText':
					atext_text = w_in_text.split(target)
					for i in range(len(atext_text)):
						returnText += atext_text[i]
						if i != len(atext_text)-1:
							returnText+= "<span style='background-color: #FFFF00'>"+target+"</span>"
					returnText_list.append(mark_safe(returnText))
			elif t == '.json':
				w_in_json = jsonParser(path+file)
				json_text = w_in_json.split(target)
				for i in range(len(json_text)):
					returnText += json_text[i]
					if i != len(json_text)-1:
						returnText += "<span style='background-color: #FFFF00'>"+target+"</span>"
				returnText_list.append(mark_safe(returnText))
		
		return_list = zip(word_in_file, returnText_list)
	return render(request, 'fulltextSearch/index.html', locals())

def upload(request):
	if 'upload' in request.POST:
		tttt = "upload success!"
		dirpath = settings.PROJECT_ROOT+"/data/"
		fname = request.FILES['myfile'].name
		filepath = dirpath+fname
		with open(filepath, 'wb+') as destination:
			for chunk in request.FILES['myfile'].chunks():
				destination.write(chunk)
		destination.close()
		#return render_to_response('fulltextSearch/index.html', locals())
		return HttpResponseRedirect('index',locals())
	
	return render(request, 'fulltextSearch/upload.html', locals())

def Zipf_xml(request):
	subtitle = "Pubmed"
	wordCount_dist = {}
	count = 0
	all_xml_query = Word_frequency.objects.filter(file_type='.xml')
	chart_list = []
	for text in all_xml_query:
		wordCount_dist[text.word] = text.frequency
	
	wordCount_dist = sorted(wordCount_dist.items(), key=lambda d: d[1], reverse=True)
	
	for word in wordCount_dist:
		count += 1
		chart_list.append((count, word[1], str(count), word[0]))
	
	chart_list = chart_list[0:150]
	
	return render(request, 'fulltextSearch/Zipf.html', locals())

def Zipf_json(request):
	subtitle = "Twitter"
	wordCount_dist = {}
	count = 0
	all_json_query = Word_frequency.objects.filter(file_type='.json')
	chart_list = []
	for text in all_json_query:
		wordCount_dist[text.word] = text.frequency
	
	wordCount_dist = sorted(wordCount_dist.items(), key=lambda d: d[1], reverse=True)
	
	for word in wordCount_dist:
		count += 1
		chart_list.append((count, word[1], str(count), word[0]))
	
	chart_list = chart_list[0:150]
	
	return render(request, 'fulltextSearch/Zipf.html', locals())

def chart(request):
	wordCount_dist = {}
	count = 0
	xml_list = []
	json_list = []
	chart_list = []
	count = 0
	all_json_query = Word_frequency.objects.filter(file_type='.json')
	
	for text in all_json_query:
		wordCount_dist[text.word] = text.frequency
	
	wordCount_dist = sorted(wordCount_dist.items(), key=lambda d: d[1], reverse=True)
	
	for word in wordCount_dist:
		count += 1
		chart_list.append((count, word[1]))
	
	json_list = chart_list
	wordCount_dist = {}
	chart_list = []
	count = 0

	all_xml_query = Word_frequency.objects.filter(file_type='.xml')
	for text in all_xml_query:
		wordCount_dist[text.word] = text.frequency
	
	wordCount_dist = sorted(wordCount_dist.items(), key=lambda d: d[1], reverse=True)
	
	for word in wordCount_dist:
		count += 1
		chart_list.append((count, word[1]))

	xml_list = chart_list[0:600]

	return render(request, 'fulltextSearch/chart.html', locals())