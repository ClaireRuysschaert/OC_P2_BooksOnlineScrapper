import requests
from bs4 import BeautifulSoup


BASE_URL = "http://books.toscrape.com/"
HOME_PAGE_URL = "https://books.toscrape.com/index.html"


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    content = response.content
    if response.ok:
        soup = BeautifulSoup(content.decode("utf-8", "ignore"), features="lxml")

    return soup


def get_categories_name_url(home_page_url: str) -> dict:
    """Get categories names and urls from home page."""

    categories_soup = get_soup(home_page_url).select(".nav-list a")
    categories_name_url = {}

    for category in categories_soup:
        category_url = BASE_URL + category["href"]
        category_name = category.text.strip()
        categories_name_url[category_name] = category_url

    del categories_name_url["Books"]  # Remove the home page from dict

    return categories_name_url


def get_book_list_url(category_url: str) -> list:
    """Get book's url list from a category url."""

    book_list_soup = get_soup(category_url).findAll("h3")
    book_links = []

    # removes "index.html" from category url given
    base_category_url = "/".join(category_url.split("/")[:-1]) + "/"

    while True:
        for book in book_list_soup:
            book_url = BASE_URL + "catalogue/" + book.a["href"][9:]
            book_links.append(book_url)

        next_soup = get_soup(category_url).select(".next a")
        if next_soup:
            next_link = base_category_url + str(next_soup[0].get("href"))
            next_link = base_category_url + str(next_soup[0].get("href"))
            category_url = next_link
            book_list_soup = get_soup(category_url).findAll("h3")
        else:
            break

    return book_links


def get_book_informations(book_url: str) -> tuple:
    """Get 9 book's information from detail book url.
    - Product page url,
    - Universal product code
    - Title
    - Price including tax
    - Price excluding tax
    - Number available
    - Product description
    - Category
    - Review rating
    - Image_url"""

    detail_book_soup = get_soup(book_url)

    title = detail_book_soup.select_one("h1").text

    column_infos = detail_book_soup.findAll("td")  # column Product information

    upc = (column_infos[0]).text
    price_without_tax = (column_infos[2]).text
    price_with_tax = (column_infos[3]).text
    availability = (column_infos[5]).text

    all_p_tags = detail_book_soup.findAll("p")

    description = (all_p_tags[3]).text.replace(";", "").strip()

    if not description:
        description = "No description for this book."

    all_a_tags = detail_book_soup.findAll("a")

    category = (all_a_tags[3]).text

    number_of_stars = detail_book_soup.select_one(".star-rating").attrs["class"][1]
    review_rating = f"{number_of_stars} out of Five"

    image_tag = detail_book_soup.select("img")
    image_url = BASE_URL + image_tag[0].get("src")

    return (
        upc,
        title,
        price_with_tax,
        price_without_tax,
        availability,
        description,
        category,
        review_rating,
        image_url,
    )
