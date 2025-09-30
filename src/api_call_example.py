import requests


# url = 'https://insurance-predictions.azurewebsites.net/predict_api'
url = 'http://localhost:5000/predict_api'

data = {
    'age': 55, 
    'sex': 'male', 
    'bmi': 59, 
    'children': 1, 
    'smoker': 'yes',
    'region': 'northwest'
}

pred = requests.post(url, json=data)

print('The expected bill is ${}'.format(pred.json()))
# print(pred.json())
