import re
import os
import string
import xml.etree.cElementTree as ET

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


