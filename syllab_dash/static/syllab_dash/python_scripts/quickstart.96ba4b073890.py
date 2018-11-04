from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time


def insertEvents():
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

testEvent = {
  'summary': 'This is a test event summary.',
  'start': {
    'dateTime': '2018-11-02T21:50:00',
    'timeZone': time.tzname[time.daylight]
  },
  'end': {
    'dateTime': '2018-11-02T22:00:00',
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
    'dateTime': '2019-11-09T21:50:00',
    'timeZone': time.tzname[time.daylight]
  },
  'end': {
    'dateTime': '2018-11-09T21:50:00',
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



"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


event = service.events().insert(calendarId='primary', body=testEvent).execute()
event2 = service.events().insert(calendarId='primary', body=testEvent2).execute()

if not event:
    print("Error inserting event 1")
if not event2:
    print("Error inserting event 2")
