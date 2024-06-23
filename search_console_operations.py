from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import SERVICE_ACCOUNT_FILE, SEARCH_CONSOLE_SCOPES

def get_search_console_service():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SEARCH_CONSOLE_SCOPES)
    service = build('searchconsole', 'v1', credentials=credentials)
    return service

def get_index_status(service, url, site_url):
    request = {
        'inspectionUrl': url,
        'siteUrl': site_url
    }
    try:
        response = service.urlInspection().index().inspect(body=request).execute()
        return response['inspectionResult']['indexStatusResult']['coverageState']
    except Exception as e:
        print(f"Error inspecting URL {url}: {e}")
        print(f"Request sent: {request}")
        return 'Error'
