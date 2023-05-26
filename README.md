# How to use the script

## Required software and tools
Before getting started, you need to install python 3 and git on your computer. 
You will also need to choose a code editor, for example VScode or PyCharm. 

## Getting started

- Clone the code from the repository *(Make sure you are in the current working directory that you want)*
> git clone https://github.com/ClaireRuysschaert/OC_P2_BooksOnlineScrapper.git

- Create and activate a virtual environment.

MacOs/Linux:
> python3 -m venv .venv
> .venv/bin/activate

Windows:
> python -m venv .venv
> .venv/Script/activate

- Then you can install all the requirements for the script.
> pip install -r requirements.txt

## Launch the script
You can now launch the **scrapper.py** that will extract the data from Books to Scrap.

The script will :
    - Get categories names and urls from home page
    - Get book's url list from a category url
    - Get 9 book's information from detail book url (Product page url, Universal product code, Title, Price including ans excluding tax, Number available, Product description, Category, Review rating, Image url) 