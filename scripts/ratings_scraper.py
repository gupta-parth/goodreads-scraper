import csv
import re
from bs4 import BeautifulSoup
from matplotlib.pyplot import text
import requests
from sympy import content

'''
We want to scrape goodreads rating for each book in the conlit dataset and the number of ratings as well.
Obviously, we want to pick the average rating which has the highest number of ratings given since
that would be the most accurate averge rating.
'''

with open('data/txtlab_CONLIT_META_2022.csv', 'r', encoding='utf8', newline='') as f:
    search_url = 'https://www.goodreads.com/search?q='

    reader = csv.reader(f, delimiter='\t')      # File is delimited with tab
    line_count = 0
    for row in reader:
        if line_count != 0:
            author_first = row[7]
            author_last = row[6]

            # The name doesn't have spaces, each new word starts with a capital
            name = row[8]
            name_list = [word for word in re.split(
                '([A-Z][^A-Z]*)', name) if word]

            # Constructing the search url
            search_book_url = search_url + author_first + '+' + author_last
            for word in name_list:
                search_book_url += '+' + word

            # Set up soup object
            page = requests.get(search_book_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Check if there are no search results
            results = soup.find('h3', class_='searchSubNavContainer').text
            if results == 'No results.':
                # Search with just the book title (remove the author name)
                search_book_url = search_url
                for word in name_list:
                    search_book_url += '+' + word
                page = requests.get(search_book_url)
                soup = BeautifulSoup(page.content, 'html.parser')

            # Get all the book results
            main_content_div = soup.find('div', class_='mainContent')
            main_content_float = main_content_div.find(
                'div', class_='mainContentFloat')
            left_container = main_content_float.find(
                'div', class_='leftContainer')
            book_results = soup.find_all('tr')
            print(
                f'Line: {line_count + 1}, Author: {author_first} {author_last}, Book: {str(name_list)}, Search: {search_book_url}')

            for book in book_results:
                rating_text = book.find('span', class_='minirating').text
                text_list = rating_text.split()
                print(
                    f"Avg: {text_list[-6]}, Number: {int(text_list[-2].replace(',',''))}")

            print('---------------------------')

        line_count += 1
        if line_count == 10:
            break
