from time import sleep

import arrow

from config import *
from utils.push import pushImage, pushMessage
from utils.sheets import GoogleSheet
from utils.content import get_final_record, plot_records_table

def main(country, state):
    if country == 'TW':
        now = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    elif country == 'US':
        now = arrow.now('America/New_York').format('YYYY-MM-DD HH:mm:ss')

    client = GoogleSheet(key_json=GOOGLE_SHEET_API_KEY,
                            sheet_url=GOOGLE_SHEET_STOCK_URL)
    records = get_final_record(client=client, country=country)
    plot_records_table(records)

    message = f'{country} Position {now} - {state}'
    pushImage(token=STOCK_ACCOUNT_LINE_NOTIFY_TOKEN,
              msg=message,
              image_path='./images/records.png')

    print("Send", message)


if __name__ == "__main__":

    while True:
        TW_now = arrow.now()
        US_now = arrow.now('America/New_York')
        main(country='TW', state='NOW')

        if TW_now.weekday() < 5:
            if TW_now.hour == 9 and TW_now.minute > 0 and TW_now.minute < 9:
                main(country='TW', state='OPEN')

            elif TW_now.hour == 13 and TW_now.minute > 30 and TW_now.minute < 39:
                main(country='TW', state='CLOSE')

        if US_now.weekday() < 5:
            if US_now.hour == 9 and US_now.minute > 30 and US_now.minute < 39:
                main(country='US', state='OPEN')

            elif US_now.hour == 16 and US_now.minute > 0 and US_now.minute < 9:
                main(country='US', state='CLOSE')

        sleep(60 * SLEEP_MINUTES)
