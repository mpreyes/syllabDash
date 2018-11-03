from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from docx.api import Document
import datetime #get timestamp as key for cache: datetime.datetime.now

import os

# Create your views here.

#helper functions

def handle_uploaded_file(file, filename):
    if not os.path.exists('uploads/'):
        print("made upload folder")
        os.mkdir('uploads/')

    with open('uploads/' + filename, 'wb+') as destination:
        print("dest " + str(destination))
        for chunk in file.chunks():
            destination.write(chunk)

    print("deleting files in upload folder")
    #delete_uploads() #uncomment me to see upload of files


def delete_uploads():
    folder = 'uploads/'
    for f in os.listdir(folder):
        print("file: " + str(f))
        file_path = os.path.join(folder,f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)



#views

def index(request):
    return render(request, 'syllab_dash/index.html')

def about(request):
    return render(request, 'syllab_dash/about.html')

def file_upload(request):
    cache_key = 'user_boo' # needs to be unique
    cache_time = 7200 # time in seconds for cache to be valid, 2 hours
    files_parsed = []
    
    if request.method == 'POST':
        for f in request.FILES.getlist('file'):
            filename = f.name
            print(filename)
            #handle_uploaded_file(f, filename)
            files_parsed.append(f)
        cache.set(cache_key,files_parsed,cache_time)
        return render(request, 'syllab_dash/list_assignments.html') #TODO: create a fail page
        #return list_assignments(render,parsed_files_list = files_parsed)
    return render(request, 'syllab_dash/list_assignments.html') #TODO: create a fail page


def show_file_contents(request):
    
    return render(request, 'syllab_dash/show_file_contents.html')



def list_assignments(request):
    data = cache.get("user_boo")
    print(data)
    parsed_files = []
    for i in data:
        with i.open() as f:
            document = Document(f) #currently only supports docx files
            for p in document.paragraphs: #maybe split up file detection into separate functions
                print(p.text)  # parsePdf(p), parseWord(p), etc ?
                parsed_files.append(p.text)
                #break
        

        #print(data)
    return render(request, 'syllab_dash/list_assignments.html',{"cached_files_list": cache.get("user_boo"), "parsed_files": parsed_files})


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')
