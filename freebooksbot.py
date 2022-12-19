#!/usr/bin/python3
import requests, random, io, os, sys
from bs4 import BeautifulSoup
from datetime import datetime
from mastodon import Mastodon

#Application variables
application_name = "freebooksbot"
secret_loc = "freebooksbot_usercred.secret" #credentials for api interfacing with server
server_api_link = "https://botsin.space/api/v2/media" #api link for media uploads only!

#Class to pull the information from sources and frame into toots
class TootFramer():

    #Upload book cover to server, return media id
    def upload_image_from_link(media_link, auth_file, application_name, server_api_link):
        with open(auth_file) as f: authorization_token = f.readline()[:-1] #get auth token for posting
        #build the request
        headers = {"Authorization": "Bearer " + authorization_token, "User-Agent":application_name}
        img = requests.get(media_link) #get the image file as multi-part file
        body = {"file":io.BytesIO(img.content)} #append that multi-part file to upload request
        data = {'upload': ''}
        #now, make the request
        metadata = requests.post(server_api_link, data=data, headers=headers, files=body)
        return metadata.json()["id"]

    #Framer for the daily Packt Free Ebook
    def packt():
        #scrape the page, push into BeautifulSoup object
        r = requests.get('https://www.packtpub.com/free-learning')
        soup = BeautifulSoup(r.text, 'html.parser')

        #Get key post elements
        book_title = soup.find("h3", {"class":"product-info__title"}).text.split(" - ")[1]
        book_author = soup.find("span", {"class":"product-info__author"}).text
        book_date = soup.find("div", {"class":"free_learning__product_pages_date"}).text.lstrip().rstrip()
        book_pages = soup.find("div", {"class":"free_learning__product_pages"}).text.lstrip().rstrip()
        book_desc = soup.find("div",{"class":"free_learning__product_description"}).text
        book_cover = soup.find("img",{"class":"product-image"})['src']

        #Build the post
        toot = "From Packt Publishing:\n" + book_title + " " + book_author + "\n"
        toot = toot + "(" + book_date + ", " + book_pages + ")\n\n"
        toot = toot + book_desc + "\n\nGet it at: https://www.packtpub.com/free-learning"

        return [toot,book_cover]

    #Framer for a random project Gutenberg book
    def gutenburg():
        #select a random book id from within the range of the Gutenberg project
        book_num = random.randint(1,69500)
        print(book_num)

        #scrape the page, push into BeautifulSoup object
        r = requests.get('https://www.gutenberg.org/ebooks/' + str(book_num))
        soup = BeautifulSoup(r.text, 'html.parser') 

        #Get key post elements
        book_title = soup.find("td",{"itemprop":"headline"}).text
        book_author_raw = soup.find("a",{"itemprop":"creator"}).text
        if len(book_author_raw.split(", ")) > 1: #if an author has multiple parts to their name
            [author_last, author_first] = [book_author_raw.split(", ")[0],book_author_raw.split(", ")[1]]
            if author_first.find("-") > -1: #possible one-named author with a date detected
                if author_first.split("-")[0].isnumeric(): #yep, it's a date - just go with "last name"
                    book_author = author_last
                else: #false alarm - hyphenated last name
                    book_author = author_first + " " + author_last
            else: #Two names, hypen free
                book_author = author_first + " " + author_last  #reorder to firstname lastname
        else: #if just one author, no date
            book_author = book_author_raw
        book_cover = soup.find("img",{"class":"cover-art"})['src']

        #Build the post
        toot = "From Project Gutenberg:\n" + book_title + "\nby " + book_author + "\n"
        toot = toot + "\n\nGet it at: https://www.gutenberg.org/ebooks/" + str(book_num)

        return [toot,book_cover]

    #framer for resources from oercommons.org
    def oercommons():
        #a couple of levels to this:
        #first, select a book topic from the set of reference numbers.
        #Then, get the number of books for the topic, pick a random book.
        #Update the selected page to be able to get the link to that book
        #Then go to the book page and scrape the data for the link.

        book_topic = random.randint(801,812) #get the topic number


#Logic to actually drive the posting
now = datetime.now()
if now.hour in [7,15,23]: #post the Packt free ebook 3 times a day
    [prepared_toot,media_link] = TootFramer.packt()
else: #for now, pull from Project Gutenburg the rest of the time
    [prepared_toot,media_link] = TootFramer.gutenburg()

#Now, for the tooting!
secret = os.path.join(sys.path[0], secret_loc) #get full path for the secrets file (in same dir as this script)
mastodon = Mastodon(access_token = secret) #create a Mastodon interface object, login
media_id = TootFramer.upload_image_from_link(media_link,secret,application_name,server_api_link) #upload the image associated with the post
mastodon.status_post(prepared_toot,media_ids=media_id) #post toot!
