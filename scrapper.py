import os
import requests
from soup_requester import (
    get_categories_name_url,
    get_book_list_url,
    get_book_informations,
)
from soup_requester import HOME_PAGE_URL

# 1 create root CSV_IMAGE folder
ROOT_FOLDER_NAME = "CSV-IMAGES"
root_folder_path = os.path.join(os.getcwd(), ROOT_FOLDER_NAME)
if not os.path.isdir(root_folder_path):
    os.mkdir(root_folder_path)

categories_name_url = get_categories_name_url(HOME_PAGE_URL)

books_categories_urls = {}
for category_name, category_url in categories_name_url.items():
    books_categories_urls[category_name] = get_book_list_url(category_url)


for category, book_links in books_categories_urls.items():
    csv_name = f"{category} - Book's information from Books to Scrape.csv"

    # 2 create one folder for each category name
    category_folder_name = category
    category_folder_path = os.path.join(root_folder_path, category_folder_name)
    if not os.path.isdir(category_folder_path):
        os.mkdir(category_folder_path)

    # Create CSV file
    with open(
        os.path.join(ROOT_FOLDER_NAME, category_folder_name, csv_name),
        "w",
        encoding="utf-8-sig",
    ) as csv_file:
        csv_file.write(
            "product_page_url;universal_ product_code (upc);title;price_including_tax;price_excluding_tax;number_available;product_description;category;review_rating;image_url\n"
        )

        image_title_and_urls_list = []
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
            image_title_and_urls_list.append((title, image_url))

    # Create the image
    for title, image_url in image_title_and_urls_list:

        image_title = title.replace("/", "-") + ".jpg"

        with open(
            os.path.join(ROOT_FOLDER_NAME, category_folder_name, image_title), "wb"
        ) as image_file:
            res = requests.get(image_url)

            for chunk in res.iter_content(100000):
                image_file.write(chunk)
