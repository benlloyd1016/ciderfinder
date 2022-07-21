import requests
from bs4 import BeautifulSoup
import pandas as pd
from cs50 import SQL

db = SQL("sqlite:///ciders.db")

def scraper():
    # This code was adapted from the walkthrough here: https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/

    # Sets the base url that all scraped links will be appended to
    baseurl = "https://shopciders.com"

    # Declares a variable to be used as the user-agent (otherwise user-agent will be Python by default which might get blocked)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    # Initializes lists and variables
    productlinks = []
    t={}
    data=[]
    c=0

    # Pulls the links for each cider from the main page and assembles them into a list
    for x in range(1): # Need to come back to this and add the correct range (1,50)
        k = requests.get('https://shopciders.com/products?&page={}'.format(x)).text
        soup=BeautifulSoup(k,'html.parser')
        productlist = soup.find_all("h3",{"class":"quarter-bottom"})


        for product in productlist:
            link = product.find("a").get('href')
            productlinks.append(baseurl + link)

    # Accesses each link in the list, pulls the cider name and description, and updates the database
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

        # Checks if this link is already in the database. If so, it updates the existing data. If not, it creates a new row.
        if db.execute("SELECT COUNT(link) FROM ciders WHERE link = ?", link)[0]['COUNT(link)'] == 0:
            db.execute("INSERT INTO ciders (link, name, price, description) VALUES(?, ?, ?, ?)", link, name, price, description)
        else:
            db.execute("UPDATE ciders SET name = ?, price = ?, description = ? WHERE link = ?", name, price, description, link)