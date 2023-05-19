import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)  # faire une fonction soup
    content = response.content
    if response.ok:  # returns status code 200
        soup = BeautifulSoup(content.decode("utf-8", "ignore"), features="lxml")
    return soup
