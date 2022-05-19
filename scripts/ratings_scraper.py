import csv

'''
We want to scrape goodreads rating for each book in the conlit dataset and the number of ratings as well.
Obviously, we want to pick the average rating which has the highest number of ratings given since
that would be the most accurate averge rating.
'''

with open('data/txtlab_CONLIT_META_2022.csv', 'r', encoding='utf8', newline='') as f:

    reader = csv.reader(f, delimiter='\t')      # File is delimited with tab
    line_count = 0
    for row in reader:
        author_first = row[7]
        author_last = row[6]
        name = row[8]
        print(f"Author: {author_first} {author_last}, Book Name: {name}")
        line_count += 1
    print(line_count)
