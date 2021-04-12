# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
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
	Google = None
	Bing = None
	Here = None
	OSM = None
	
	if request.method == "GET":
		pass
	elif request.method == "POST":
		try:
			dir_solicitada = request.POST["listDirecciones"]
			location_Google = geocoder.google(dir_solicitada)
			location_Bing = geocoder.bing(dir_solicitada)
			location_Here = geocoder.here(dir_solicitada, app_id='PWQguUtERmkUxTmtHjHX',
                    app_code='dYlmePq5h6xBhq1DYD1Ljw')
			location_OSM = geocoder.osm(dir_solicitada)
			if location_Google.ok == False and location_Bing.ok == False and location_Here == False and location_OSM.ok == False:
				Google = None
				Bing = None
				Here = None
				OSM = None
				dir_solicitada = dir_solicitada
				mensaje_alerta ='Ningún servicio pudo geocodificar esta dirección, ¡la encontrarías tu en el mapa!'
				print("Ningún servicio arrojó resultados")
			else:
				dir_solicitada = dir_solicitada
				if location_Google.ok == False: #No Google
					Google = None
					print('Google is False')
					if location_Bing.ok == False: #No Google y Bing
						Bing = None
						if location_Here.ok == False: #Ni Google, ni Bing, ni Here
							Here = None
							# Al menos uno debe estar por lo tanto Sí OSM
							OSM = location_OSM.json
							print('Google, Bing and Here are False but OSM not')
							mensaje_alerta = 'Unicamente el servicio de OpenStreetMap ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
						else:
							Here = location_Here.json
							if location_OSM.ok == False:
								OSM = None
								print('Only Here is True')
								mensaje_alerta = 'Unicamente el servicio de Here Maps ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
							else:
								OSM = location_OSM.json
								print('Only Here and OSM are True')
								mensaje_alerta = 'Los servicios de Here Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
					else:
						Bing = location_Bing.json #No Google, Sí Bing
						if location_Here.ok == False: 
							Here = None
							if location_OSM.ok == False:
								OSM = None
								print('Google, Here and OSM are False but Bing not') #No Google, No Here, No OSM, Sí Bing
								mensaje_alerta = 'Unicamente el servicio de Bing Maps ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
							else:
								OSM = location_OSM.json
								print('Google, and Here are False but Bing and OSM not') #No Google, No Here, Sí OSM, Sí Bing
								mensaje_alerta = 'Los servicios de Bing Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
						else:											
							Here = location_Here.json #No Google, Sí Bing, Sí Here ¿OSM?
							if location_OSM.ok == False:
								OSM = None
								mensaje_alerta = 'Los servicios de Bing Maps y Here Maps han encontrado esta dirección, ¡a ver qué tal!'
								print("Google and OSM are False but Bing and Here is not")
							else:
								OSM = location_OSM.json
								print("Google is False but Bing, Here and OSM is not")
								mensaje_alerta = 'Los servicios de Bing Maps, Here Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
				elif location_Bing.ok == False: #No Bing y Sí Google y ¿Here y OSM?
					Google = location_Google.json
					Bing = None 
					print('Bing is False but Google not') 
					if location_Here.ok == False: #Sí Google, No Bing, No Here
						Here = None
						if location_OSM.ok == False: #Sí Google, No Bing, No Here, No OSM
							OSM = None
							mensaje_alerta = 'Unicamente el servicio de Google Maps ha podido encontrar esta dirección, ¡bueno al menos alguno sí, a ver qué tal!'
							print('Bing, Here and OSM are False but Google not')
						else:
							OSM = location_OSM.json
							print('Bing and Here are false but Google and OSM not')
							mensaje_alerta = 'Los servicios de Google Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
					else:					#No Bing, Sí Google, Sí Here  ¿OSM?
						Here = location_Here.json
						if location_OSM.ok == False:
							OSM = None
							print("Bing and OSM are False, but Google and Here not")
							mensaje_alerta = 'Los servicios de Google Maps y Here Maps han encontrado esta dirección, ¡a ver qué tal!'
						else:
							OSM = location_OSM.json
							print("Bing are False, but Google, Here and OSM not")
							mensaje_alerta = 'Los servicios de Google Maps, Here Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
						
				elif location_Here.ok == False: #Sí Google, Sí Bing y ¿Here y OSM?
					Here = None
					print('Here is false but Google and Bing not')
					Google = location_Google.json
					Bing = location_Bing.json
					if location_OSM.ok == False:
						OSM = None
						print('Here and OSM are false but Google and Bing not')
						mensaje_alerta = 'Los servicios de Google Maps y Bing Maps han encontrado esta dirección, ¡a ver qué tal!'
					else:
						OSM = location_OSM.json
						print('Here is false but Google, Bing and OSM not')
						mensaje_alerta = 'Los servicios de Google Maps, Bing Maps y OpenStreetMap han encontrado esta dirección, ¡a ver qué tal!'
				elif location_OSM.ok == False:
					OSM = None
					print('OSM is false but Google, Bing and Here not')
					Google = location_Google.json
					Bing = location_Bing.json
					Here = location_Here.json
					mensaje_alerta = 'Los servicios de Google Maps, Bing Maps y Here Maps han encontrado esta dirección, ¡a ver qué tal!'
				else:
					Google = location_Google.json
					Bing = location_Bing.json
					Here = location_Here.json
					OSM = location_OSM.json
					mensaje_alerta = 'Todos los servicios encontraron esta dirección, ¡cúal localicación crees que será la mejorl!'
					print("Estan los cuatro")
					print("Resultados Google:")
					#print(yGoogle, xGoogle)
					print(location_Google.json)
					print("Resultados Bing:")
					#print(yBing, xBing)
					print(location_Bing.json)
					print("Resultados Here")
					#print(yHere, xHere)
					print(location_Here.json)
					print("Resultados OSM:")
					print(location_OSM.json)
					#print(yOSM, xOSM)
		except Exception as e:
			mensaje_alerta = 'Servicio no disponible, intentelo más tarde.'
			print(e)
			pass
	else:
		dir_solicitada = None
		mensaje_alerta = None
		Google = None
		Bing = None
		Here = None
		OSM = None
		pass

	context = {'jsonGoogle': Google, 'jsonBing': Bing, 'jsonHere': Here, \
	'jsonOSM': OSM, 'dir_solicitada': dir_solicitada,'mensaje_alerta': mensaje_alerta}

	return render(request, 'app.html', context)
	return HttpResponse(Google, content_type='application/json')

