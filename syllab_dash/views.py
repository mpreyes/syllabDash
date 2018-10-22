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
        handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
        return render(request, 'syllab_dash/list_assignments.html') #on upload
    return render(request, 'syllab_dash/file_upload.html') #on fail


# class file_upload(FormView):
#     template_name = 'file_upload.html'
#     form_class = UploadForm
#     success_url = '/list_assignments/'

#     def form_valid(self, form):
#         for each in form.cleaned_data['attachments']:
#             Attachment.objects.create(file=each)
#         return super(file_upload, self).form_valid(form)



# class file_upload(FormView):
#     form_class = FileFieldForm
#     template_name = 'file_upload.html'  # Replace with your template.
#     success_url = '/list_assignments.html'  # Replace with your URL or reverse().

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 print("got files ")
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)



def show_file_contents(request):
    return render(request, 'syllab_dash/show_file_contents.html')


def list_assignments(request):
    return render(request, 'syllab_dash/list_assignments.html')


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')
