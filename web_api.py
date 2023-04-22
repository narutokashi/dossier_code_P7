import pandas as pd
import pickle, joblib
import numpy as np
from flask import Flask, jsonify, render_template, request, session


model = joblib.load("trained_ppl.pkl")

# Load the dataset from CSV file
df = pd.read_csv('data_api.csv')

# Define the Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the client ID from the HTML form
    client_id = int(request.form['client_id'])

    # Check if the client ID is in the dataset
    if client_id not in df['SK_ID_CURR'].values:
        return render_template('index1.html',
                               prediction_text='Client ID not found in the dataset')

    # Get the corresponding row from the test data
    row = df[df['SK_ID_CURR'] == client_id].iloc[:, 1:]


    # Make the prediction
    proba = model.predict_proba(row)[0][1]
    pred = model.predict(row)[0]

    # Set the loan status based on the predicted value
    if pred < 0.5:
        loan_status = 'Accepted'
    else:
        loan_status = 'Rejected'

    # Format the output
    prediction_text = f"Probability of loan acceptance: {proba:.2}"
    loan_status_text = f"Loan status: {loan_status}"

    # Render the template with the prediction and loan status
    return render_template('index1.html',
                           prediction_text=prediction_text,
                           loan_status_text=loan_status_text)

@app.route('/test', methods=['GET', 'POST'])
def test_predict():
    if request.method == 'POST':
        client_id = request.form['client_id']

        # Check if the client ID is in the dataset
        if int(client_id) not in df['SK_ID_CURR'].values:
            return jsonify({'error': 'Client ID not found in the dataset'})

        # Get the corresponding row from the test data
        row = df[df['SK_ID_CURR'] == int(client_id)].iloc[:, 1:]

        # Test the prediction
        proba = model.predict_proba(row)[0][1]
        pred = model.predict(row)[0]
        assert pred in [0, 1], "Prediction must be either 0 or 1"

        # Set the loan status based on the predicted value
        if pred < 0.5:
            loan_status = 'Accepted'
        else:
            loan_status = 'Rejected'

        # Return the results as a dictionary
        return {
            "prediction": proba,
            "loan_status": loan_status
        }

    return render_template('test.html')



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)