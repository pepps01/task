from flask import Flask, request, jsonify
import requests
import json
from dotenv import dotenv_values

app = Flask(__name__)
API_KEY = dotenv_values(".env") ['IP_BASE_API_KEY']

@app.route("/")
def world():
    return jsonify("welcome")


@app.route("/api/hello")
def hello_world():
    try:
        if request.method=="GET":
            visitor_name = request.args.get('visitor_name')
            # location_namer = 
            ip_address= request.environ['REMOTE_ADDR']
            temperature=0
            city=""

            url= f'https://api.ipbase.com/v1/json/{ip_address}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
              
                temperature = get_temperature(data.get('latitude'),data.get('longitude'), API_KEY)

                city = "Lagos"
                result = {
                    "client_ip": ip_address,
                    "location":city,
                    "greetings":f"Hello,{visitor_name}!, the temperature is {temperature} degrees Celsius in {city}",
                }
                return jsonify(result)
            else:
                return jsonify("The api failed to fetch")


    except ConnectionError:
        print(ConnectionError)
    except EnvironmentError:
        print(EnvironmentError)


def get_temperature(latitude, longitude, api_key):
    try:
        api= f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
        response = requests.get(api)
        temperature =""

        if response.status_code == 200:
            data = response.json()
            temperature =  calculate_temperature(int(data.get('main')['temp']))
        
        return temperature
    except ConnectionError as e:
        raise e

def calculate_temperature(f):
    return int(float(((f-32) * 5)/9))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
