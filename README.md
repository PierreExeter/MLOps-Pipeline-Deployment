# MLOps Pipeline Deployment

AZURE:
https://www.datacamp.com/tutorial/tutorial-machine-learning-pipelines-mlops-deployment

HEROKU:
https://medium.com/data-science/build-and-deploy-your-first-machine-learning-web-app-e020db344a99

## Docker Install (recommended)

1. Clone the repository

```
git clone 
```

2. Build the image

```
docker compose build
```

azure registry name
insurancemodel.azurecr.io

name of image
pycaret-insurance

docker build -t insurancemodel.azurecr.io/pycaret-insurance:latest .


3. Launch the Docker container
```
docker compose up -d
```

ISSUE HERE: This does not run

docker run -d -p 5000:5000 insurancemodel.azurecr.io/pycaret-insurance


## Local Install

1. Clone the repository

```
git clone
```

2. Install the dependencies

```
conda create -n pycaret-env python=3.11 -y
conda activate pycaret-env
pip install -U -r requirements.txt


conda install -c rapidsai -c nvidia -c conda-forge cuml
```

python src/train_model.py

python src/app.py

served on:
http://127.0.0.1:5000/




