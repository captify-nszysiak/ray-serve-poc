import requests

input = "['one direction edinburgh one direction edinburgh girlguiding edinburgh young adult books edinburgh " \
        "edinburgh hamster accessories hamster accessories edinburgh hamster accessories edinburgh hamster " \
        "accessories edinburgh'] "

response = requests.post("http://127.0.0.1:8000/", json=input)
response = response.text
print(response)
