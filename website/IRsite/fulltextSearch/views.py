from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import Word
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings#PROJECT_ROOT
from django.urls import reverse
from django.utils.safestring import mark_safe

#from .upload_file import handle_uploaded_file

import re
import os
import string
import xml.etree.cElementTree as ET
import json
import ast

import spacy
#from keras.preprocessing import sequence
#from keras.models import load_model

word_dic = spacy.load('en')
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


def index(request):
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
		
		#word_all_file = list(set(word_all_file))
		for i in range(len(word_in_file)):
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







