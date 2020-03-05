from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import subprocess as sp
import time

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    calendarList = service.calendarList().list().execute()

    # create an array for later use of calendarId
    calendarIds = []
    # populate calendarIds from the API
    for calendar in calendarList['items']:
        calendarIds.append(calendar['id'])

    # print the list of available calendarss
    it = 1
    sys.stdout.flush()
    for calendar in calendarList['items']:
        print(str(it) + ". " + calendar['summary'])
        it += 1
    userInput = 0

    print("Choose a calendar to show events from it")
    # let the user choose the calendar
    while True:
        try:
            userInput = int(input())
        except ValueError:
            userInput = 0
        finally:
            if not (1 <= userInput <= it - 1):
                print("The input must be a number!! between 1 and ", it - 1)
            if userInput != 0 and 1 <= userInput <= it - 1:
                break

    # add time
    #different time format for different things
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    tomorrow = tomorrow.isoformat() + 'Z'

    # get the events and print them
    first10Events = service.events().list(calendarId=calendarIds[userInput - 1], timeMin=now,
                                   maxResults=10, singleEvents=True,
                                   orderBy='startTime').execute()

    #the problem is that today and tomorrow are not of time type
    weeklyEvents = service.events().list(calendarId=calendarIds[userInput - 1],
                                         timeMin=now, timeMax=tomorrow,
                                         singleEvents=True, orderBy='startTime'
                                         ).execute()

    print("Do you want to see the events for the next day or the first 10 events?")
    print("1. Events for today")
    print("2. first 10 events")
    inp = input()
    if int(inp) == 1:
        try:
            if weeklyEvents['items']:
                for event in weeklyEvents['items']:
                    print(event['summary'] + " -----", str(event['start'].get('dateTime')))
        except:
            print("This calendar has no events!")
    if int(inp) == 2:
        try:
            if first10Events['items']:
                for event in first10Events['items']:
                    print(event['summary'] + " -----", str(event['start'].get('dateTime')))
        except:
            print("This calendar has no events!")
    if inp is not None:
        # tryingto do the equivalent of ;
        # which is do nothing
        inp = 3

    #let the user see all events from all calendars for today
    print('Press Enter to continue...')
    input()

def doMain():
    while True:
        os.system('cls')
        print("Do you want to close the app or look at another calendar?")
        print("1. Look at calendars..")
        print("2. Exit..")
        inp = input()
        if int(inp) == 1:
            main()
        if int(inp) == 2:
            break
        if inp is not None:
            # tryingto do the equivalent of ;
            # which is do nothing
            inp = 3
    # fix this
    # it doesn't work correctly
    for i in range(3, -1, -1):
        if i != 0:
            print('Closing app in ', i, 'seconds')
        time.sleep(1)


if __name__ == '__main__':
    doMain()
    #transform datetime in time
    #now = datetime.datetime.utcnow()  # 'Z' indicates UTC time
    #tonight = now + datetime.timedelta(hours=24)
    #print(now)
    #print(tonight.iso)



