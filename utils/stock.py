import requests
from bs4 import BeautifulSoup

from config import TW_REAL_TIME_URL, US_REAL_TIME_URL


def _convert_float(text):
    if text.find(',') != -1:
        return float(''.join(text.split(',')))
    else:
        return float(text)


def _get_real_time_TW(stock_id):
    stock_resquest = requests.get(TW_REAL_TIME_URL.format(stock_id))
    stock_soup = BeautifulSoup(stock_resquest.text, 'html.parser')
    stock_soup = stock_soup.find('span', id="Price1_lbTPrice")

    return _convert_float(stock_soup.text)


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
