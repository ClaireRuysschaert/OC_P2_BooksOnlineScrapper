from soup_requester import get_soup

category_url = ("http://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html")
final_book_links = []


def get_book_list_url(category_url):
    """get a book's category url and returns book url list"""

    book_list_soup = get_soup(category_url).select("article a")  # <a> in <article>
    book_links = []

    next_soup = get_soup(category_url).select(".next a")
    next_link = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/" + str(next_soup[0].get("href"))

    # first iteration
    for num, book in enumerate(book_list_soup):
        if (num%2)==0:
            book_url = ("https://books.toscrape.com/catalogue/" + book.get("href")[9:])
            book_links.append(book_url)
    
    # next iterations
    while next_soup:
        next_link = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/" + str(next_soup[0].get("href"))
        category_url = next_link
        book_list_soup = get_soup(category_url).select("article a")
        for num, book in enumerate(book_list_soup):
            if (num%2)==0:
                book_url = ("https://books.toscrape.com/catalogue/" + book.get("href")[9:])  
                book_links.append(book_url)
        next_soup = get_soup(category_url).select(".next a")

    return book_links


final_book_links += get_book_list_url(category_url)


def get_book_informations(book_url: str):
    
    soup = get_soup(book_url)

    title = ((soup.find("title")).text)[5:-1]  # Remove \n and spaces from title
    tds = soup.findAll("td")  # column Product information with all the informations
    upc = (tds[0]).text
    price_without_tax = (tds[2]).text
    price_with_tax = (tds[3]).text
    availability = (tds[5]).text
    all_p_tags = soup.findAll("p")
    description = (all_p_tags[3]).text.replace(";", "")
    all_a_tags = soup.findAll("a")
    category = (all_a_tags[3]).text
    number_of_stars = soup.select_one(".star-rating").attrs["class"][1]
    review_rating = f"{number_of_stars} out of Five"
    image_tag = soup.select("img")
    image_url = "http://books.toscrape.com/" + image_tag[0].get("src")

    return (upc, title, price_with_tax, price_without_tax, availability, description, category, review_rating, image_url)


with open("test.csv", "w", encoding="utf-8-sig") as csv_file:
    
    csv_file.write(
        "product_page_url|universal_ product_code (upc)|title|price_including_tax|price_excluding_tax|number_available|product_description|category|review_rating|image_url\n")
    
    for book_url in final_book_links:
        (upc, title, price_with_tax, price_without_tax, availability, description, category, review_rating, image_url) = get_book_informations(book_url)
        csv_file.write("|".join([book_url, upc, title, price_with_tax, price_without_tax, availability, description, category, review_rating, image_url]))
        csv_file.write("\n")
