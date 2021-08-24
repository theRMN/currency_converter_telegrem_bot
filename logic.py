import re
import requests
from bs4 import BeautifulSoup

USD_KZT = 'https://prodengi.kz/kurs-valyut/konverter-valyut'
CURRENCY = 'https://prodengi.kz/kurs-valyut'


def actual_course():
    full_page = requests.get(USD_KZT)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.find_all('p', {'class': 'course-input'})
    content = re.sub('^\s+|\n|\r|\s+$', '', convert[0].text)
    return content


def currency():
    full_page = requests.get(CURRENCY)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    data = soup.find('div', class_='national-bank-rate-simple-detail').text.split()
    c_data = {data[i]: data[i+1] for i in range(0, len(data), 2)}
    return c_data

