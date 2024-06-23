import pandas as pd
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SPREADSHEET_ID, URL_SHEET_NAME, DIRECTORY_SHEET_NAME, PROPERTY_URL
from sheets_operations import get_sheet_service, get_sheet_values, update_sheet_values, add_columns_to_sheet
from search_console_operations import get_search_console_service, get_index_status
from utils import get_column_letter

def main():
    service = get_sheet_service()
    search_console_service = get_search_console_service()
    
    # シートメタデータの取得
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')

    # URLシートのデータを取得
    for sheet in sheets:
        if sheet.get("properties", {}).get("title", "") == URL_SHEET_NAME:
            url_column_count = sheet.get("properties", {}).get("gridProperties", {}).get("columnCount", 26)
            break

    last_url_column_letter = get_column_letter(url_column_count)
    url_range_name = f'{URL_SHEET_NAME}!A1:{last_url_column_letter}'
    url_values = get_sheet_values(service, SPREADSHEET_ID, url_range_name)
    
    if len(url_values) > 1:
        df = pd.DataFrame(url_values[1:], columns=url_values[0])
    else:
        df = pd.DataFrame(columns=['url'])

    num_columns = len(df.columns)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    df[date] = df['url'].apply(lambda url: get_index_status(search_console_service, url, PROPERTY_URL))

    new_column_letter = get_column_letter(num_columns + 1)

    # 列が足りない場合に列を追加
    if num_columns + 1 > url_column_count:
        add_columns_to_sheet(service, SPREADSHEET_ID, URL_SHEET_NAME, num_columns + 1 - url_column_count)

    update_range = f'{URL_SHEET_NAME}!{new_column_letter}1'
    url_values = [[date]] + df[date].values.reshape(-1, 1).tolist()
    update_sheet_values(service, SPREADSHEET_ID, update_range, url_values)

    # directoriesシートのデータを取得
    for sheet in sheets:
        if sheet.get("properties", {}).get("title", "") == DIRECTORY_SHEET_NAME:
            directory_column_count = sheet.get("properties", {}).get("gridProperties", {}).get("columnCount", 26)
            break

    last_directory_column_letter = get_column_letter(directory_column_count)
    directory_range_name = f'{DIRECTORY_SHEET_NAME}!A1:{last_directory_column_letter}'
    directory_values = get_sheet_values(service, SPREADSHEET_ID, directory_range_name)

    if len(directory_values) > 1:
        directory_df = pd.DataFrame(directory_values[1:], columns=directory_values[0])
    else:
        directory_df = pd.DataFrame(columns=['directory'])

    num_directory_columns = len(directory_df.columns)
    directory_df[date] = 0.0

    for i, row in directory_df.iterrows():
        regex = row['directory']
        matched_urls = df[df['url'].str.contains(regex, na=False, regex=True)]
        total_count = matched_urls.shape[0]
        indexed_count = matched_urls[matched_urls[date] == 'Submitted and indexed'].shape[0]
        index_rate = indexed_count / total_count if total_count > 0 else 0
        directory_df.at[i, date] = index_rate

    new_directory_column_letter = get_column_letter(num_directory_columns + 1)

    # 列が足りない場合に列を追加
    if num_directory_columns + 1 > directory_column_count:
        add_columns_to_sheet(service, SPREADSHEET_ID, DIRECTORY_SHEET_NAME, num_directory_columns + 1 - directory_column_count)

    directory_update_range_name = f'{DIRECTORY_SHEET_NAME}!{new_directory_column_letter}1'
    directory_values = [[date]] + directory_df[date].values.reshape(-1, 1).tolist()
    update_sheet_values(service, SPREADSHEET_ID, directory_update_range_name, directory_values)

if __name__ == "__main__":
    main()
