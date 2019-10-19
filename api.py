from flask import Flask
import numpy as np
import gensim
import sys

app = Flask(__name__)

sys.setrecursionlimit(3000)
print("Loading NLP Model...")

nlp_model = gensim.models.KeyedVectors.load_word2vec_format('/Users/christinalle/Desktop/GoogleNews-vectors-negative300.bin.gz', binary = True)

print("NLP Model Loaded")

@app.route('/get/<string>')
def word2vec_func(string):
    word_array = string.split()
    single_vector = np.zeros(300)
    for word in word_array:
        try:
            single_vector += nlp_model.get_vector(word)
        except:
            continue
    return single_vector

@app.route('/get/<word>')
def find_food_sim(word):
    if nlp_model.similarity('edible', word) > .1 and nlp_model.similarity('food', word) > .15:
        return True
    else:
        return False

@app.route('/get/<word>')
def get_vec(word):
    return nlp_model.get_vector(word)

if __name__ == '__main__':
    app.run(debug=True)