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
    """
    take a bs4 element ResultSet with all the rows of the page and returns text with wanted informations 
    """
    upc = (tds[0]).text
    product_type = (tds[1]).text
    price_without_tax = ((tds[2]).text)
    price_with_tax = ((tds[3]).text)
    availability = (tds[5]).text
    return upc, product_type, price_without_tax, price_with_tax, availability

upc, product_type, price_without_tax, price_with_tax, availability = get_the_individual_td(tds)
all_p_tags = soup.findAll("p")
description = (all_p_tags[3]).text
all_a_tags = soup.findAll("a")
category = (all_a_tags[3]).text

def get_number_stars(selected_html: bs4.element.Tag):
    """
    Give the book's star rating
    Maximum rate is 5/5
    """
    number_of_stars = selected_html.attrs["class"][1]
    return f"{number_of_stars} out of Five"


number_of_stars = get_number_stars(soup.select_one(".star-rating"))

image_tag = soup.select("img")
image_url = "http://books.toscrape.com/" + image_tag[0].get("src")

with open("test.csv", "w", encoding="utf-8-sig") as csv_file: 
    csv_file.write(
        "product_page_url;universal_ product_code (upc);title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n"
    )
    csv_file.write(';'.join([url, upc, title, price_with_tax, price_without_tax, availability, description, category, number_of_stars, image_url])
    )
