from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from docx.api import Document
import datetime #get timestamp as key for cache: datetime.datetime.now
from itertools import islice
import os

# Create your views here.

#helper functions

# def handle_uploaded_file(file, filename):
#     if not os.path.exists('uploads/'):
#         print("made upload folder")
#         os.mkdir('uploads/')

#     with open('uploads/' + filename, 'wb+') as destination:
#         print("dest " + str(destination))
#         for chunk in file.chunks():
#             destination.write(chunk)

#     print("deleting files in upload folder")
#     #delete_uploads() #uncomment me to see upload of files


# def delete_uploads():
#     folder = 'uploads/'
#     for f in os.listdir(folder):
#         print("file: " + str(f))
#         file_path = os.path.join(folder,f)
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print(e)




def parse_tables(f,filename): # returns tables in document
    print("parse files")
    document_tables = []
    document = Document(f) #currently only supports docx files
    for t in document.tables: #m
        print("__ table __ ")
        print(t)
        document_tables.append(t)
    return document_tables
            

#views

def index(request):
    return render(request, 'syllab_dash/index.html')

def about(request):
    return render(request, 'syllab_dash/about.html')

def file_upload(request):
    cache_key = 'user_boo' # needs to be unique
    cache_time = 7200 # time in seconds for cache to be valid, 2 hours
    files_parsed = [] #files parsed
    parsed_tables = [] #extracting tables from document
    candidate_tables = [] # tables that contain "date", or "week", or 
    parsed_assignments = []
    if request.method == 'POST':
        for f in request.FILES.getlist('file'):
            filename = f.name
            print(filename)
            parsed_tables = parse_tables(f,filename)
            candidate_tables = get_tables_cont_dates(parsed_tables)
            parsed_assignments =  parse_assignments(candidate_tables)
            files_parsed.append(f)
        cache.set(cache_key,files_parsed,cache_time)
        return render(request, 'syllab_dash/list_assignments.html') #TODO: create a fail page
        #return list_assignments(render,parsed_files_list = files_parsed)
    return render(request, 'syllab_dash/file_upload.html') #TODO: create a fail page



def show_file_contents(request):

    return render(request, 'syllab_dash/show_file_contents.html')

# def get_table_index(tables):
#     tableList = []
#     for table in tables: 
#         for i, cell in table.rows[0]:
#             if 'date' in cell.text:
#                 tableList.append(i)

# def parse_table(index);
#     table = tables[index]


def get_tables_cont_dates(tables): #parse tables, return those containing "date", "week"
    candidate_tables = []
    print("parse tables, return those containing 'date', 'week'")
    for i in tables:
        for row in i.rows:
            for cell in row.cells:
                if("date" in cell.text.lower() or "week" in cell.text.lower()):
                    candidate_tables.append(i)
                    break
    return candidate_tables

def parse_assignments(candidate_tables):
    data = []
    for c in candidate_tables:
        print(c)
        for i, row in enumerate(c.rows):
            
            text = (cell.text for cell in row.cells)
            # Establish the mapping based on the first row
            # headers; these will become the keys of our dictionary
            if i == 0:
                print(text)
                keys = tuple(text)
                #print(keys)
                continue
            # Construct a dictionary for this row, mapping
            # keys to values for this row
            row_data = dict(zip(keys, text))
            data.append(row_data)
    # print(data)
    lower_data = []
    for i in data:
        lower_dict = dict((k.lower(), v.strip('\n')) for k, v in i.items())
        lower_data.append(lower_dict)
        print(lower_dict)
    # print("after removal")
    # print(lower_data)
    return lower_data

        
def list_assignments(request):
    data = cache.get("user_boo")
    print(data)
    parsed_files = []
    # for i in data:
    #     with i.open() as f:
    #         document = Document(f) #currently only supports docx files
    #         for p in document.paragraphs: #maybe split up file detection into separate functions
    #             #print(p.text)  # parsePdf(p), parseWord(p), etc ?
    #             parsed_files.append(p.text)
    #             #break
        

        #print(data)
    return render(request, 'syllab_dash/list_assignments.html',{"cached_files_list": cache.get("user_boo"), "parsed_files": parsed_files})


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')
