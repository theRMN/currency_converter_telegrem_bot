import requests
from bs4 import BeautifulSoup

CURRENCY = 'https://prodengi.kz/kurs-valyut'


def currency():
    full_page = requests.get(CURRENCY)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    data = soup.find('div', class_='national-bank-rate-simple-detail').text.split()
    c_data = {data[i]: data[i+1] for i in range(0, len(data), 2)}
    return c_data

