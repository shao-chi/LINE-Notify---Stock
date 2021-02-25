from time import sleep

import arrow

from config import *
from utils.push import pushImage, pushMessage
from utils.sheets import GoogleSheet
from utils.content import get_final_record, plot_records_table

def main(country, state):
    if country == 'TW':
        date = arrow.now().format('YYYY-MM-DD')
    elif country == 'US':
        date = arrow.now('US/Pacific').format('YYYY-MM-DD')

    client = GoogleSheet(key_json=GOOGLE_SHEET_API_KEY,
                            sheet_url=GOOGLE_SHEET_STOCK_URL)
    records = get_final_record(client=client, country='US')
    plot_records_table(records)

    pushImage(token=STOCK_ACCOUNT_LINE_NOTIFY_TOKEN,
              msg=f'{country} Position {date} - {state}',
              image_path='./images/records.png')


if __name__ == "__main__":

    while True:
        TW_now = arrow.now()
        US_now = arrow.now('US/Pacific')

        if TW_now.hour == 9 and (TW_now.minute > 0 or TW_now.minute < 9):
            main(country='TW', state='OPEN')
            print(f"Send TW Position {TW_now.format('YYYY-MM-DD')} - OPEN")

        elif TW_now.hour == 13 and (TW_now.minute > 30 or TW_now.minute < 39):
            main(country='TW', state='CLOSE')
            print(f"Send TW Position {TW_now.format('YYYY-MM-DD')} - CLOSE")

        if US_now.hour == 6 and (US_now.minute > 30 or US_now.minute < 39):
            main(country='US', state='OPEN')
            print(f"Send US Position {TW_now.format('YYYY-MM-DD')} - OPEN")

        elif US_now.hour == 13 and (US_now.minute > 0 or US_now.minute < 9):
            main(country='US', state='CLOSE')
            print(f"Send US Position {TW_now.format('YYYY-MM-DD')} - CLOSE")

        sleep(60 * SLEEP_MINUTES)
