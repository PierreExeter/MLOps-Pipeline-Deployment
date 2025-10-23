API
===

The Insurance Prediction API provides programmatic access to the machine learning model for predicting insurance costs.

Endpoints
---------

/predict_api (POST)
^^^^^^^^^^^^^^^^^^^

Predicts insurance costs based on input parameters.

**Request Format:**

.. code-block:: http

   POST /predict_api
   Content-Type: application/json

   {
     "age": 25,
     "sex": "male",
     "bmi": 22.5,
     "children": 0,
     "smoker": "no",
     "region": "southwest"
   }

**Parameters:**

- **age** (integer): Patient's age (18-65)
- **sex** (string): "male" or "female"
- **bmi** (float): Body Mass Index (15.0-55.0)
- **children** (integer): Number of children (0-5)
- **smoker** (string): "yes" or "no"
- **region** (string): "southwest", "southeast", "northwest", or "northeast"

**Response Format:**

.. code-block:: http

   HTTP 200 OK
   Content-Type: application/json

   3250

**Response:** Integer representing expected insurance cost in dollars.

**Error Responses:**

- **400 Bad Request**: Invalid input parameters or missing required fields
- **500 Internal Server Error**: Model prediction failure

Request Examples
^^^^^^^^^^^^^^^^

To send a request to the API using the example script:

.. code-block:: bash

   python src/api_call_example.py

This will make a POST request to ``http://localhost:5000/predict_api`` with sample data and print the predicted insurance cost.

**Custom Requests with curl:**

.. code-block:: bash

   curl -X POST http://localhost:5000/predict_api \
     -H "Content-Type: application/json" \
     -d '{
       "age": 35,
       "sex": "female",
       "bmi": 28.5,
       "children": 2,
       "smoker": "yes",
       "region": "northeast"
     }'

**Python Requests:**

.. code-block:: python

   import requests

   url = 'http://localhost:5000/predict_api'
   data = {
       'age': 35,
       'sex': 'female',
       'bmi': 28.5,
       'children': 2,
       'smoker': 'yes',
       'region': 'northeast'
   }

   response = requests.post(url, json=data)
   prediction = response.json()
   print(f'Expected insurance cost: ${prediction}')
