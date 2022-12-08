from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.packtpub.com/free-learning')
soup = BeautifulSoup(r.text, 'html.parser')

book_title = soup.find("h3", {"class":"product-info__title"}).text
book_author = soup.find("span", {"class":"product-info__author"}).text
book_date = soup.find("div", {"class":"free_learning__product_pages_date"}).text
book_pages = soup.find("div", {"class":"free_learning__product_pages"}).text
book_desc = soup.find("div",{"class":"free_learning__product_description"}).text
book_cover = soup.find("img",{"class":"product-image"})['src']

print(book_title)
print(book_author)
print(book_date)
print(book_pages)
print(book_desc)
print(book_cover)
