import requests
from bs4 import BeautifulSoup

from config import FINMIND_API, US_REAL_TIME_URL


def _convert_float(text):
    if text.find(',') != -1:
        return float(''.join(text.split(',')))
    else:
        return float(text)


def _get_real_time_TW(stock_id):
    parameter = {"dataset": "TaiwanStockPriceTick",
                 "data_id": stock_id}

    stock_resquest = requests.get(FINMIND_API, params=parameter)
    stock_data = stock_resquest.json()['data']

    return stock_data[-1]['deal_price']


def _get_real_time_US(stock_id):
    parameter = {"s": stock_id}

    stock_resquest = requests.get(US_REAL_TIME_URL, params=parameter)
    stock_soup = BeautifulSoup(stock_resquest.text, 'html.parser')
    
    return _convert_float(stock_soup.find_all('font')[3].text)


def get_real_time(stock_id, country):
    assert country in ['TW', 'US']

    if country == 'TW':
        return _get_real_time_TW(stock_id=stock_id)
    elif country == 'US':
        return _get_real_time_US(stock_id=stock_id)
