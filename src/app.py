from flask import Flask, request, render_template, jsonify
from pycaret.regression import load_model, predict_model
from waitress import serve
import pandas as pd
import numpy as np
import sys

"""
USAGE :
# for production
python src/app.py --production

# for development (default)
python src/app.py
"""


app = Flask(__name__)

model = load_model('model/pycaret-model')

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    col = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
    data_unseen = pd.DataFrame([final], columns = col)
    
    prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction['prediction_label'][0])
    return render_template('home.html', pred='The expected bill for this person is ${}.'.format(prediction))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = int(prediction['prediction_label'][0])
    return jsonify(output)


if __name__ == '__main__':
    if '--production' in sys.argv:
        print("Starting production server with Waitress...")
        serve(app, host='0.0.0.0', port=5000, threads=4)
    else:
        print("Starting development server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
  

