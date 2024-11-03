from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)

with open("ML_MODEL (1).pkl", "rb") as file:
    model = pickle.load(file)

def make_prediction(data):
    prediction_array = np.array([data])
    prediction = model.predict(prediction_array)
    return int(round(prediction[0]))

@app.route('/')
def landing():
    return render_template('intro.html')

@app.route('/predict-page')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    venue = data['venue']
    batting_team = data['batting_team']
    bowling_team = data['bowling_team']
    runs = data['runs']
    wickets = data['wickets']
    overs = data['overs']
    runs_last_5 = data['runs_last_5']
    wickets_last_5 = data['wickets_last_5']

    input_data = [venue]

    teams = [
        "Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab",
        "Kolkata Knight Riders", "Mumbai Indians", "Rajasthan Royals",
        "Royal Challengers Bangalore", "Sunrisers Hyderabad"
    ]
    for team in teams:
        input_data.append(1 if batting_team == team else 0)
    for team in teams:
        input_data.append(1 if bowling_team == team else 0)

    input_data.extend([runs, wickets, overs, runs_last_5, wickets_last_5])
    predicted_score = make_prediction(input_data)

    return jsonify({"predicted_score": f"would lie between {predicted_score-10} and {predicted_score + 10}"})

if __name__ == '__main__':
    app.run(debug=True)
