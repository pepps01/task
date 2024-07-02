from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def world():
    return jsonify("welcome")

@app.route("/api/hello")
def hello_world():
    try:
        if request.method=="GET":
            visitor_name = request.args.get('vistor_name')
            if visitor_name:
                ip_address=request.environ['REMOTE_ADDR']
                api_key="0c3133342a2344fd6d7696da0bb6f4b9"
                latitude =0
                longitude =0
                temperature =0
                city=""

                url= f'https://api.ipbase.com/v1/json/{ip_address}'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    city = data.get('city') 
                    latitude = data.get('latitude')
                    longitude = data.get('longitude')
                else:
                    return jsonify("fialed ipbase")


                api= f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
                degree_response = requests.get(api)
                if degree_response.status_code == 200:
                    res_data = degree_response.json()
                    temperature = calculate_temperature(int(res_data.get('main')['temp']))
                else:
                    return jsonify("fdegree issues")

                result = {
                    "client_ip": request.environ['REMOTE_ADDR'],
                    "location":city,
                    "greeting":f"Hello,{visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
                }
                return jsonify(result)
            else:
                return jsonify(message="Wrong argument")
        
    except ConnectionError:
        print(ConnectionError)
    except EnvironmentError:
        print(EnvironmentError)

def calculate_temperature(f):
    return int(float(((f-32) * 5)/9))

if __name__ == '__main__':
    app.run()
