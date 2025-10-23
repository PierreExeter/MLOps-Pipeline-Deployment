App Deployment to Azure
===================================

.. _deployment:

Manual Deployment
------------------------

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

   docker push insurancemodel.azurecr.io/mlops-insurance-prediction:latest

This will take some time, depending on the size of the image. The image should appear in the ACR.

5. Create a web app on Azure Azure portal > create a resource > web app > create > Choose a name (e.g. insurance-predictions)

Select the following options: 

- Publish : Choose Container 
- Choose a region and a pricing plan (there is a free plan called “Free F1”).

6. Link the ACR image to your application

Go to the Docker tab and fill the following details: 

- **Source** : ``Azure Container Registry`` 
- **Registry** : ``insurancemodel`` 
- **Image** : ``mlops-insurance-prediction``
- **Tag** : ``latest`` 
- **Port** : ``5000``

7. The app is running and deployed to
   `https://insurance-predictions.azurewebsites.net <https://insurance-predictions.azurewebsites.net/>`__
   

Continuous Deployment with GitHub Actions
------------------------------------------------

Prerequisites
-------------

- Azure CLI installed and logged in
- Azure Container Registry: ``insurancemodel``
- Azure Web App: ``insurance-predictions``
- GitHub repository with appropriate permissions

Step 1: Create Azure Service Principal
--------------------------------------

Run the following commands in Azure CLI to create a service principal with the necessary permissions.

Get Resource IDs
^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Get ACR resource ID
   ACR_ID=$(az acr show --name insurancemodel --query id -o tsv)

   # Get Web App resource ID
   WEBAPP_ID=$(az webapp show --name insurance-predictions --query id -o tsv --resource-group <your-resource-group>)

   # Verify both IDs are retrieved
   echo "ACR ID: $ACR_ID"
   echo "WebApp ID: $WEBAPP_ID"

Create Service Principal
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   az ad sp create-for-rbac \
     --name "github-actions-mlops-deployment" \
     --role contributor \
     --scopes $ACR_ID $WEBAPP_ID

**Save the output!** It will look like:

.. code-block:: json

   {
     "appId": "xxxx-xxxx-xxxx-xxxx",
     "displayName": "github-actions-mlops-deployment",
     "password": "xxxx-xxxx-xxxx-xxxx",
     "tenant": "xxxx-xxxx-xxxx-xxxx"
   }

Grant ACR Push Permission
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   az role assignment create \
     --assignee <appId-from-above> \
     --scope $ACR_ID \
     --role AcrPush

Step 2: Configure GitHub Secrets
--------------------------------

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

1. AZURE_CREDENTIALS
^^^^^^^^^^^^^^^^^^^^^

Format the service principal output as JSON:

.. code-block:: json

   {
     "clientId": "<appId from service principal>",
     "clientSecret": "<password from service principal>",
     "subscriptionId": "<run: az account show --query id -o tsv>",
     "tenantId": "<tenant from service principal>"
   }

2. AZURE_REGISTRY_USERNAME
^^^^^^^^^^^^^^^^^^^^^^^^^^

Value: ``<appId from service principal>``

3. AZURE_REGISTRY_PASSWORD
^^^^^^^^^^^^^^^^^^^^^^^^^^

Value: ``<password from service principal>``

Step 3: Verify Workflow Configuration
-------------------------------------

The workflow file ``.github/workflows/azure-deploy.yml`` is configured with:

- **Registry Name**: ``insurancemodel``
- **Image Name**: ``mlops-insurance-prediction``
- **Web App Name**: ``insurance-predictions``

If any of these need to be changed, edit the ``env:`` section in the workflow file.

Step 4: Understanding Workflow Execution
----------------------------------------

Workflow Chain
^^^^^^^^^^^^^^

When you push to the ``main`` branch:

1. **Python Application** workflow runs first (tests and linting)
2. **Only if tests pass**, the Azure deployment workflow triggers automatically
3. If tests fail, deployment is skipped (preventing broken code from being deployed)

Automatic Trigger
^^^^^^^^^^^^^^^^^

1. Create a pull request and merge it to ``main``
2. The Python application workflow runs first
3. If successful, the deployment workflow triggers automatically
4. Monitor progress in the Actions tab

Manual Trigger
^^^^^^^^^^^^^^

1. Go to Actions tab in GitHub
2. Select "Deploy to Azure Container Registry and Web App"
3. Click "Run workflow"
4. Select the ``main`` branch
5. Click "Run workflow"


Troubleshooting
---------------

Workflow fails at "Log in to Azure Container Registry"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Verify ``AZURE_REGISTRY_USERNAME`` and ``AZURE_REGISTRY_PASSWORD`` are correct
- Check service principal has AcrPush role

Workflow fails at "Deploy to Azure Web App"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Verify ``AZURE_CREDENTIALS`` secret is properly formatted JSON
- Check service principal has contributor role on Web App
- Ensure Web App is configured to use containers

Docker build fails
^^^^^^^^^^^^^^^^^^

- Check Dockerfile syntax
- Verify all required files are present in repository
- Check build logs for specific errors

Image Tags
----------

The workflow creates two tags for each deployment:

- ``latest``: Always points to the most recent deployment
- ``<commit-sha>``: Specific commit version (e.g., ``abc1234``)

Full image path: ``insurancemodel.azurecr.io/mlops-insurance-prediction:latest``

Security Notes
--------------

- Service principal credentials are stored as GitHub encrypted secrets
- Credentials are never exposed in logs
- Azure logout is performed after each workflow run
- Consider rotating service principal credentials periodically

