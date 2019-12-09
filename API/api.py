from flask import Flask
import numpy as np
import gensim
import sys

app = Flask(__name__)

# loading model needs to be its own method?
sys.setrecursionlimit(3000)
print("Loading NLP Model...")
 
nlp_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/christinalle/Desktop/GoogleNews-vectors-negative300.bin.gz', binary = True)

print("NLP Model Loaded")

# methods for getting string responses for debugging
@app.route('/get/testword2vec/<string>')
def word2vec_func_s(string):
    word_array = string.split()
    single_vector = np.zeros(300)
    for word in word_array:
        try:
            single_vector += nlp_model.get_vector(word)
        except:
            continue
    return str(single_vector)
        # ''.join(single_vector)

@app.route('/get/testfindfoodsim/<word>')
def find_food_sim_s(word):
    if nlp_model.similarity('edible', word) > .1 and nlp_model.similarity('food', word) > .15:
        return 'true'
    else:
        return 'false'

# methods for getting expected type responses for debugging
@app.route('/get/word2vec/<string>')
def word2vec_func(string):
    word_array = string.split()
    single_vector = np.zeros(300)
    for word in word_array:
        try:
            single_vector += nlp_model.get_vector(word)
        except:
            continue
    return single_vector

@app.route('/get/findfoodsim/<word>')
def find_food_sim(word):
    if nlp_model.similarity('edible', word) > .1 and nlp_model.similarity('food', word) > .15:
        return True
    else:
        return False

# if this method is uncommented, the API will not work, could possibly be because the route is not defined
# @app.route('/get/<word>')
# def get_vec(word):
#     return nlp_model.get_vector(word)

if __name__ == '__main__':
    app.run(debug=True)