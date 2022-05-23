import csv
import re
from bs4 import BeautifulSoup
import requests


'''
We want to scrape goodreads rating for each book in the conlit dataset and the number of ratings as well.
Obviously, we want to pick the average rating which has the highest number of ratings given since
that would be the most accurate averge rating.
'''
misses = []
with open('data/txtlab_CONLIT_META_2022.csv', 'r', encoding='utf8', newline='') as f, \
        open('data/output.csv', 'a', encoding='utf8', newline='') as out:
    search_url = 'https://www.goodreads.com/search?q='

    reader = csv.reader(f, delimiter='\t')      # File is delimited with tab
    writer = csv.writer(out, delimiter='\t')
    header = ['ID', 'Category', 'Language', 'Genre', 'Genre2', 'Pubdate', 'Author_Last', 'Author_First',
              'Work_Title', 'Translation', 'PubHouse',
              'Prize', 'WinnerShortlist', 'Author_Gender', 'Author_Nationality', 'Goodreads_Rating', 'Review_Count', 'Goodreads_URL']
    writer.writerow(header)

    rows = [r for r in reader]

    for i in range(len(rows)):
        row = rows[i]
        if i != 0:
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
            print(search_book_url)

            # Check if there are no search results
            tries = 3
            for x in range(tries):
                try:
                    results = soup.find(
                        'h3', class_='searchSubNavContainer').text
                    if results == 'No results.':
                        # Search with just the book title (remove the author name)
                        search_book_url = search_url
                        for word in name_list:
                            search_book_url += '+' + word
                        page = requests.get(search_book_url)
                        soup = BeautifulSoup(page.content, 'html.parser')
                except:
                    if x < tries - 1:
                        continue
                    else:
                        print(soup)
                        print(f"Index: {i}")
                        raise
                break

            # Get all the book results
            tries = 3
            for x in range(tries):
                try:
                    main_content_div = soup.find('div', class_='mainContent')
                    main_content_float = main_content_div.find(
                        'div', class_='mainContentFloat')
                    left_container = main_content_float.find(
                        'div', class_='leftContainer')
                    book_results = soup.find_all('tr')
                except:
                    if x < tries - 1:
                        continue
                    else:
                        print(soup)
                        print(f"Index: {i}")
                        raise

            print(
                f'Line: {i}, Author: {author_first} {author_last}, Book: {str(name_list)}, Search: {search_book_url}')
            max_reviews = -10000000000
            rating = 0.00
            for book in book_results:
                rating_text = book.find('span', class_='minirating').text
                text_list = rating_text.split()
                num_reviews = int(text_list[-2].replace(',', ''))
                rating_given = text_list[-6]
                if num_reviews > max_reviews:
                    max_reviews = num_reviews
                    rating = rating_given
                print(
                    f"Avg: {text_list[-6]}, Number: {int(text_list[-2].replace(',',''))}")
            if max_reviews == -10000000000:
                misses.append("Line " + str(i))

            print(f"Rating: {rating}, Reviews: {max_reviews}")
            row.append(rating)
            row.append(max_reviews)
            row.append(search_book_url)
            writer.writerow(row)
            print('---------------------------')

print(len(misses))
print(misses)
