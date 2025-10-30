
import requests

url = 'https://api.huum.eu/action/home/start'
myobj = {'targetTemperature' : 40}
#enter your username and password from app
usern = 'justintsmith@gmail.com'
passw = 'hy6Dr.Jm8391'
x = requests.post(url, data = myobj, auth=(usern,passw))
print(x.json())

