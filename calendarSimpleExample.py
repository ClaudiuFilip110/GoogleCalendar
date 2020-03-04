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

    #create an array for later use of calendarId
    calendarIds = []
    #populate calendarIds from the API
    for calendar in calendarList['items']:
        calendarIds.append(calendar['id'])

    #print the list of available calendarss
    i=1
    sys.stdout.flush()
    for calendar in calendarList['items']:
        print(str(i) + ". " + calendar['summary'])
        i+=1
    userInput = 0

    print("Choose a calendar to show events from it")
    #let the user choose the calendar
    while True:
        try:
            userInput = int(input())
        except ValueError:
            userInput = 0
        finally:
            if not(1 <= userInput <= i-1):
                print("The input must be a number!! between 1 and ", i-1)
            if userInput != 0 and 1 <= userInput <= i-1:
                break

    #add time for printing purposes
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    #get the events and print them
    events = service.events().list(calendarId=calendarIds[userInput-1], timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()

    try:
        errorBlock = events['items'][0]['id']
        if events['items']:
            for event in events['items']:
                print(event['summary'] + " -----", str(event['start'].get('dateTime')))
    except:
        print("This calendar has no events!")



    """
    the next task is to design an UI.
    """

if __name__ == '__main__':
    main()
    while True:
        print("Do you want to close the app or look at another calendar?")
        print("1. Look at calendar")
        print("2. Exit")
        inp = input()
        if int(inp) == 1:
            main()
        if int(inp) == 2:
            break
    #fix this
    #it doesn't work correctly
    for i in range(3, -1, -1):
        if i != 0:
            print('Closing app in ', i, 'seconds')
        time.sleep(1)