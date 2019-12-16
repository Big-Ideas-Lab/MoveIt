#---------------------------------------------------------------------------------------------
                #PART 0: Imports, NLP database load, nutrition tree build
#---------------------------------------------------------------------------------------------

#NEEDS TO BE PRUNED

import os
import json
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
                            #PART 2: Nutrition Scoring
#---------------------------------------------------------------------------------------------

#Function to search ingredients in tree and find closest one in dataframe
#---------------------------------------------------------------------------------------------

#Needs to be updated with V2. 

def nutri_search(string): # string is the ingredient

    row = closest_food(string)
# =============================================================================
#     nutrients = ['nf_calories',
#      'nf_cholesterol',
#      'nf_dietary_fiber',
#      'nf_p',
#      'nf_potassium',
#      'nf_protein',
#      'nf_saturated_fat',
#      'nf_sodium',
#      'nf_sugars',
#      'nf_total_carbohydrate',
#      'nf_total_fat',
#      'nf_total_saturated_fat',
#      'nf_calcium_dv',
#      'nf_mg']
# =============================================================================
    try:
        cal = row['nf_calories']
    except:
        cal = 0
    try:
        sugars = 4*row['nf_sugars']
    except:
        sugars = 0
    try:
        totfat = 9*row['nf_total_fat']
    except:
        totfat = 0
#    try:
#        unsatfat = row['nf_total_fat'] - row['nf_saturated_fat']
#    except:
#        unsatfat = 0
    try:
        satfat = 9*row['nf_saturated_fat']
    except:
        satfat = 0
    # try:
    #     transfat = 0 # need to fix this/elim
    # except:
    #     transfat = 0
    try:
        chol = row['nf_cholesterol']
    except:
        chol = 0
    try:
        carbs = 4*row['nf_total_carbohydrate']
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
    # try:
    #     folate = 0
    # except:
    #     folate = 0
    try:
        potass = row['nf_potassium']
    except:
        potass = 0
#    try:
#        vd = 0
#    except:
#        vd = 0
    try:
        calcium = row['nf_calcium_dv']
    except:
        calcium = 0

    nutri_dict={'cal':cal,'sugars':sugars,'totfat':totfat,'satfat':satfat, 'chol':chol, 'carbs':carbs,'protein':protein,'fiber':fiber,'sod':sod,'mag':mag,'potass':potass,'calcium':calcium} 

    return nutri_dict

#Weight function for different nutrient needs
#---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    nutri_search(sys.argv[1])
