import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3



def get_div_tags(soup):
    selected_class = 'book-item'
    div_tags = soup.find_all('div', {'class': selected_class})
    return div_tags


def get_titles(tags_list):
    title_list = []
    for tag in tags_list:
        title = tag.find_all('a')[1].text.strip()
        title_list.append(title)
    return title_list
        

def get_authors(tags_list):
    author_list = []
    for tag in tags_list:
        author = tag.find_all('a')[2].text.strip()
        author_list.append(author)
    return author_list


def get_date(tags_list):
    date_list = []
    for tag in tags_list:
        try:
            date = tag.find('p', {'class': 'published'}).text
            date_list.append(date)
        except AttributeError:
            date_list.append(None)
    return date_list



''' get individual book info '''
def cover_list(tags_list):
    cover_list = []
    for tag in tags_list:
        try:
            cover = tag.find('p', {'class': 'format'}).text
            cover_list.append(cover)
        except AttributeError:
            cover_list.append(None)
    return cover_list


def get_price(tags_list):
    price_list = []
    for tag in tags_list:
        try:
            price = tag.find('div', {'class': 'price-wrap'}).find('span').text.split('₹')[1].replace(',', '')
            price_list.append(float(price))
        except AttributeError:
            price_list.append(None)
    return price_list


def get_ratings(soup):
    rating = []
    total_ratings = []
    rating_tags = soup.find('div', {'class': 'rating-wrap'})
    try:
        if rating_tags is None:
            rating.append(None)
            total_ratings.append(None)
        else:
            rating.append(float(rating_tags.find_all('span')[5].text.strip()))
            total_ratings.append(int(rating_tags.find_all('span')[6].text.strip().strip('()').split(' ')[0].replace(',', '')))
    except IndexError:
        rating.append(None)
        total_ratings.append(None)
    return rating, total_ratings


def get_language(soup):
    language = []
    language_tags = soup.find('ul', {'class': 'meta-info'})
    try:
        if language_tags is None:
            language.append(None)
        else:
            language.append(language_tags.select('span > a')[0].text)
    except (AttributeError, IndexError):
        language.append(None)
    return language


def get_publisher(soup):
    publisher = []
    publisher.append(soup.select_one('.biblio-info').select_one('span[itemprop="publisher"]').text.strip())
    return publisher


def get_book_info(tags_list):
    rating = []
    total_ratings = []
    language = []
    publisher = []
    for tag in tags_list:
        href = tag.find('div', {'class': 'item-info'}).find('a')['href']
        response = requests.get('https://www.bookdepository.com' + href)
        soup = BeautifulSoup(response.text, 'html.parser')
        stars, total_rating = get_ratings(soup)
        rating += stars
        total_ratings += total_rating
        language += get_language(soup)
        publisher += get_publisher(soup)
    return rating, total_ratings, language, publisher


def scrape_data():
    books = {
    'title': [],
    'author': [],
    'published': [],
    'publisher': [],
    'format': [],
    'language': [],
    'price (₹)': [],
    'rating': [],
    'total_ratings': []
    }
    page = 1
    while page < 35:
        response = requests.get(f'https://www.bookdepository.com/bestsellers?page={page}')
        print(f'Scraping page no: {page}, Page response code: {response.status_code}')
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tags = get_div_tags(soup)
        books['title'] += get_titles(div_tags)
        books['author'] += get_authors(div_tags)
        books['published'] += get_date(div_tags)
        books['format'] += cover_list(div_tags)
        books['price (₹)'] += get_price(div_tags)
        rating, total_ratings, language, publisher = get_book_info(div_tags)
        books['publisher'] += publisher
        books['language'] += language
        books['rating'] += rating
        books['total_ratings'] += total_ratings
        page = page + 1
    return pd.DataFrame(books)


def main():
    books_df = scrape_data()
    print("Inserting data into database...")
    with sqlite3.connect('books.db') as con:
        cur = con.cursor()
        for index, row in books_df.iterrows():
            cur.execute(
                "INSERT INTO books (title, author, published, publisher, format, language, price, rating, total_ratings) VALUES (?,?,?,?,?,?,?,?,?)",
                (row['title'], row['author'], row['published'], row['publisher'], row['format'], row['language'], row['price (₹)'], row['rating'], row['total_ratings'],))
    print("Completed.")


main()

