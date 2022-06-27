import os
import httplib2
import apiclient
from decimal import Decimal
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pycbrf import ExchangeRates


def get_currency() -> Decimal:

    now_date = datetime.now()
    curr_rub = ExchangeRates(now_date)
    return curr_rub["USD"].value


CREDENTIALS_FILE: str = 'credentials.json'

spreadsheet_id: str = os.getenv('SPREADSHEET_ID')
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']
)

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_all_values() -> tuple:

    info = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="B2:D",
        majorDimension="ROWS"
    ).execute()

    return info.get("values")


def get_deleted_sales(new_sale_list: tuple, old_sale_list: list) -> list:

    deleted_sales_tuple = tuple(sale[0] for sale in old_sale_list if sale[0] not in new_sale_list)
    print(deleted_sales_tuple)

    deleted_sales = list()

    for sale in old_sale_list:
        if sale[0] not in new_sale_list:
            deleted_sales.append(sale[0])

    return deleted_sales
