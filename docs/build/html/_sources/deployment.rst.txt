Deployment on Azure
===================================

.. _deployment:


1. Log in to Azure

2. Create a new Azure Container Registry (ACR) named “insurancemodel.azurecr.io”

3. Authenticate with Azure credentials

::

   docker login insurancemodel.azurecr.io

The username is name of the registry, in this example “insurancemodel”.
The password can be found in Azure Container Registry > Access keys.
Tick the box “admin user” to reveal the password.

4. Push the image to the Azure registry

::

   docker push insurancemodel.azurecr.io/pycaret-insurance:latest

This will take some time, depending on the size of the image. The image should appear in the ACR.

5. Create a web app on Azure Azure portal > create a resource > web app > create > Choose a name (e.g. insurance-predictions)

Select the following options: 

- Publish : Choose Container 
- Choose a region and a pricing plan (there is a free plan called “Free F1”).

6. Link the ACR image to your application

Go to the Docker tab and fill the following details: 

- Source : Azure Container Registry 
- Registry : insurancemodel 
- Image : pycaret-insurance 
- tag : latest 
- port : 5000

7. The app is running and deployed to
   `https://insurance-predictions.azurewebsites.net <https://insurance-predictions.azurewebsites.net/>`__
   
