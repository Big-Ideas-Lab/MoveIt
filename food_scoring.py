#---------------------------------------------------------------------------------------------
            #PART 3: Score local meals ### NEEDS TO BE UPDATED FOR FIREBASE.
#---------------------------------------------------------------------------------------------
#NEEDS TO BE PRUNED

import os
import requests
import urllib.request as urllib2
import re
import googlemaps as gmap
import json
import gensim
import pandas as pd
import numpy as np
from scipy import spatial
import sys
#from nutrition import nutri_search

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


def score_local_meals_per_user(radius,lat,long,gender,activity,age):
    #Collect options in the area.
    
    #bring in JSON data herea / connect to FIREBASE here.

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
    
if __name__ == "__main__":
    score_local_meals_per_user(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))