# MLOps Pipeline Deployment

![app_screenshot](docs/img/app_screenshot.png)

[VIEW DEPLOYED APP HERE](https://insurance-predictions.azurewebsites.net/)

This project demonstrates a MLOps pipeline for deploying a machine learning model into a production-ready web application. The goal is to help an insurance company forecast patient charges using input like age, gender, BMI, number of children, and smoking status.

The solution includes:
- A **machine learning** model trained to predict insurance charges
- A **Flask back-end** to serve predictions
- A **HTML / CSS front-end** for user input
- Containerization with **Docker**
- Cloud deployment on **Microsoft Azure**
- A CI/CD pipeline with **Github Actions**
- A product **documentation**


## Docker Install (recommended)

1. Clone the repository

```
git clone https://github.com/PierreExeter/MLOps-Pipeline-Deployment
```

2. Build the image

```
docker build -t insurancemodel.azurecr.io/pycaret-insurance:latest .
```

The diferent elements in this command are : 
- Azure registry name : insurancemodel.azurecr.io
- Docker image name : pycaret-insurance
- tag : latest


3. Run the Docker container
```
docker run -d -p 5000:5000 insurancemodel.azurecr.io/pycaret-insurance
```

The web app is served on [http://localhost:5000/](http://localhost:5000/)

4. Open the container (optional)

```
docker exec -it <container-id> /bin/bash
```

5. Stop the container
```
docker stop <container-id>
```

## Azure Deployment

1. Log in to Azure
2. Create a new Azure Container Registry (ACR) named "insurancemodel.azurecr.io"
3. Authenticate with Azure credentials

```
docker login insurancemodel.azurecr.io
```
The username is name of the registry, in this example "insurancemodel".
The password can be found in Azure Container Registry > Settings > Access keys. Tick the box "admin user" to reveal the password.

4. Push the image to the Azure registry
```
docker push insurancemodel.azurecr.io/pycaret-insurance:latest
```

This will take some time, depending on the size of the image. The image should appear in the ACR.

5. Create a web app on Azure
Azure portal > create a resource > web app > create > Choose a name (e.g. insurance-predictions)
 
Select the following options:
- Publish : Choose Container
- Choose a region and a pricing plan (there is a free plan called "Free F1").
 
6. Link the ACR image to your application

Go to the Docker tab and fill the following details:
- Source : Azure Container Registry
- Registry : insurancemodel
- Image : pycaret-insurance
- tag : latest
- port : 5000

7. The app is running and deployed to [https://insurance-predictions.azurewebsites.net](https://insurance-predictions.azurewebsites.net/) 



## Local Install

1. Clone the repository

```
git clone https://github.com/PierreExeter/MLOps-Pipeline-Deployment
```

2. Install [uv](https://github.com/astral-sh/uv)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate the environment

```
uv venv --python 3.11
source .venv/bin/activate
```

4. Install the dependencies

```
uv pip install -r requirements.txt
```

3. Train the model
```
python src/train_model.py
```

4. Run the app locally
```
# development
python src/app.py

# production
python src/app.py --production

```

The web app is served on [http://localhost:5000/](http://localhost:5000/)

5. Test sending a request to the API

```
python src/api_call_example.py
```

