Unit Tests
==========

.. _unit_test:

Running Tests
-------------

To run the complete test suite, execute:

.. code-block:: bash

   pytest src/all_tests.py -v

For more verbose output including test timing:

.. code-block:: bash

   pytest src/all_tests.py -vv

Test Coverage
-------------

The test suite covers the following areas:

**Model Validation Tests:**

- **Model Binary Creation** (``test_model_binary_created``): Verifies that the machine learning model can be trained and saved successfully as a pickle file.

**API Endpoint Tests:**

- **Home Route** (``test_home_route``): Ensures the homepage (``/``) loads properly and returns HTTP 200.
- **Form Prediction** (``test_predict_route_post``): Tests the web form endpoint (``/predict``) with sample patient data, verifying predictions are returned in the expected format.
- **API Prediction** (``test_predict_api_route``): Tests the JSON API endpoint (``/predict_api``) with structured data, ensuring it returns integer predictions.
- **HTTP Method Validation** (``test_predict_route_get``): Confirms that GET requests to prediction endpoints are handled appropriately (should not allow form submissions via GET).

Test Data
---------

The tests use realistic sample data representing typical insurance prediction scenarios:

.. code-block:: python

   {
       'age': '25',        # Young adult
       'sex': 'male',      # Gender
       'bmi': '22.5',      # Normal weight
       'children': '0',    # No children
       'smoker': 'no',     # Non-smoker
       'region': 'southwest'  # US region
   }

Expected Outcomes
-----------------

- **All tests should pass** in a properly configured environment
- **Model training may take 1-2 minutes** on first run (``test_model_binary_created``)
- **API responses should return integer dollar amounts** (e.g., ``3250`` for $3,250)
- **HTTP status codes should be 200** for successful requests

Debugging Failed Tests
----------------------

If tests fail, check:

1. **Model File**: Ensure ``model/pycaret-model.pkl`` exists or can be created
2. **Dependencies**: Verify all required packages are installed
3. **Flask App**: Confirm the app can start (``python src/app.py``)
4. **Permissions**: Check write permissions for model directory

Skipping Slow Tests
-------------------

To skip the model training test during development:

.. code-block:: bash

   pytest src/all_tests.py -v -k "not test_model_binary_created"
