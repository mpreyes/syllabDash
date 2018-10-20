from django.shortcuts import render 
from django.http import HttpResponseRedirect
from django.conf import settings
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
    if request.method == 'POST':
        for f in request.FILES.getlist('file'):
            filename = f.name
            print(filename)
            handle_uploaded_file(f, filename)
        return render(request, 'syllab_dash/list_assignments.html') #on upload
    return render(request, 'syllab_dash/file_upload.html') #TODO: create a fail page


def show_file_contents(request):
    return render(request, 'syllab_dash/show_file_contents.html')


def list_assignments(request):
    return render(request, 'syllab_dash/list_assignments.html')


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')

