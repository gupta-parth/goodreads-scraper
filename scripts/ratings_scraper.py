import csv
import re

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
        author_first = row[7]
        author_last = row[6]

        # The name doesn't have spaces, each new word starts with a capital
        name = row[8]
        name_list = [word for word in re.split('([A-Z][^A-Z]*)', name) if word]
        search_book_url = search_url + author_first + '+' + author_last
        for word in name_list:
            search_book_url += '+' + word
        if line_count != 0:
            print(
                f'Author: {author_first} {author_last}, Book: {str(name_list)}, Search: {search_book_url}')
        line_count += 1
        if line_count == 2:
            break
