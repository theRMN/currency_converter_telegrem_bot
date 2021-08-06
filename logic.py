import re
import requests
from bs4 import BeautifulSoup

USD_KZT = 'https://prodengi.kz/kurs-valyut/konverter-valyut'


def actual_course():
    full_page = requests.get(USD_KZT)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.find_all('p', {'class': 'course-input'})
    content = re.sub('^\s+|\n|\r|\s+$', '', convert[0].text)
    return content
