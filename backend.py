#---------------------------------------------------------------------------------------------
                #PART 0: Imports, NLP database load, nutrition tree build
#---------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
import os
import requests
import urllib.request as urllib2
import re
import googlemaps as gmap
import json
from geopy.geocoders import Nominatim
import gensim
import pandas as pd
import numpy as np
from scipy import spatial
import sys

sys.setrecursionlimit(3000)

print("Loading NLP Model...")
#---------------------------------------------------------------------------------------------
#importing the nlp model
nlp_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/joshuadarcy/Desktop/GoogleNews-vectors-negative300.bin', binary = True)
print("NLP Model Loaded")


#function to read nutritional database csv, word2vec for each item, convert vectors to searchable tree
#---------------------------------------------------------------------------------------------

def word2vec_func(string):
    word_array = string.split()
    single_vector = np.zeros(300)
    for word in word_array:
        try:
            single_vector += nlp_model.get_vector(word)
        except:
            continue
    return single_vector

print("Building Tree...")
df = pd.read_csv('/Users/joshuadarcy/Desktop/foods.csv')
df['vector'] = df.apply(lambda x: word2vec_func(x['food_name']),axis=1)
nump_array = np.array(df['vector'])
concat = np.concatenate(nump_array)
reshaped = concat.reshape(-1,300)
tree = spatial.KDTree(reshaped)
print("Tree built.")

#---------------------------------------------------------------------------------------------
     #PART 1: Find local restaurants, compare to AllMenus.com, construct food dataset
#---------------------------------------------------------------------------------------------



#setup Google search API, default type = 'restaurant' but can use other queries
#---------------------------------------------------------------------------------------------

class google_api_search(object):

    def search_parse(self, lat, lng):
        location = (lat, lng)
        # Query google places api
        goog = gmap.Client(key=self.api_key)
        geocode_result = goog.places(query=self.query, location=location, radius=self.radius, type = 'restuarant')

        goog.places
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


#function to help the "About Grubhub" web scraping issue
#---------------------------------------------------------------------------------------------

def sort_header(bea_soup):
    all_headers = bea_soup.find_all('h1')
    for header in all_headers:
        text = header.get_text()
        if 'Grub' in text:
            continue
        else:
            return text

#Collect restaurant -- currently Durham, need to expand progammatically with allmenus
#---------------------------------------------------------------------------------------------
def collect_durham(rad,lat,long):

    # testing difference radii, questions about how to get more restaurants
    set1 = set(google_api_search(query='restaurant|dining', radius=rad).search_parse(lat, long))

    # find the union of all the sets (a set will inherently get rid of multiples)
    source_list = set1

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

    URL_base2 = "https://www.allmenus.com/nc/durham/"

    # where all the data is stored for the JSON
    restaurants = []

    for id, location_goog in zip(links_used, locations_used):
        URL = URL_base2 + id
        r = requests.get(URL)
        bsObj = BeautifulSoup(r.content, 'html.parser')

        #Function to parse out any mention of Grubhub
        restaurant = sort_header(bsObj)

        #Check for chains, skip if chain present
        if any (restp['Name'] == restaurant for restp in restaurants):
            continue

        location = location_goog
        name = restaurant
        titles = bsObj.find_all("span", attrs={'class': 'item-title'})
        ingredients = bsObj.find_all("p", attrs={'class': 'description'})

        prices = bsObj.find_all("span", attrs={'class': 'item-price'})


        # where all the menu items are held with the format above
        # use regex to clean up the ingredients, will have to continue adding to this dictionary

        remove = {',': '', '.': '', ':':''}
        pattern = '|'.join(sorted(re.escape(k) for k in remove))

        #cleaning/processing of ingredients by menu item
        #create array of menu items

        menu = []
        for item, price, ingredient in zip(titles, prices, ingredients):

            menu_item = {
            "item": "",
            "price": "",
            "ingredients": []
            }

            #menu name
            menu_item["item"] = item.get_text()

            #menu price
            stripped_price = price.get_text()
            stripped_price = stripped_price.strip(' \t\n')
            menu_item["price"] = stripped_price
            clean_ingredient = str(ingredient.get_text())


            clean_ingredient = re.sub(pattern, lambda m: remove.get(m.group(0).upper()), clean_ingredient, flags=re.IGNORECASE)
            current_ingredient = re.split("[\s,\&]", clean_ingredient)

            if len(current_ingredient) == 1:
                current_ingredient = re.split("[\s,\&]", menu_item["item"])

            final_ingredient = []

            #NLP to find food
            for word in current_ingredient:
                try:
                    if nlp_model.similarity('edible', word) > .1 and nlp_model.similarity('food', word) > .15:
                        final_ingredient.append(word)
                except:
                    continue

            menu_item['ingredients'] = final_ingredient

            menu.append(menu_item)

        data = {
            "Name": name,
            "Location": location,
            "Menu": menu
        }
        restaurants.append(data)

    return restaurants
#---------------------------------------------------------------------------------------------
                            #PART 2: Nutrition Scoring
#---------------------------------------------------------------------------------------------


#Function to search ingredients in tree and find closest one in dataframe
#---------------------------------------------------------------------------------------------
def nutri_search(string,df):
    word_array = string.split()
    single_vector = np.zeros(300)

    for word in word_array:
        try:
            single_vector += nlp_model.get_vector(word)
        except:
            continue
    nutrients = ['nf_calories',
     'nf_cholesterol',
     'nf_dietary_fiber',
     'nf_p',
     'nf_potassium',
     'nf_protein',
     'nf_saturated_fat',
     'nf_sodium',
     'nf_sugars',
     'nf_total_carbohydrate',
     'nf_total_fat',
     'nf_total_saturated_fat',
     'nf_calcium_dv',
     'nf_mg']

    metric, location = tree.query(single_vector)
    row = df.iloc[location]

    try:
        cal = row['nf_calories']
    except:
        cal = 0
    try:
        sugars = row['nf_sugars']
    except:
        sugars = 0
    try:
        totfat = row['nf_total_fat']
    except:
        totfat = 0
    try:
        unsatfat = row['nf_total_fat'] - row['nf_saturated_fat']
    except:
        unsatfat = 0
    try:
        satfat = row['nf_saturated_fat']
    except:
        satfat = 0
    try:
        transfat = row['nf_total_fat'] - row['nf_saturated_fat']
    except:
        transfat = 0
    try:
        carbs = row['nf_total_carbohydrate']
    except:
        carbs = 0
    try:
        protein = row['nf_protein']
    except:
        protein = 0
    try:
        fiber = row['nf_dietary_fiber']
    except:
        fiber = 0
    try:
        sod = row['nf_sodium']
    except:
        sod = 0
    try:
        mag = row['nf_mg']
    except:
        mag = 0
    try:
        folate = 0
    except:
        folate = 0
    try:
        potass = row['nf_potassium']
    except:
        potass = 0
    try:
        vd = 0
    except:
        vd = 0

    nutri_dict={'cal':cal,'sugars':sugars,'totfat':totfat,'unsatfat':unsatfat,'satfat':satfat,'transfat':transfat,'carbs':carbs,'protein':protein,'fiber':fiber,'sod':sod,'mag':mag,'totfolate':folate,'potass':potass,'vd':vd}

    return nutri_dict

#Weight function for different nutrient needs
#---------------------------------------------------------------------------------------------

def weight(recDict):
    switcher = {
    'cal': (2,3),
    'sugars': (1,3),
    'totfat': (1,3),
    'unsatfat': (2,2),
    'satfat': (1,3),
    'transfat': (1,3),
    'carbs': (2,3),
    'protein': (2,3),
    'fiber': (3,1),
    'sod': (1,3),
    'mag': (2,1),
    'totfolate': (2,1),
    'potass': (2,1),
    'vd': (2,1),
    }
    weight_adequacy = {} #{'nutrient': weight_value, etc}
    weight_moderation = {}
    for nutrient in recDict:
        weight_adequacy[nutrient], weight_moderation[nutrient] = switcher[nutrient]
    return weight_adequacy, weight_moderation


#Return dictionary of nutrient values per ingredient per food item
#---------------------------------------------------------------------------------------------

def single_dictionary(menu_item):
    ingredients_list = menu_item['ingredients']
    #create new dict
    menu_item['nutrition'] = {}
    for ingredient in ingredients_list:
        try:
            menu_item['nutrition'][ingredient] = nutri_search(ingredient,df)
        except:
            continue
    return menu_item

#Score menu item
#---------------------------------------------------------------------------------------------
def nutrientScore(nutrition_info, recommended_dict_i):
    recDict = recommended_dict_i
    nutrient_sum_dict={'cal':0,'sugars':0,'totfat':0,'unsatfat':0,'satfat':0,'transfat':0,'carbs':0,'protein':0,'fiber':0,'sod':0,'mag':0,'totfolate':0,'potass':0,'vd':0}
    nutrient_fracs={}
    for ingredient_key in nutrition_info:
        nutrition_dict_for_ingredient = nutrition_info[ingredient_key]
        for nutrient in nutrition_dict_for_ingredient:
            ingredient_nutrient_value = nutrition_dict_for_ingredient[nutrient]
            nutrient_sum_dict[nutrient] = nutrient_sum_dict[nutrient]+ingredient_nutrient_value

    for nutrient in nutrient_sum_dict:
        goal = recDict[nutrient]
        actual = nutrient_sum_dict[nutrient]
        frac = actual/goal
        nutrient_fracs[nutrient] = frac

    # select weights for each adequacy and moderation for each nutrient
    weight_adequacy, weight_moderation = weight(recDict)

    # Scoring
    nutrient_scores_adequacy= {}
    nutrient_scores_moderation = {}
    for nutrient in nutrient_fracs:
        if nutrient_fracs[nutrient] >= 2 :
            nutrient_scores_adequacy[nutrient] = 3* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = -3* weight_moderation[nutrient]
        if nutrient_fracs[nutrient] >= 1.25 and nutrient_fracs[nutrient] <2:
            nutrient_scores_adequacy[nutrient] = 2* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = -2* weight_moderation[nutrient]
        if nutrient_fracs[nutrient] >= 1 and nutrient_fracs[nutrient] <1.25:
            nutrient_scores_adequacy[nutrient] = 1* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = -1* weight_moderation[nutrient]
        if nutrient_fracs[nutrient] >= .75 and nutrient_fracs[nutrient] <1:
            nutrient_scores_adequacy[nutrient] = -1* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = 1* weight_moderation[nutrient]
        if nutrient_fracs[nutrient] >= .5 and nutrient_fracs[nutrient] <.75:
            nutrient_scores_adequacy[nutrient] = -2* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = 2* weight_moderation[nutrient]
        if nutrient_fracs[nutrient] >= 0 and nutrient_fracs[nutrient] <.5:
            nutrient_scores_adequacy[nutrient] = -3* weight_adequacy[nutrient]
            nutrient_scores_moderation[nutrient] = 3* weight_moderation[nutrient]
    adequacy = sum(nutrient_scores_adequacy.values())
    moderation = sum(nutrient_scores_moderation.values())
    score = adequacy + moderation # a more positive score is better

    return score

# Generate the recommended nutritional intake depending on gender and activity
#---------------------------------------------------------------------------------------------

def recommended_dict(gender, activity, age):
    if gender == 0:
        if activity == 0:
            if  age >=16 and age <=18:
                cals = 2400;percent_totfat = .3;protein = 52;fiber = 30.8
            elif age >=19 and age <=20:
                cals = 2600;percent_totfat = .275;protein = 56;fiber = 33.6
            elif age >=21 and age <=30:
                cals = 2400;percent_totfat = .275;protein = 56;fiber = 33.6
            elif  age >=31 and age <=40:
                cals = 2400;protein = 56;percent_totfat = .275;fiber = 30.8
            elif  age >=41 and age <=50:
                cals = 2200;percent_totfat = .275;protein = 56;fiber = 30.8
            elif  age >=51 and age <=60:
                cals = 2200;percent_totfat = .275;protein = 56;fiber = 28
            elif  age >=61:
                cals = 2000;percent_totfat = .275;protein = 56;fiber = 28
        elif activity == 1:
            if  age >=16 and age <=25:
                cals = 2800;percent_totfat = .3;protein = 52
                if age >=16 and age <= 18:
                    fiber = 30.8
                elif age >=19 and age <= 25:
                    fiber = 33.6
            elif age >=26 and age <=45:
                cals = 2600;percent_totfat = .275;protein = 56
                if age >= 26 and age <=30:
                    fiber = 33.6
                elif age >= 31 and age <= 45:
                    fiber = 30.8
            elif age >=46 and age <= 65:
                cals = 2400;percent_totfat = .275;protein = 56
                if age >= 46 and age <= 50:
                    fiber = 30.8
                elif age >=51:
                    fiber = 28
            elif age >=66:
                cals = 2200;percent_totfat = .275;protein = 56
        elif activity == 2:
            if  age >=16 and age <=18:
                cals = 3200;percent_totfat = .3;protein = 52;fiber = 30.8
            elif  age >=19 and age <=35:
                cals = 3000;percent_totfat = .275;protein = 56
                if age >= 19 and age <= 30:
                    fiber = 33.6
                elif age >= 31 and age >= 35:
                    fiber = 30.8
            elif  age >=36 and age <=55:
                cals = 2800;percent_totfat = .275;protein = 56
                if age >= 36 and age <= 50:
                    fiber = 30.8
                elif age >=51 and age <= 55:
                    fiber = 28
            elif  age >=56 and age <=75:
                cals = 2600;percent_totfat = .275;protein = 56;fiber = 28
            elif age >= 76:
                cals = 2400;percent_totfat = .275;protein = 56;fiber = 28

        recommended_dict = {'cal':cals/3,'sugars':.09*cals/3,'totfat': percent_totfat*cals/3,'unsattfat':.6*percent_totfat*cals/3,'satfat':.09*cals/3,'transfat':.01*cals/3,'carbs':130/3,'protein':56/3,'fiber':fiber/3,'sod':2300/3,'mag':420/3,'totfolate':400/3,'potass':4700/3,'vd':600/3}

    elif gender == 1:
        if activity == 0:
            if age >=16 and age <=18:
                cals = 1800;percent_totfat = .3;fiber = 25.2
            elif  age >=19 and age <=25:
                cals = 2000;percent_totfat = .275;fiber = 28
            elif  age >=26 and age <=50:
                cals = 1800;percent_totfat = .275
                if age >= 26 and age <=30:
                    fiber = 28
                elif age >30 and age <=50:
                    fiber = 25.2
            elif  age >=51:
                cals = 1600;percent_totfat = .275;fiber = 22.4
        elif activity == 1:
            if age >=16 and age <=18:
                cals = 2000;percent_totfat = .3;fiber = 25.2
            elif  age >=19 and age <=25:
                cals = 2500;percent_totfat = .275;fiber = 28
            elif  age >=26 and age <=50:
                cals = 2000;percent_totfat = .275
                if age >= 26 and age <=30:
                    fiber = 28
                elif age >30 and age <=50:
                    fiber = 25.2
            elif  age >=51:
                cals = 1800;percent_totfat = .275;fiber = 22.4
        elif activity == 2:
            if age >=16 and age <=30:
                cals = 2400;percent_totfat = .275
                if age >=16 and age <=18:
                    fiber = 25.2
                elif age >18 and age <=25:
                    fiber = 28
                elif age >= 26 and age <=30:
                    fiber = 28
            elif age >30 and age <=60:
                cals = 2200;percent_totfat = .275
                if age >30 and age <=50:
                    fiber = 25.2
                elif age> 50:
                    fiber = 22.4
            elif age>60:
                cals = 2000;percent_totfat = .275;fiber = 22.4

        recommended_dict = {'cal':cals/3,'sugars':.09*cals/3,'totfat': percent_totfat*cals/3,'unsatfat':.6*percent_totfat*cals/3,'satfat':.09*cals/3,'transfat':.01*cals/3,'carbs':130/3,'protein':46/3,'fiber':fiber/3,'sod':2300/3,'mag':320/3,'totfolate':400/3,'potass':4700/3,'vd':600/3}

    else:
        recommended_dict = {'cal':2400/3,'sugars':.09*2400/3,'totfat': .275*2400/3,'unsatfat':.6*.275*2400/3,'satfat':.09*2400/3,'transfat':.01*2400/3,'carbs':130/3,'protein':46/3,'fiber':25.2/3,'sod':2300/3,'mag':320/3,'totfolate':400/3,'potass':4700/3,'vd':600/3}
    return recommended_dict

#---------------------------------------------------------------------------------------------
            #PART 3: Putting it all together, currently only taking 5 menu items each
#---------------------------------------------------------------------------------------------


def score_local_meals_per_user(radius,lat,long,gender,activity,age):
    #Collect options in the area.
    restaurants = collect_durham(radius,lat,long)
    print("Restaurants Collected.")
    #Optimal recommended dictionary construction, will need to move this outside function in future

    recommended_dictionary = recommended_dict(gender=gender,activity=activity,age=age)

    #Add in nutritional values for each item in dictionary
    for restaurant in restaurants:
        menu = restaurant['Menu']
        counter = 0
        for item in menu:
            menu[counter]['Score'] = nutrientScore(single_dictionary(item)['nutrition'],recommended_dictionary)
            counter +=1

            if counter == 5:
                print("Nutritional information obtained from {}.".format(restaurant['Name']))
                break

    for restaurant in restaurants:
        menu = restaurant['Menu']
        counter = 0
        for item in menu:
            try:
                print('Restaurant: {} ({})\nItem: {}\nScore: {}'.format(restaurant['Name'],restaurant['Location'],item['item'], item['Score']))
            except:
                continue

if __name__ == "__main__":
    score_local_meals_per_user(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
