from django.shortcuts import render 
# Create your views here.



def index(request):
      return render(request, 'syllab_dash/index.html')

def about(request):
    return render(request, 'syllab_dash/about.html')

def file_upload(request):
      return render(request, 'syllab_dash/file_upload.html')

def show_file_contents(request):
    return render(request, 'syllab_dash/show_file_contents.html')


def list_assignments(request):
    return render(request, 'syllab_dash/list_assignments.html')


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')

