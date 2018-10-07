import os

#PROJECT_ROOT
from django.conf import settings

def handle_uploaded_file(f, path):
    dirpath = settings.PROJECT_ROOT+"/data/test"
    p = '/Users/Solitude6060/Google_iir/Course/107_1/IR/HW1/website/IRsite/IRsite/data'
    fpath = dirpath + path
    with open(p, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            #destination.close()