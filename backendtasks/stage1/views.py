from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from requests import get
from dotenv import load_dotenv
import os
load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
IP_LOCATION_RESOLVER = "https://api.iplocation.net/?ip="

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(ip):
    data = get(f"{IP_LOCATION_RESOLVER}{ip}").json()
  
    return data.get('country_name')

def get_temperature(location):
    LOCATION_WEATHER_RESOLVER = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    data = get(LOCATION_WEATHER_RESOLVER).json()
    print(data)
    return "11"


class HelloView(APIView):

    def get(self, request):

        ip =  get_client_ip(request)
        name = request.query_params.get('name', 'John Doe')
        location = get_location(ip)
        temperature = get_temperature(location)

        response = {
            "client_ip": ip,
            "location": location,
            "greeting": f"Hello, {name}!, the temperature is {temperature} degrees Celsius. in {location}"
        }
        return Response(response)

