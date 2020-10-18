import requests
import json             # To use request package in current program 
url = 'https://disease.sh/v3/covid-19/all' 
response = requests.get(url)        # To execute get request 
print(response.status_code)     # To print http response code  
print(response.text)            # To print formatted JSON response 

url = 'https://disease.sh/v3/covid-19/gov/israel?allowNull=true' 
response = requests.get(url)        # To execute get request 
print(response.status_code) 

result = json.loads(response.text) 


