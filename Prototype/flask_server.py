from flask import Flask, request, render_template
import main
import json
import requests
import urllib
import random

from Genetic import functions as f
from Genetic.Genome import Genome
import Genetic.global_variables as gv
import Genetic.sentence_formation as sf
import main

app = Flask(__name__)
json_data = None
input_text = None

@app.route('/')
def simple_page():
    return "Please go to <a href='/knights-and-knaves'> INPUT PAGE</a>"


@app.route('/knights-and-knaves')
def input_page():
    return render_template('index.html')


@app.route('/get-next-question')
def get_next_question():
    random_no = random.randint(3,3)
    while(True):
        try:
            # create boolean quesstion
            g = main.create_boolean_question(population_size=50,
                                            number_of_people=random_no)

            # select random names
            random.shuffle(gv.NAMES)
            names = {a:b for a, b in zip(g.variables, gv.NAMES)}
            
            #generate verbal questio for boolean equation and names selected. 
            i, q = sf.generate_question(g, names, random_no)
            k_or_k = lambda x: "Knight" if x else "Knave"

            print(names)
            print({a:k_or_k(b) for a,b in zip(gv.NAMES, gv.ASSUMED_ANSWER)})
            break
        except:
            print("Error Occured")
            raise

    return json.dumps({"question" : q, "introduction": i})


if __name__ == '__main__':
    app.run(debug=True, port = 5000)
