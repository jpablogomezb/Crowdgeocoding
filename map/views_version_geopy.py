# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from geopy.geocoders import GoogleV3
from geopy.geocoders import Bing
from geopy.geocoders import OpenMapQuest
import geocoder

# Create your views here.

def home(request):

	context = { }
	template = 'home.html'
	return render(request, template, context)

@login_required
def app2(request):

	context = { }
	template = 'app.html'
	return render(request, template, context)
		

def app(request):

	dir_solicitada = None
	mensaje_alerta = None
	yGoogle = None
	xGoogle = None

	yBing = None
	xBing = None

	yMapQuestOSM = None
	xMapQuestOSM = None

	if request.method == "GET":
		pass
	elif request.method == "POST":
		try:
			dir_solicitada = request.POST["listDirecciones"]
			g = geocoder.google(dir_solicitada)
			geolocator_Google = GoogleV3(timeout=10)
			geolocator_Bing = Bing('Aj-muALyX0OpYsdC50eA6F4VIfK1LU4tSrh-I6bGlFdgLAK8ZzysnRZbuZOGNvA1',timeout=10)
			geolocator_MapQuestOSM = OpenMapQuest(timeout=10)
			location_Google = geolocator_Google.geocode(dir_solicitada)
			location_Bing = geolocator_Bing.geocode(dir_solicitada)
			location_MapQuestOSM = geolocator_MapQuestOSM.geocode(dir_solicitada)
			if location_Google is None and location_Bing is None and location_MapQuestOSM is None:
				yGoogle = None
				xGoogle = None
				yBing = None
				xBing = None
				xMapQuestOSM = None
				yMapQuestOSM = None
				dir_solicitada = dir_solicitada
				mensaje_alerta ='Ningún servicio pudo geocodificar esta dirección, ¡la encontrarias tu en el mapa!'
				print("Ningún servicio arrojó resultados")
			else:
				dir_solicitada = dir_solicitada
				if location_Google is None: #No Google
					yGoogle = None
					xGoogle = None
					print('Google is None')
					if location_Bing is None: #No Google y Bing
						yBing = None
						xBing = None
						# Al menos uno debe estar por lo tanto Sí MapQuestOSM
						yMapQuestOSM = location_MapQuestOSM.latitude
						xMapQuestOSM = location_MapQuestOSM.longitude
						print('Google and Bing is None but MapQuestOSM not')
						mensaje_alerta = 'Unicamente el servicio de MapQuest Open ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
					else:
						yBing = location_Bing.latitude
						xBing = location_Bing.longitude
						if location_MapQuestOSM is None:
							yMapQuestOSM = None
							xMapQuestOSM = None
							print('Google and MapQuestOSM is None but Bing not') #Sí Bing
							mensaje_alerta = 'Unicamente el servicio de Bing Maps ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
						else: 											# Sí Bing y MapQuestOSM
							yMapQuestOSM = location_MapQuestOSM.latitude
							xMapQuestOSM = location_MapQuestOSM.longitude
							mensaje_alerta = 'Los servicios de Bing Maps y MapQuest Open han encontrado esta dirección, ¡a ver qué tal!'
							print("Google is None but Bing and OSM is not")
				elif location_Bing is None: #No Bing y Sí Google y ¿MapQuestOSM?
					yBing = None
					xBing = None 
					print('Bing is None but Google not') 
					if location_MapQuestOSM is None: #Sí Google no los demas
						yMapQuestOSM = None
						xMapQuestOSM = None
						yGoogle = location_Google.latitude
						xGoogle = location_Google.longitude
						mensaje_alerta = 'Unicamente el servicio de Google Maps ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
						print('Bing and OSM is None but Google not')
					else:					# Sí Google y OSM
						yGoogle = location_Google.latitude
						xGoogle = location_Google.longitude
						xMapQuestOSM = location_MapQuestOSM.longitude
						yMapQuestOSM = location_MapQuestOSM.latitude
						mensaje_alerta = ' Los servicios de Google Maps y MapQuest Open han encontrado esta dirección, ¡a ver qué tal!'
						print("Bing is None but Google and OSM is not")
				elif location_MapQuestOSM is None: #Sí Google y Sí Bing
					yMapQuestOSM = None
					xMapQuestOSM = None
					print('OSM is None but Google and Bing not')
					yGoogle = location_Google.latitude
					xGoogle = location_Google.longitude
					yBing = location_Bing.latitude
					xBing = location_Bing.longitude
					mensaje_alerta = 'Los servicios de Google Maps y Bing Maps han encontrado esta dirección, ¡a ver qué tal!'
				else:
					yGoogle = location_Google.latitude
					xGoogle = location_Google.longitude
					yBing = location_Bing.latitude
					xBing = location_Bing.longitude
					yMapQuestOSM = location_MapQuestOSM.latitude
					xMapQuestOSM = location_MapQuestOSM.longitude
					mensaje_alerta = 'Todos los servicios encontraron esta dirección, ¡cúal localicación crees que será la mejorl!'
					print("Estan los tres")
					print("Resultados Google:")
					#print(location_Google.raw)
					print(yGoogle, xGoogle)
					print("Resultados Bing:")
					#print(location_Bing.raw)
					print(yBing, xBing)
					print("Resultados OSM:")
					print(location_MapQuestOSM.raw)
					#print(yMapQuest Open, xMapQuest Open)
		except Exception as e:
			mensaje_alerta = 'Servicio no disponible, intentelo más tarde.'
			print(e)
			pass
	else:
		dir_solicitada = None
		mensaje_alerta = None
		yGoogle = None
		xGoogle = None
		yBing = None
		xBing = None
		xMapQuestOSM = None
		yMapQuestOSM = None
		pass

	context = {'yGoogle': yGoogle,'xGoogle': xGoogle,'yBing': yBing, 'xBing': xBing, \
	'yMapQuestOSM':yMapQuestOSM,'xMapQuestOSM': xMapQuestOSM, \
	 'dir_solicitada': dir_solicitada,'mensaje_alerta': mensaje_alerta}

	return render(request, 'app.html', context)
