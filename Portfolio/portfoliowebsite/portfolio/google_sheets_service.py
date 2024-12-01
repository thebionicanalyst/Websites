from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE =  '/code/secrets/bionic-gs-key.json'

def connect_to_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    client = gspread.authorize(creds)
    return client

def append_to_sheet(sheet_id,values):
    client = connect_to_google_sheets()
    sheet = client.open_by_key(sheet_id)
    sheet.values_append(
    range='Contacts',  # Specify the sheet name
    body={'values': values},
    params={'valueInputOption': 'RAW'}  # or 'USER_ENTERED' based on your needs
)
