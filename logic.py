import requests
from bs4 import BeautifulSoup
from config import MAIN_CURRENCY, CURRENCY_URL


def get_currency_data():
    full_page = requests.get(CURRENCY_URL)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    data = soup.find('div', class_='national-bank-rate-simple-detail').text.split()
    currency_data = {data[i]: data[i+1] for i in range(0, len(data), 2)}

    return currency_data


def cur_convert(amount, currency, new_currency):
    currency_data = get_currency_data()
    currency_data[MAIN_CURRENCY] = 1

    if currency and new_currency not in currency_data:
        return None

    if currency == new_currency:
        return amount

    if currency == MAIN_CURRENCY:
        result = amount / float(currency_data[new_currency])
    else:
        result = (amount * float(currency_data[currency])) / float(currency_data[new_currency])

    return round(result, 2)

