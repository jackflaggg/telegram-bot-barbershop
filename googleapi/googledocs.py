import os

import gspread_asyncio
from google.oauth2.service_account import Credentials


# First, set up a callback function that fetches our credentials off the disk.
# gspread_asyncio needs this to re-authenticate when credentials expire.

def get_creds():
    # To obtain a service account JSON file, follow these steps:
    # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
    creds = Credentials.from_service_account_file(os.path.abspath('googleapi/key.json'))
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


# Create an AsyncioGspreadClientManager object which
# will give us access to the Spreadsheet API.

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


async def insert_rows(rows: list, url):
    agc = await agcm.authorize()
    agc = await agc.open_by_url(url)
    sh = await agc.get_worksheet(0)
    await sh.insert_rows(rows, row=3)


async def delete_task(url):
    agc = await agcm.authorize()
    agc = await agc.open_by_url(url)
    sh = await agc.get_worksheet(0)
    await sh.batch_clear(['A3:J1000'])


async def update_status(url, time, call, user):
    agc = await agcm.authorize()
    agc = await agc.open_by_url(url)
    sh = await agc.get_worksheet(0)
    find_time = await sh.find(time.replace('.', ':'))
    await sh.update_cell(call, find_time.col, user)


async def get_data_time(url):
    agc = await agcm.authorize()
    agc = await agc.open_by_url(url)
    sh = await agc.get_worksheet(0)
    data = await sh.get_values(range_name=f'')
    return data


async def remove_from_table(url,user_id):
    agc = await agcm.authorize()
    agc = await agc.open_by_url(url)
    sh = await agc.get_worksheet(0)
    found = await sh.find(str(user_id))
    await sh.update_cell(found.row, found.col, '')
