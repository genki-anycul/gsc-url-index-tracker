from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import SERVICE_ACCOUNT_FILE, SCOPES

def get_sheet_service():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_sheet_values(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

def update_sheet_values(service, spreadsheet_id, range_name, values):
    body = {
        'range': range_name,
        'majorDimension': 'ROWS',
        'values': values
    }
    response = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    return response

def add_columns_to_sheet(service, spreadsheet_id, sheet_name, num_columns):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')

    for sheet in sheets:
        if sheet.get("properties", {}).get("title", "") == sheet_name:
            sheet_id = sheet.get("properties", {}).get("sheetId", "")
            break

    requests = [{
        "appendDimension": {
            "sheetId": sheet_id,
            "dimension": "COLUMNS",
            "length": num_columns
        }
    }]
    body = {
        "requests": requests
    }
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    return response
