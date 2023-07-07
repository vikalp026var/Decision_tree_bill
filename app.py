from flask import Flask, render_template, request
from flask import Response
import numpy as np 
import pymongo
import pickle

app = Flask(__name__)

model = pickle.load(open('tree.pkl','rb'))

uri = "mongodb+srv://vikalp026varshney:vikalp026var@cluster0.r31hq0n.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client['Decision_tree']
collections = db['collections']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        Variance = float(request.form.get('Variance'))
        Skewness = float(request.form.get('Skewness'))
        Curtosis = float(request.form.get('Curtosis'))
        Entropy = float(request.form.get('Entropy'))

        result = model.predict([[Variance, Skewness, Curtosis, Entropy]])

        collections.insert_many([
            {
                'Variance': Variance,
                'Skewness': Skewness,
                'Curtosis': Curtosis,
                'Entropy': Entropy,
                'result': int(result[0])
            }
        ])

        return render_template('index.html', result=result[0])

    return render_template('index.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0")
