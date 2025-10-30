import requests

url = 'https://api.huum.eu/action/home/status'
#enter your username and password from app
usern = 'justintsmith@gmail.com'
passw = 'hy6Dr.Jm8391'
x = requests.get(url, auth=(usern,passw))
print(x.json())

