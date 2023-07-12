from django.http import HttpResponse
from django.shortcuts import render
import requests
import random
import json
from django.http import JsonResponse


# Create your views here.

def home(request):
    r = requests.get('https://countriesnow.space/api/v0.1/countries/capital')
    data = r.json()

    if data['error']:
        return render(request, 'error.html')
    if request.method == 'POST':

        # get data
        form_data = request.POST
        status, result = checkAnswer(data['data'], form_data.get('Question'), form_data.get('answer'))

        return JsonResponse({"success": status, "data": result})


    city = []
    country = ''

    context = {}
    if data['error'] == False :
        country, city = randonCountryListCity(data['data'])
        context['country'] = country
        context['city_list'] = json.dumps(city)
        


    return render(request, 'index.html', context)

 

def checkAnswer(data, country, city):
    country_obj = ''
    for obj in data:
        if obj["name"] == country:
            country_obj = obj
            break


    if country_obj :
        if country_obj['capital'] == city:
            return True, country_obj
    
    return False, country_obj

def randonCountryListCity(data):
    obj = random.choice(data)
    city_list = [ obect_city["capital"] for obect_city in data]

    return obj["name"], city_list