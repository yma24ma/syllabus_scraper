import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Authenticates with Google and returns the Calendar service.
    Handles token refreshing and initial login flow.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                return None # Signal that credentials.json is missing
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def add_event_to_calendar(service, title, date_str, effort_hours=1):
    """
    Adds a single event to the primary calendar.
    date_str should be 'YYYY-MM-DD'.
    """
    try:
        # Parse date
        start_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        end_date = start_date  # All day event usually
        
        event = {
          'summary': title,
          'description': f'Estimated Effort: {effort_hours} hours. Added via Syllabus Scraper.',
          'start': {
            'date': start_date.isoformat(),
            'timeZone': 'America/Los_Angeles', # Hardcoded for now, could be dynamic
          },
          'end': {
            'date': end_date.isoformat(),
            'timeZone': 'America/Los_Angeles',
          },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return True, event.get('htmlLink')
    except Exception as e:
        return False, str(e)
