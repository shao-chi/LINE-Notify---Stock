import plotly.graph_objects as go
import pandas as pd

from config import *
from utils.stock import get_real_time

def get_final_record(client, country):
    assert country in ['TW', 'US']

    client.set_worksheet(sheet_name=POSITION_SHEET_NAME[country])

    stock_list = client.get_values(start=SHEET_VALUE_START,
                                   end=SHEET_VALUE_END)
    stock = []
    for stock_data in stock_list:
        if stock_data[0] == '':
            break

        price = get_real_time(stock_id=stock_data[0],
                              country=country)
        cost = float(stock_data[3])
        gain = str(round(((price - cost) / cost) * 100, 3)) + '%'

        stock_dict = {"id": stock_data[0],
                      "name": stock_data[1],
                      "cost": cost,
                      "price": price,
                      "gain": gain}

        stock.append(stock_dict)

    return stock


def plot_records_table(records):
    length = len(records)
    dataframe = pd.DataFrame.from_records(records)

    # Set gain color
    text_color = []
    for col in dataframe.columns:
        if col != 'gain':
            text_color.append(['darkslategray'] * length)
        else:
            color = []

            for gain in dataframe['gain'].values:
                if gain[0] != '-':
                    color.append('red')
                else:
                    color.append('green')

            text_color.append(color)

    fig = go.Figure(data=[go.Table(header=dict(values=dataframe.columns),
                                   cells=dict(values=dataframe.values.T,
                                              font=dict(color=text_color)))])
    fig.write_image('./images/records.png', scale=2)
