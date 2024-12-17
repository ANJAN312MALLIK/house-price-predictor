import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load data and model
data = pd.read_csv('data/Cleaned_data (1).xls')
pipe = pickle.load(open('models/RidgeModel.pkl', 'rb'))

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;  /* Background color set to black */
    }
    body {
        font-family: 'Pacifico', cursive;
        padding: 20px;
    }
    .form-container {
        background-color: #44444c;
        padding: 30px;
        border-radius: 8px;
        margin-bottom: 30px;
    }
    .label-highlight {
        background-color: #fffae5;
        display: block;
        width: 100%;
        padding: 10px 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .btn-primary {
        padding: 10px 20px;
    }
    .prediction {
        color: #db6307;
        font-weight: bold;
        margin-top: 20px;
    }
    .header-title {
        color: #f39c12;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .sub-title {
        color: #E50914;  /* Updated blue to red */
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    .select-location {
        color: #E50914;  /* Set to red */
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    .prediction-output {
        color: #e74c3c;
        font-weight: bold;
        font-size: 1.5em;
        margin-top: 20px;
    }

    /* Responsive Design */
    @media screen and (max-width: 600px) {
        .header-title {
            font-size: 1.8em;
        }
        .sub-title, .select-location, .prediction-output {
            font-size: 1.2em;
        }
        .form-container {
            padding: 15px;
        }
    }

    @media screen and (min-width: 601px) and (max-width: 1200px) {
        .header-title {
            font-size: 2.2em;
        }
        .sub-title, .select-location, .prediction-output {
            font-size: 1.4em;
        }
        .form-container {
            padding: 25px;
        }
    }

    @media screen and (min-width: 1201px) {
        .header-title {
            font-size: 2.5em;
        }
        .sub-title, .select-location, .prediction-output {
            font-size: 1.5em;
        }
        .form-container {
            padding: 30px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom JavaScript
st.markdown(
    """
    <script>
      function send_data(event) {
        event.preventDefault();

        var fd = new FormData(document.querySelector("form"));

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/predict", true);
        document.getElementById("prediction").innerHTML =
          "Wait predicting price....";
        xhr.onreadystatechange = function () {
          if (xhr.readyState == XMLHttpRequest.DONE) {
            document.getElementById("prediction").innerHTML =
              "Prediction: " + xhr.responseText;
          }
        };
        xhr.send(fd);
      }
    </script>
    """,
    unsafe_allow_html=True
)

st.markdown('<h2 class="header-title">House Price Predictor</h2>', unsafe_allow_html=True)

# Create a selectbox for locations
st.markdown('<h3 class="select-location">Select the Location</h3>', unsafe_allow_html=True)
locations = sorted(data['location'].unique())
location = st.selectbox('', locations)

st.markdown('<h3 class="sub-title">Enter BHK</h3>', unsafe_allow_html=True)
bhk = st.slider('Enter BHK', 1, 10, 1)

st.markdown('<h3 class="sub-title">Enter Number of Bathrooms</h3>', unsafe_allow_html=True)
bath = st.slider('Enter Number of Bathrooms', 1, 10, 1)

st.markdown('<h3 class="sub-title">Enter Square Feet</h3>', unsafe_allow_html=True)
sqft = st.slider('Enter Square Feet', 400, 10000, 400)

# Predict button
if st.button('Predict Price'):
    input_data = pd.DataFrame([[location, sqft, bath, bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])
    prediction = pipe.predict(input_data)[0] * 1e5
    prediction = abs(prediction)  # Ensure prediction is positive
    st.markdown(f'<div class="prediction-output">Prediction: ₹{np.round(prediction, 2)}</div>', unsafe_allow_html=True)

     
