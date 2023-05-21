from soup_requester import (
    get_categories_name_url,
    get_book_list_url,
    get_book_informations,
)
from soup_requester import HOME_PAGE_URL


categories_name_url = get_categories_name_url(HOME_PAGE_URL)
books_categories_urls = {}

for category_name, category_url in categories_name_url.items():
    books_categories_urls[category_name] = get_book_list_url(category_url)

for category, book_links in books_categories_urls.items():
    csv_file_name = f"{category} - Book's information from Books to Scrape.csv"

    with open(csv_file_name, "w", encoding="utf-8-sig") as csv_file:
        csv_file.write(
            "product_page_url;universal_ product_code (upc);title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n"
        )

        for book_url in book_links:
            (
                upc,
                title,
                price_with_tax,
                price_without_tax,
                availability,
                description,
                category,
                review_rating,
                image_url,
            ) = get_book_informations(book_url)
            csv_file.write(
                ";".join(
                    [
                        book_url,
                        upc,
                        title,
                        price_with_tax,
                        price_without_tax,
                        availability,
                        description,
                        category,
                        review_rating,
                        image_url,
                    ]
                )
            )
            csv_file.write("\n")
