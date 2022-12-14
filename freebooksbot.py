import requests, random, io
from bs4 import BeautifulSoup
from datetime import datetime
from mastodon import Mastodon

#Application variables
application_name = "freebooksbot"
secret_loc = "freebooksbot_usercred.secret"
server_api_link = "https://botsin.space/api/v2/media"

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

        return [toot,book_cover]

    #Framer for a random project Gutenburg book
    def gutenburg(book_num):
        #scrape the page, push into BeautifulSoup object
        r = requests.get('https://www.gutenberg.org/ebooks/' + str(book_num))
        soup = BeautifulSoup(r.text, 'html.parser') 

        #Get key post elements
        book_title = soup.find("title").text.split(" - ")[0]
        book_cover = soup.find("img",{"class":"cover-art"})['src']

        #Build the post
        toot = "From Project Gutenberg:\n" + book_title + "\n"
        toot = toot + "\n\nGet it at: https://www.gutenberg.org/ebooks/" + str(book_num)

        return [toot,book_cover]

#Logic to actually drive the posting
now = datetime.now()
if now.hour in ['7','15','23']: #post the Packt free ebook 3 times a day
    [prepared_toot,media_link] = TootFramer.packt()
else: #for now, pull from Project Gutenburg the rest of the time
    [prepared_toot,media_link] = TootFramer.gutenburg(random.randint(1,69500))

#Now, for the tooting!
mastodon = Mastodon(access_token = secret_loc) #create a Mastodon interface object, login
media_id = TootFramer.upload_image_from_link(media_link, secret_loc,application_name,server_api_link)
mastodon.status_post(prepared_toot,media_ids=media_id) #post toot!
