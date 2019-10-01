from flask import Flask, render_template, request
app = Flask(__name__)
from bs4 import BeautifulSoup
import os
import requests
import urllib.request as urllib2
import re
import googlemaps as gmap
import json
# import numpy as np
from geopy.geocoders import Nominatim

import gensim


# from nltk.corpus import wordnet as wn
# >>> food = wn.synset('food.n.02')
# >>> list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

class google_api_search(object):

    def search_parse(self, lat, lng):
        location = (lat, lng)
        # Query google places api
        goog = gmap.Client(key=self.api_key)
        geocode_result = goog.places(query=self.query, location=location, radius=self.radius)

        # Collect results
        results = geocode_result['results']

        # Clean JSON and create list
        geo_list = []
        for result in results:
            name = result['name'].lower()
            latitude = result['geometry']['location']['lat']
            longitude = result['geometry']['location']['lng']
            geo_list.append((name, (latitude, longitude)))

        return geo_list

    def __init__(self, query='restaurant', radius=1000):
        # set parameters
        self.radius = radius
        self.api_key = 'AIzaSyDzs7Yezb7ZUCCajqPY0yjRR4LBUkA2Ugw'
        self.query = query
        # run search parse and create an instance variable called geo_list that you can reference
        # self.geo_list = self.search_parse(35.9940, -78.8986)

# testing difference radii, questions about how to get more restaurants
set1 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.9940, -78.8986))
set2 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(36.002, -78.9148))
set3 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(36.01699, -78.90912))
set4 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.900664, -78.894297))
set5 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.954672, -78.995010))
set6 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.904437, -78.942995))
set7 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.878584, -78.848129))
set8 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(36.076245, -78.910215))
set9 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.993081, -78.868973))
set10 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.924819,-78.844015))
set11 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.949501,-78.923388))
set12 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.909337,-78.986132))
set13 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(36.057837,-78.929465))
set14 = set(google_api_search(query='restaurant|food|dining', radius=500).search_parse(35.862324,-78.818222))

# find the union of all the sets (a set will inherently get rid of multiples)
source_list = set1 | set2 | set3 | set4 | set5 | set6 | set7 | set8 | set9 | set10 | set11 | set12 | set13 | set14
print(source_list)
print(len(source_list))

# split the geo_list into two separate arrays, one for purely names and one for locations
names, locations = zip(*source_list)
map_locations = dict(zip(names, locations))

# WEB SCRAPING

# starting link for allmenus, call BeautifulSoup
URL_base = "https://www.allmenus.com/nc/durham/-/"
page = urllib2.urlopen(URL_base)
soup = BeautifulSoup(page, "html.parser")
all_possible_links = soup.findAll("a", {"data-masterlist-id": re.compile(r".*")})

# all the correct, cleaned links gotten from BeautifulSoup
links = []

# list of restaurant names obtained from the links
master_list = []

# FINAL list of restaurants used found based on the intersection of master_list and names from above
links_used = []
locations_used = []
names_used = []

# the list of restaurants that overlap with google places, hard-coded currently WILL HAVE TO FIND MORE EFFICIENT METHOD

# used to traverse all the possibilities on allmenus and find out what matches google places results
for link in all_possible_links:
    if link.has_attr('href'):
        raw_href = link.attrs['href']
        wanted_href = raw_href.replace("/nc/durham/", "")
        turn_string = str(wanted_href)
        find = str(re.search("(?<=-).*", turn_string).group())
        find = find.replace('/menu/', '')
        find = find.replace('-', ' ')
        find = find.replace(' s', '\'s')
        master_list.append(find)
        links.append(wanted_href)

        if find in names:
            links_used.append(wanted_href)
            locations_used.append(map_locations.get(find))
            names_used.append(find)

# find the intersection of the lists
master_list_set = set(master_list)
final_list = master_list_set.intersection(names)
print(final_list)
print(len(final_list))
print(len(links_used))
# print(links)

URL_base2 = "https://www.allmenus.com/nc/durham/"

# where all the data is stored for the JSON
restaurants = []

chains = {"mcdonald's", "chipotle", "burger king", "arby's", "waffle house", "mellow mushroom", "taco bell", "hardee's", "pizza hut", "church's chicken", "wendy's", "cook out", "papa john's pizza"}

#importing the model

nlp_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/christinalle/Desktop/GoogleNews-vectors-negative300.bin.gz', binary = True)

for id, location_goog in zip(links_used, locations_used):
    URL = URL_base2 + id
    r = requests.get(URL)
    bsObj = BeautifulSoup(r.content, 'html5lib')

    restaurant = bsObj.find("h1").get_text()
    # restaurant = name
    if restaurant in chains:
        address = bsObj.find("a", attrs={'class': 'menu-address'})
        geolocator = Nominatim(user_agent="MoveIt")
        location = geolocator.geocode(address.get_text())
        location = (location.latitude, location.longitude)
    else:
        location = location_goog
    name = restaurant
    titles = bsObj.find_all("span", attrs={'class': 'item-title'})
    ingredients = bsObj.find_all("p", attrs={'class': 'description'})

    prices = bsObj.find_all("span", attrs={'class': 'item-price'})

    menu_item = {
        "item": "",
        "price": "",
        "ingredients": []
    }

    # where all the menu items are held with the format above
    menu = []

    # use regex to clean up the ingredients, will have to continue adding to this dictionary
    # remove = {' or': ',', ' and': ',', ' with': ',', 'With ': ',', "touch of ": '', 'own ': '',
    #           'our ': '', 'Our ': '', '.': ''}
    remove = {',': '', '.': '', ':':''}
    pattern = '|'.join(sorted(re.escape(k) for k in remove))

    # cleaning/processing of ingredients by menu item
    final_ingredient = []
    for item, price, ingredient in zip(titles, prices, ingredients):
        menu_item["item"] = item.get_text()
        stripped_price = price.get_text()
        stripped_price = stripped_price.strip(' \t\n')
        menu_item["price"] = stripped_price
        clean_ingredient = str(ingredient.get_text())
        # clean_ingredient = clean_ingredient.strip()
        # print(clean_ingredient)

        clean_ingredient = re.sub(pattern, lambda m: remove.get(m.group(0).upper()), clean_ingredient, flags=re.IGNORECASE)
        current_ingredient = re.split("[\s,\&]", clean_ingredient)

        if len(current_ingredient) == 1:
            # current_ingredient = re.split("[,\&]", menu_item["item"])
            current_ingredient[0] = menu_item["item"]

        # FOR JOSHUA, IMPLEMENTING THE MODEL
        for word in current_ingredient:
            if nlp_model.similarity('edible', word) > .1 and nlp_model.similarity('food', word) > .15:
                final_ingredient.append(word)

        menu_item["ingredient"] = final_ingredient
        # if there are no ingredients, put the menu item name as the default

        menu.append(menu_item.copy())

        data = {
            "Name": name,
            "Location": location,
            "Menu": menu
        }
        restaurants.append(data.copy())

with open("restaurants.json", "w") as writeJSON:
    json.dump(restaurants, writeJSON, ensure_ascii=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)