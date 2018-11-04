from __future__ import print_function

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from docx.api import Document

from dateutil import parser
from itertools import islice
import os  #get timestamp as key for cache: datetime.datetime.now
import rfc3339      # for date object -> date string
from datetime import * #get timestamp as key for cache: datetime.datetime.now

# imports for google api
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
import time

# Create your views here.

def file_tables(f,filename): # returns tables in document
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
    #insertEvents(request)
    return render(request, 'syllab_dash/index.html')

def about(request):
    return render(request, 'syllab_dash/about.html')

def file_upload(request):
    cache_key = 'user_boo' # needs to be unique
    cache_time = 7200 # time in seconds for cache to be valid, 2 hours
    files_parsed = [] #files parsed
    parsed_tables = [] #extracting tables from document
    candidate_tables = [] # tables that contain "date", or "week", or
    parsed_table_data = [] #each row is dictionary, headers mapped to column data
    parsed_assignments = [] #only event data pulled from parsed_table_data
    if request.method == 'POST':
        for f in request.FILES.getlist('file'):
            filename = f.name
            print(filename)
            parsed_tables = file_tables(f,filename)
            candidate_tables = get_tables_cont_dates(parsed_tables)
            parsed_table_data =  parse_table_data(candidate_tables)
            display_table_files = (filename, parsed_table_data)
            parsed_assignments = parse_assignments(parsed_table_data)
            files_parsed.append(parsed_assignments)
        cache.set(cache_key,files_parsed,cache_time)
        return redirect('list_assignments') #TODO: create a fail page
        #return list_assignments(render,parsed_files_list = files_parsed)
    return render(request, 'syllab_dash/file_upload.html') #TODO: create a fail page


def show_file_contents(request):

    return render(request, 'syllab_dash/show_file_contents.html')

    return render(request, 'syllab_dash/show_file_contents.html')


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

def parse_table_data(candidate_tables):
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
                continue
            # Construct a dictionary for this row, mapping
            # keys to values for this row
            row_data = dict(zip(keys, text))
            data.append(row_data)

    lower_data = []
    for i in data:
        lower_dict = dict((k.lower(), v.strip('\n')) for k, v in i.items())
        lower_data.append(lower_dict)
    return lower_data


def parse_assignments(table_data):
    assignments = []
    for row in table_data:
        date = parse_date(row["date"])
        timezone = datetime.utcnow().astimezone().tzinfo
        event = {
            'summary': 'TESTING',
            'location': '',
            'description': '',
            'start': {
                'dateTime': date,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': date,
                'timeZone': timezone,
            },
            'recurrence': [],
            'attendees': [],
            'reminders': {
                'useDefault': False,
                'overrides': [
                  {'method': 'popup', 'minutes': 24 * 60 * 7},
                  {'method': 'popup', 'minutes': 24 * 60},
                ],
            },
            }
        assignments.append(event)
        print(event['start']['dateTime'])
    return assignments


def parse_date(date):
    date = parser.parse(date, fuzzy=True)
    if date.year:
        datetime_object = rfc3339.rfc3339(date) #change to rfc3339 format
    else:
        datetime_object = rfc3339.rfc3339(date) #change to rfc3339 format


def list_assignments(request):
    data = cache.get("user_boo")
    print(data)

    # for i in data:
    #     filename, table = i
    #     print(filename)
    #     print(table)
    # for i in data:
    #     with i.open() as f:
    #         document = Document(f) #currently only supports docx files
    #         for p in document.paragraphs: #maybe split up file detection into separate functions
    #             #print(p.text)  # parsePdf(p), parseWord(p), etc ?
    #             parsed_files.append(p.text)
    #             #break


        #print(data)
    return render(request, 'syllab_dash/list_assignments.html',{"file_data": data })


def finished_upload(request):
    return render(request, 'syllab_dash/finished_upload.html')

"""
def insertEvents(request):
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    testEvent = {
      'summary': 'This is a test event summary.',
      'start': {
        'dateTime': '2018-11-02T22:10:00',
        'timeZone': time.tzname[time.daylight]
      },
      'end': {
        'dateTime': '2018-11-02T23:00:00',
        'timeZone': time.tzname[time.daylight]
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'days': 7},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }


    testEvent2 = {
      'summary': 'This is a test event summary.',
      'start': {
        'dateTime': '2019-11-09T22:10:00',
        'timeZone': time.tzname[time.daylight]
      },
      'end': {
        'dateTime': '2018-11-09T23:00:00',
        'timeZone': time.tzname[time.daylight]
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'days': 7},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }



    """
    # Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    # """
    #
    # flow = OAuth2WebServerFlow(
    #     client_id='319052537199-fndghhjj6akqht9gmooe818k5b00jnp6.apps.googleusercontent.com',
    #     client_secret='6yYGMakT8_lBX4mTiUr7yfb5',
    #     scope='https://www.googleapis.com/auth/calendar',
    #     user_agent='Syllab-Dash',
    # )
    # storage = Storage('calendar.dat')
    # credentials = storage.get()
    #
    # code = request.GET.get('code')
    # if credentials is None or credentials.invalid == True:
    #     oauth_callback = 'index.html'
    #     flow.redirect_uri = oauth_callback
    #     flow.step1_get_authorize_url()
    #     credential = flow.step2_exchange(code, http=None)
    #     storage.put(credential)
    #     credential.set_store(storage)
    # http = httplib2.Http()
    # http = credentials.authorize(http)
    #
    # service = build(serviceName='calendar', version='v3', http=http,
    #                 developerKey='AIzaSyBP60OCOPNIXTWVHG-XmorCqvBsjzThdFQ')
    #
    # event = service.events().insert(calendarId='primary', body=testEvent).execute()
    # event2 = service.events().insert(calendarId='primary', body=testEvent2).execute()
    #
    # if not event:
    #     print("Error with adding event 1")
    # else:
    #     print("Added event 1 successfully... maybe.")
    # if not event2:
    #     print("Error with adding event 2")
    # else:
    #     print("Added event 2 successfully... maybe.")
