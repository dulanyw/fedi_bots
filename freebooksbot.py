import requests, random
from bs4 import BeautifulSoup
from datetime import datetime
from mastodon import Mastodon

#Class to pull the information from sources and frame into toots
class TootFramer():

    #Framer for the daily Packt Free Ebook
    def packt():
        #scrape the page, push into BeautifulSoup object
        r = requests.get('https://www.packtpub.com/free-learning')
        soup = BeautifulSoup(r.text, 'html.parser')

        #Get key post elements
        book_title = soup.find("h3", {"class":"product-info__title"}).text
        book_author = soup.find("span", {"class":"product-info__author"}).text
        book_date = soup.find("div", {"class":"free_learning__product_pages_date"}).text
        book_pages = soup.find("div", {"class":"free_learning__product_pages"}).text
        book_desc = soup.find("div",{"class":"free_learning__product_description"}).text
        book_cover = soup.find("img",{"class":"product-image"})['src']

        #Build the post
        toot = "From Packt Publishing:\n" + book_title + " " + book_author + "\n"
        toot = toot + "(" + book_date + ", " + book_pages + "\n\n"
        toot = toot + book_desc + "\n\nGet it at: https://www.packtpub.com/free-learning"

        return toot

    #UNDER CONSTRUCTION - Framer for a random project Gutenburg book
    def gutenburg(book_num):
        #scrape the page, push into BeautifulSoup object
        r = requests.get('https://www.gutenberg.org/ebooks/' + str(book_num))
        soup = BeautifulSoup(r.text, 'html.parser') 

        #Get key post elements

        #Build the post

        return toot

#Logic to actually drive the posting
now = datetime.now()
if hour in ['7','15','23']: #post the Packt free ebook 3 times a day
    prepared_toot = TootFramer.packt()
else: #for now, pull from Project Gutenburg
    #v---UNDER CONSTRUCTION---v
    #prepared_toot = TootFramer.gutenburg(random.randint(1,69500))
    pass

#Now, for the tooting!
mastodon = Mastodon(access_token = 'pytooter_usercred.secret') #create a Mastodon interface object, login
mastodon.toot(prepared_toot) #post toot!
