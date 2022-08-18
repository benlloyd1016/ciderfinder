import requests
from bs4 import BeautifulSoup
from cs50 import SQL

db = SQL("sqlite:///ciders.db")

def scraper():
    # This code was adapted from the walkthrough here: https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/
    baseurl = "https://shopciders.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'} # Declares a variable to be used as the user-agent (otherwise user-agent will be Python by default which might get blocked)
    productlinks = []

    # Pulls the links for each cider from the main page and assembles them into a list
    for x in range(1,50): # Need to come back to this and add the correct range (1,50)
        k = requests.get('https://shopciders.com/products?&page={}'.format(x)).text
        soup=BeautifulSoup(k,'html.parser')
        productlist = soup.find_all("h3",{"class":"quarter-bottom"})

        for product in productlist:
            link = product.find("a").get('href')
            productlinks.append(baseurl + link)

    # Accesses each link in the list, pulls the cider data, and updates the database
    for link in productlinks:
        f = requests.get(link,headers=headers).text
        hun=BeautifulSoup(f,'html.parser')

        # Gets name
        try:
            name=hun.find("h2").text.replace('\n',"")
        except:
            name=None

        # Gets price
        try:
            price=hun.find("div",{"class":"hero-3 product-price"}).text.replace('\t',"").replace('\n',"")
        except:
            price=None

        # Gets description
        try:
            description=hun.find("div",{"class":"product-description"}).text.replace('\t',"").replace('\n',"")
        except:
            description=None

        # Gets picture
        try:
            image_link_basic=hun.find("img",{"class":"img-responsive center-block"},{"src":True})
            image_link=image_link_basic['src']
            image=("https:" + image_link)
        except:
            image_link_basic=None

        # Updates the database
        update_db(link, name, price, description, image)

def update_db(link, name, price, description, image):

    # If this URL is not already in the database, it creates a new row for the data.
    if db.execute("SELECT COUNT(link) FROM ciders WHERE link = ?", link)[0]['COUNT(link)'] == 0:
        db.execute("INSERT INTO ciders (link, name, price, description, image) VALUES(?, ?, ?, ?, ?)", link, name, price, description, image)
    
    # If the URL is already in the database, it updates the existing row containing this URL.
    else:
        db.execute("UPDATE ciders SET name = ?, price = ?, description = ?, image = ? WHERE link = ?", name, price, description, image, link)