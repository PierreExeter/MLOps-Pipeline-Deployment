Installation
===================================

.. _installation:

Docker Install
----------------

1. Clone the repository

::

   git clone https://github.com/PierreExeter/MLOps-Pipeline-Deployment

2. Build the image

::

   docker build -t insurancemodel.azurecr.io/mlops-insurance-prediction:latest .

The diferent elements in this command are :

- Azure registry name : insurancemodel.azurecr.io
- Docker image name : mlops-insurance-prediction
- tag : latest

3. Run the Docker container

::

   docker run -d -p 5000:5000 insurancemodel.azurecr.io/mlops-insurance-prediction

The web app is served on http://localhost:5000/

4. Open the container (optional)

::

   docker exec -it <container-id> /bin/bash

5. Stop the container

::

   docker stop <container-id>

Local Install
----------------

1. Clone the repository

::

   git clone https://github.com/PierreExeter/MLOps-Pipeline-Deployment

2. Install the dependencies

::

   conda create -n pycaret-env python=3.11 -y
   conda activate pycaret-env
   pip install -U -r requirements.txt

3. Train the model

::

   python src/train_model.py

4. Run the app locally

::

   # development
   python src/app.py

   # production
   python src/app.py --production

The web app is served on http://localhost:5000/
