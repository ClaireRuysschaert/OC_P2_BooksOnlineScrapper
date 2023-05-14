import requests
from bs4 import BeautifulSoup
import bs4 

url = "http://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/index.html"

response = requests.get(url)
content = response.content
if response.ok:  # returns status code 200
    soup = BeautifulSoup(content.decode('utf-8','ignore'), features="lxml")

title = ((soup.find("title")).text)[5:-1] # Remove \n and spaces from title

tds = soup.findAll("td")  # column Product information with all the informations

def get_the_individual_td(tds: bs4.element.ResultSet):
    upc = (tds[0]).text
    product_type = (tds[1]).text
    price_without_tax = ((tds[2]).text)
    price_with_tax = ((tds[3]).text)
    availability = (tds[5]).text
    number_of_reviews = (tds[6]).text
    return upc, product_type, price_without_tax, price_with_tax, availability, number_of_reviews

upc, product_type, price_without_tax, price_with_tax, availability, number_of_reviews = get_the_individual_td(tds)
all_p_tags = soup.findAll("p")
description = (all_p_tags[3]).text
all_a_tags = soup.findAll("a")
category = (all_a_tags[3]).text

image_tag = soup.select("img")
image_url = "http://books.toscrape.com/" + image_tag[0].get("src")

with open("test.csv", "w", encoding="utf-8-sig") as csv_file: 
    csv_file.write(
        "product_page_url;universal_ product_code (upc);title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n"
    )
    csv_file.write(';'.join([url, upc, title, price_with_tax, price_without_tax, availability, description, category, number_of_reviews, image_url])
    )
