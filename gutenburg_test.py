import requests, random
from bs4 import BeautifulSoup

r = requests.get('https://www.gutenberg.org/ebooks/1000')
soup = BeautifulSoup(r.text, 'html.parser') 

book_title = soup.find("title").text.split(" - ")[0]
book_cover = soup.find("img",{"class":"cover-art"})['src']

print(book_title)
print(book_cover)

