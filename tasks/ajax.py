# -*- coding: utf-8 -*-
import json, geocoder
from random import randint
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.contrib.gis.geos import fromstr, Point
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.encoding import smart_str, smart_unicode
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as _


from .models import UserProfile, Task, TaskAddress, AddressResult

#Project Vars
google_api_key = settings.GOOGLE_API
bing_api_key = settings.BING_API
mapquest_api_key = settings.MAPQUEST_API
mapbox_api_key = settings.MAPBOX_API
#here_app_id = settings.HERE_APP_ID
#here_app_code = settings.HERE_APP_CODE 

#Gets random addresses to geocode based on task, user and max_number_answers
def get_address(request):
    if request.is_ajax and request.method == "GET":
        the_task = None
        task_id = request.GET.get('task_id')
        the_task = Task.objects.get(pk=task_id)
        address_list = []
        task_address = ''
        #address_items = {}
        try:
            count = TaskAddress.objects.filter(task_name=the_task, status='IP').count()
            #print(count)
            #random_object = TaskAddress.objects.all()[randint(0, count - 1)] #single random object
            while len(address_list) < 5:
                try:
                    task_address = TaskAddress.objects.filter(task_name=the_task, status='IP')[randint(0, count - 1)]
                except Exception, e:
                    raise e
                if AddressResult.objects.filter(address=task_address, user=request.user.id).exists():
                    pass
                    # also if max_number_answers dont show
                else:
                    #address_items['task_address'] = task_address.address_text
                    #address_list.append({'task_address': task_address.address_text})
                    #address_list['address'].append(task_address.address_text)
                    if task_address.address_text not in address_list:
                        #address_list['task_address'] = task_address.address_text
                        address_list.append(task_address.address_text)
                        task_address = ''
            #print(address_list)
        except Exception, e:
            print(e)
                 
        return HttpResponse(json.dumps(address_list, sort_keys=True),content_type="application/json")
    else:
        raise Http404

# Obtains the online geocoder services results an response as a JSON 
def get_geocoders_output(request):
    if request.method == "GET":
        try:
            data = {}
            my_address = request.GET.get('address')
            location_Google = geocoder.google(my_address, method='geocode', key=google_api_key)
            location_Bing = geocoder.bing(my_address, key=bing_api_key)
            location_MapQuest = geocoder.mapquest(my_address, key=mapquest_api_key)
            location_OSM = geocoder.osm(my_address)
            #location_MapBox = geocoder.mapbox(my_address, key=mapbox_api_key)
            #location_Here = geocoder.here(my_address, app_id=here_app_id, app_code=here_app_code)

            data['address_requested'] = my_address
            data['google_longitude'] = location_Google.lng
            data['google_latitude'] = location_Google.lat
            data['google_confidence'] = location_Google.confidence
            data['google_accuracy'] = location_Google.accuracy
            data['google_quality'] = location_Google.quality
            data['google_info'] = location_Google.ok
            data['bing_longitude'] =  location_Bing.lng
            data['bing_latitude'] = location_Bing.lat
            data['bing_confidence'] =  location_Bing.confidence
            data['bing_accuracy'] = location_Bing.accuracy
            data['bing_quality'] =  location_Bing.quality
            data['mapquest_longitude'] =  location_MapQuest.lng
            data['mapquest_latitude'] = location_MapQuest.lat
            data['mapquest_confidence'] =  location_MapQuest.confidence
            data['mapquest_accuracy'] = location_MapQuest.accuracy
            data['mapquest_quality'] =  location_MapQuest.quality
            data['osm_longitude'] =  location_OSM.lng
            data['osm_latitude'] = location_OSM.lat
            data['osm_confidence'] = location_OSM.confidence
            data['osm_accuracy'] = location_OSM.accuracy
            data['osm_quality'] =  location_OSM.quality

            #Conditions to display results message
            if location_Google.ok == False and location_Bing.ok == False and location_MapQuest == False and location_OSM.ok == False:
                data['result_message'] = _('No service geocode this location, could you find it on the map!')
                #print("Ningún servicio arrojó resultados")
            else:
                if location_Google.ok == False: #No Google
                    #print('Google is False')
                    if location_Bing.ok == False: #No Google y Bing
                        if location_MapQuest.ok == False: #Ni Google, ni Bing, ni Here
                            #print('Google, Bing and Here are False but OSM not')
                            data['result_message'] = _('Only OpenStreetMap service has been able to find this location, well at least one, let us see how it is going!')
                        else:
                            if location_OSM.ok == False:
                                #print('Only Here is True')
                                data['result_message'] = _('Only MapQuest service has been able to find this location, well at least one, let us see how it is going!')
                            else:
                                #print('Only Here and OSM are True')
                                data['result_message'] = _('MapQuest and OpenStreetMap services have been able to find this location, let us see how it is going!')
                    else:
                        if location_MapQuest.ok == False: 
                            if location_OSM.ok == False:
                                #print('Google, Here and OSM are False but Bing not') #No Google, No Here, No OSM, Sí Bing
                                data['result_message'] = _('Only Bing Maps service has been able to find this location, well at least one, let us see how it is going!')
                            else:
                                #print('Google, and Here are False but Bing and OSM not') #No Google, No Here, Sí OSM, Sí Bing
                                data['result_message'] = _('Bing Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                        else:                                           
                            if location_OSM.ok == False:
                                data['result_message'] = _('Bing Maps and MapQuest services have been able to find this location, let us see how it is going!')
                                #print("Google and OSM are False but Bing and Here is not")
                            else:
                                #print("Google is False but Bing, Here and OSM is not")
                                data['result_message'] = _('Bing Maps, MapQuest and OpenStreetMap services have been able to find this location, let us see how it is going!')
                elif location_Bing.ok == False: #No Bing y Sí Google y ¿Here y OSM?
                    print('Bing is False but Google not') 
                    if location_MapQuest.ok == False: #Sí Google, No Bing, No Here
                        if location_OSM.ok == False: #Sí Google, No Bing, No Here, No OSM
                            data['result_message'] = _('Only Google Maps service has been able to find this location, well at least one, let us see how it is going!')
                            #print('Bing, Here and OSM are False but Google not')
                        else:
                            #print('Bing and Here are false but Google and OSM not')
                            data['result_message'] = _('Google Maps and OpenStreetMap services have been able to find this location, let us see how it is going!')
                    else:                   #No Bing, Sí Google, Sí Here  ¿OSM?
                        if location_OSM.ok == False:
                            #print("Bing and OSM are False, but Google and Here not")
                            data['result_message'] = _('Google Maps and MapQuest services have been able to find this location, let us see how is going!')
                        else:
                            #print("Bing are False, but Google, Here and OSM not")
                            data['result_message'] = _('Google Maps, MapQuest and OpenStreetMap services have been able to find this location, let us see how it is going!')
                        
                elif location_MapQuest.ok == False: #Sí Google, Sí Bing y ¿Here y OSM?
                    #print('MapQuest is false but Google and Bing not')
                    if location_OSM.ok == False:
                        #print('Here and OSM are false but Google and Bing not')
                        data['result_message'] = _('Google Maps and Bing Maps services have been able to find this location, let us see how is going!')
                    else:
                        #print('Here is false but Google, Bing and OSM not')
                        data['result_message'] = _('Google Maps, Bing Maps and OpenStreetMap services have been able to find this location, let us see how it is going!')
                elif location_OSM.ok == False:
                    #print('OSM is false but Google, Bing and Here not')
                    data['result_message'] = _('Google Maps, Bing Maps and MapQuest services have been able to find this location, let us see how it is going!')
                else:
                    data['result_message'] = _('All geocoding services found this address, what location do you think will be the best!')
                    #print("Estan los cuatro")

            #print data
            return HttpResponse(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')),content_type="application/json")

        except Exception, e:
            print(e)
            data = {}
            data['result_message'] = _('Platform services not available, please try it later.')
            return HttpResponse(json.dumps(data),content_type="application/json")
        
    else:
        return HttpResponse(json.dumps({"Bad request": "Please try again, thanks"}),
            content_type="application/json")

# Saves task-address results on AddressResult Model 
def save_answer(request):
    
    if request.is_ajax() and request.POST:
        task_id = request.POST.get('task_id')
    	dir_solicitada = request.POST.get('direccion_sol')
    	id_geo = request.POST.get('id_geo')
        xGoogle = request.POST.get('xGoogle', 'n/a')
        yGoogle = request.POST.get('yGoogle', 'n/a')
        accuGoogle = request.POST.get('accuGoogle', 'n/a')
        qualGoogle = request.POST.get('qualGoogle', 'n/a')
        confGoogle = request.POST.get('confGoogle', 'n/a')
        xBing = request.POST.get('xBing', 'n/a')
        yBing = request.POST.get('yBing' , 'n/a')
        accuBing = request.POST.get('accuBing', 'n/a')
        qualBing = request.POST.get('qualBing', 'n/a')
        confBing = request.POST.get('confBing', 'n/a')
        xMapquest = request.POST.get('xMapquest', 'n/a')
        yMapquest = request.POST.get('yMapquest', 'n/a')
        accuMapquest = request.POST.get('accuMapquest', 'n/a')
        qualMapquest = request.POST.get('qualMapquest', 'n/a')
        confMapquest = request.POST.get('confMapquest', 'n/a')
        xOSM = request.POST.get('xOSM', 'n/a')
        yOSM = request.POST.get('yOSM', 'n/a')
        accuOSM = request.POST.get('accuOSM', 'n/a' )
        qualOSM = request.POST.get('qualOSM', 'n/a')
        confOSM = request.POST.get('confOSM')
        cs_X = request.POST.get('csX', 'n/a')
        cs_Y = request.POST.get('csY', 'n/a')
      
        id_geocoder = id_geo
        print id_geocoder
    
        if id_geocoder == '1':
            the_geom = fromstr('POINT(' + xGoogle + " " + yGoogle + ')')
        elif id_geocoder == '2':
            the_geom = fromstr('POINT(' + xBing + " " + yBing + ')')
        elif id_geocoder == '3':
            the_geom = fromstr('POINT(' + xMapquest + " " + yMapquest + ')')
        elif id_geocoder == '4':
            the_geom = fromstr('POINT(' + xOSM + " " + yOSM + ')')
        else:
            the_geom = fromstr('POINT(' + cs_X + " " + cs_Y + ')')
        print the_geom

        the_task = Task.objects.get(pk=task_id)
        address_object = TaskAddress.objects.get(task_name=the_task, address_text=dir_solicitada)
        #print address_object.address_text

        #Guardar resultados
        result = AddressResult(user=request.user, address=address_object, geom_result=the_geom, selected_geocoder=id_geo,
        		coord_Google=yGoogle + ", " + xGoogle, coord_Bing= yBing + ", " + xBing,
        		coord_Mapquest=yMapquest + ", " + xMapquest, coord_OSM=yOSM + ", " + xOSM,
        		quality_Google=qualGoogle, quality_Bing=qualBing, quality_Mapquest=qualMapquest,quality_OSM=qualOSM,
        		accuracy_Google=accuGoogle, accuracy_Bing=accuBing, accuracy_Mapquest=accuMapquest, accuracy_OSM=accuOSM,
        		confidence_Google=confGoogle, confidence_Bing=confBing,
        		confidence_Mapquest=confMapquest, confidence_OSM=confOSM,
        		suggested_Coord=cs_X + "," + cs_Y)
        result.save()
        
        actual_number_ans = AddressResult.objects.filter(address=address_object).count()
        answers_needed = the_task.max_number_answers
        if actual_number_ans == answers_needed:
            address_object.status = 'F'
            address_object.save()

        return HttpResponseRedirect('/map/task/' + task_id + '/') 
    else:
        raise Http404


# Subscribes user to a task
def post_task(request):
    if request.method == 'POST':
        id_task = request.POST.get('the_post')
        user_object = UserProfile.objects.get(user=request.user.pk)
        task_object = Task.objects.get(pk=id_task)
        user_object.my_tasks.add(task_object)
        user_object.save()
        return redirect_to_login('')
    else:
        raise Http404



# Versión alternativa para obtener los resultados como diccionario de Python y no JSON (needs review)
def get_geocoders_results(request):

    if request.is_ajax() and request.method == 'POST':
        dir_solicitada = request.POST['my_address']                                          
        #response_dict = {}                                          
        try:
            location_Google = geocoder.google(dir_solicitada)
            location_Bing = geocoder.bing(dir_solicitada)
            location_MapQuest = geocoder.here(dir_solicitada, app_id='PWQguUtERmkUxTmtHjHX',
                    app_code='dYlmePq5h6xBhq1DYD1Ljw')
            location_OSM = geocoder.osm(dir_solicitada)
            if location_Google.ok == False and location_Bing.ok == False and location_MapQuest == False and location_OSM.ok == False:
                yGoogle = None
                xGoogle = None
                confGoogle = None
                accuGoogle = None
                qualGoogle = None
                yBing = None
                xBing = None
                confBing = None
                accuBing = None
                qualBing = None
                yHere = None
                xHere = None
                confHere = None
                accuHere = None
                qualHere = None
                xOSM = None
                yOSM = None
                confOSM = None
                accuOSM = None
                qualOSM = None
                dir_solicitada = dir_solicitada
                print(dir_solicitada)
                mensaje_alerta =_('No service geocode this location, could you find it on the map!')
                print("Ningún servicio arrojó resultados")
            else:
                dir_solicitada = dir_solicitada
                print(dir_solicitada)
                if location_Google.ok == False: #No Google
                    yGoogle = None
                    xGoogle = None
                    confGoogle = None
                    accuGoogle = None
                    qualGoogle = None
                    print('Google is False')
                    if location_Bing.ok == False: #No Google y Bing
                        yBing = None
                        xBing = None
                        confBing = None
                        accuBing = None
                        qualBing = None
                        if location_MapQuest.ok == False: #Ni Google, ni Bing, ni Here
                            yHere = None
                            xHere = None
                            confHere = None
                            accuHere = None
                            qualHere = None
                            # Al menos uno debe estar por lo tanto Sí OSM
                            yOSM = location_OSM.lat
                            xOSM = location_OSM.lng
                            confOSM = location_OSM.confidence
                            accuOSM = location_OSM.accuracy
                            qualOSM = location_OSM.quality
                            print('Google, Bing and Here are False but OSM not')
                            mensaje_alerta = _('Only OpenStreetMap service has been able to find this location, well at least one, let us see how is going!')
                        else:
                            yHere = location_MapQuest.lat
                            xHere = location_MapQuest.lng
                            confHere = location_MapQuest.confidence
                            accuHere = location_MapQuest.accuracy
                            qualHere = location_MapQuest.quality
                            if location_OSM.ok == False:
                                yOSM = None
                                xOSM = None
                                confOSM = None
                                accuOSM = None
                                qualOSM = None
                                print('Only Here is True')
                                mensaje_alerta = _('Only Here Maps service has been able to find this location, well at least one, let us see how is going!')
                            else:
                                yOSM = location_OSM.lat
                                xOSM = location_OSM.lng
                                confOSM = location_OSM.confidence
                                accuOSM = location_OSM.accuracy
                                qualOSM = location_OSM.quality
                                print('Only Here and OSM are True')
                                mensaje_alerta = _('Here Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                    else:
                        yBing = location_Bing.lat #No Google, Sí Bing
                        xBing = location_Bing.lng
                        confBing = location_Bing.confidence
                        accuBing = location_Bing.accuracy
                        qualBing = location_Bing.quality
                        if location_MapQuest.ok == False: 
                            yHere = None
                            xHere = None
                            confHere = None
                            accuHere = None
                            qualHere = None
                            if location_OSM.ok == False:
                                yOSM = None
                                xOSM = None
                                confOSM = None
                                accuOSM = None
                                qualOSM = None
                                print('Google, Here and OSM are False but Bing not') #No Google, No Here, No OSM, Sí Bing
                                mensaje_alerta = _('Only Bing Maps service has been able to find this location, well at least one, let us see how is going!')
                            else:
                                yOSM = location_OSM.lat
                                xOSM = location_OSM.lng
                                confOSM = location_OSM.confidence
                                accuOSM = location_OSM.accuracy
                                qualOSM = location_OSM.quality
                                print('Google, and Here are False but Bing and OSM not') #No Google, No Here, Sí OSM, Sí Bing
                                mensaje_alerta = _('Bing Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                        else:                                           
                            yHere = location_MapQuest.lat
                            xHere = location_MapQuest.lng # No Google, Sí Bing, Sí Here ¿OSM?
                            confHere = location_MapQuest.confidence
                            accuHere = location_MapQuest.accuracy
                            qualHere = location_MapQuest.quality
                            if location_OSM.ok == False:
                                yOSM = None
                                xOSM = None
                                confOSM = None
                                accuOSM = None
                                qualOSM = None
                                mensaje_alerta = _('Bing Maps and Here Maps services have been able to find this location, let us see how is going!')
                                print("Google and OSM are False but Bing and Here is not")
                            else:
                                yOSM = location_OSM.lat
                                xOSM = location_OSM.lng
                                confOSM = location_OSM.confidence
                                accuOSM = location_OSM.accuracy
                                qualOSM = location_OSM.quality
                                print("Google is False but Bing, Here and OSM is not")
                                mensaje_alerta = _('Bing Maps, Here Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                elif location_Bing.ok == False: #No Bing y Sí Google y ¿Here y OSM?
                    yGoogle = location_Google.lat
                    xGoogle = location_Google.lng
                    confGoogle = location_Google.confidence
                    accuGoogle = location_Google.accuracy
                    qualGoogle = location_Google.quality
                    yBing = None
                    xBing = None
                    confBing = None
                    accuBing = None
                    qualBing = None
                    print('Bing is False but Google not') 
                    if location_MapQuest.ok == False: #Sí Google, No Bing, No Here
                        yHere = None
                        xHere = None
                        confHere = None
                        accuHere = None
                        qualHere = None
                        if location_OSM.ok == False: #Sí Google, No Bing, No Here, No OSM
                            yOSM = None
                            xOSM = None
                            confOSM = None
                            accuOSM = None
                            qualOSM = None
                            mensaje_alerta = _('Only Google Maps service has been able to find this location, well at least one, let us see how is going!')
                            print('Bing, Here and OSM are False but Google not')
                        else:
                            yOSM = location_OSM.lat
                            xOSM = location_OSM.lng
                            confOSM = location_OSM.confidence
                            accuOSM = location_OSM.accuracy
                            qualOSM = location_OSM.quality
                            print('Bing and Here are false but Google and OSM not')
                            mensaje_alerta = _('Google Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                    else:                   #No Bing, Sí Google, Sí Here  ¿OSM?
                        yHere = location_MapQuest.lat
                        xHere = location_MapQuest.lng
                        confHere = location_MapQuest.confidence
                        accuHere = location_MapQuest.accuracy
                        print(accuHere)
                        qualHere = location_MapQuest.quality
                        print(qualHere)
                        if location_OSM.ok == False:
                            yOSM = None
                            xOSM = None
                            confOSM = None
                            accuOSM = None
                            qualOSM = None
                            print("Bing and OSM are False, but Google and Here not")
                            mensaje_alerta = _('Google Maps and Here Maps services have been able to find this location, let us see how is going!')
                        else:
                            yOSM = location_OSM.lat
                            xOSM = location_OSM.lng
                            confOSM = location_OSM.confidence
                            accuOSM = location_OSM.accuracy
                            qualOSM = location_OSM.quality
                            print("Bing are False, but Google, Here and OSM not")
                            mensaje_alerta = _('Google Maps, Here Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                        
                elif location_MapQuest.ok == False: #Sí Google, Sí Bing y ¿Here y OSM?
                    yHere = None
                    xHere = None
                    confHere = None
                    accuHere = None
                    qualHere = None
                    print('Here is false but Google and Bing not')
                    yGoogle = location_Google.lat
                    xGoogle = location_Google.lng
                    confGoogle = location_Google.confidence
                    accuGoogle = location_Google.accuracy
                    qualGoogle = location_Google.quality
                    yBing = location_Bing.lat
                    xBing = location_Bing.lng
                    confBing = location_Bing.confidence
                    accuBing = location_Bing.accuracy
                    qualBing = location_Bing.quality
                    if location_OSM.ok == False:
                        xOSM = None
                        yOSM = None
                        confOSM = None
                        accuOSM = None
                        qualOSM = None
                        print('Here and OSM are false but Google and Bing not')
                        mensaje_alerta = _('Google Maps and Bing Maps services have been able to find this location, let us see how is going!')
                    else:
                        yOSM = location_OSM.lat
                        xOSM = location_OSM.lng
                        confOSM = location_OSM.confidence
                        accuOSM = location_OSM.accuracy
                        qualOSM = location_OSM.quality
                        print('Here is false but Google, Bing and OSM not')
                        mensaje_alerta = _('Google Maps, Bing Maps and OpenStreetMap services have been able to find this location, let us see how is going!')
                elif location_OSM.ok == False:
                    yOSM = None
                    xOSM = None
                    confOSM = None
                    accuOSM = None
                    qualOSM = None
                    print('OSM is false but Google, Bing and Here not')
                    yGoogle = location_Google.lat
                    xGoogle = location_Google.lng
                    confGoogle = location_Google.confidence
                    accuGoogle = location_Google.accuracy
                    qualGoogle = location_Google.quality
                    print(yGoogle, xGoogle)
                    yBing = location_Bing.lat
                    xBing = location_Bing.lng
                    confBing = location_Bing.confidence
                    accuBing = location_Bing.accuracy
                    qualBing = location_Bing.quality
                    print(yBing, xBing)
                    yHere = location_MapQuest.lat
                    xHere = location_MapQuest.lng
                    confHere = location_MapQuest.confidence
                    accuHere = location_MapQuest.accuracy
                    qualHere = location_MapQuest.quality
                    print(yHere, xHere)
                    mensaje_alerta = _('Google Maps, Bing Maps and Here Maps services have been able to find this location, let us see how is going!')
                else:
                    yGoogle = location_Google.lat
                    xGoogle = location_Google.lng
                    confGoogle = location_Google.confidence
                    accuGoogle = location_Google.accuracy
                    qualGoogle = location_Google.quality
                    yBing = location_Bing.lat
                    xBing = location_Bing.lng
                    confBing = location_Bing.confidence
                    accuBing = location_Bing.accuracy
                    qualBing = location_Bing.quality
                    yHere = location_MapQuest.lat
                    xHere = location_MapQuest.lng
                    confHere = location_MapQuest.confidence
                    accuHere = location_MapQuest.accuracy
                    qualHere = location_MapQuest.quality
                    yOSM = location_OSM.lat
                    xOSM = location_OSM.lng
                    confOSM = location_OSM.confidence
                    accuOSM = location_OSM.accuracy
                    qualOSM = location_OSM.quality
                    mensaje_alerta = _('All geocoding services found this address, what location do you think will be the best!')
                    print("Estan los cuatro")
                    print("Resultados Google:")
                    print(yGoogle, xGoogle)
                    #print(location_Google.json)
                    print("Resultados Bing:")
                    print(yBing, xBing)
                    #print(location_Bing.json)
                    print("Resultados Here")
                    print(yHere, xHere)
                    #print(location_MapQuest.json)
                    print("Resultados OSM:")
                    #print(location_OSM.json)
                    print(yOSM, xOSM)
        except Exception as e:
            mensaje_alerta = _('Platform services not available, please try it later.')
            print(e)
            pass
    else:
        dir_solicitada = None
        mensaje_alerta = None
        yGoogle = None
        xGoogle = None
        confGoogle = None
        accuGoogle = None
        qualGoogle = None
        yBing = None
        xBing = None
        confBing = None
        accuBing = None
        qualBing = None
        yHere = None
        xHere = None
        confHere = None
        accuHere = None
        qualHere = None
        xOSM = None
        yOSM = None
        confOSM = None
        accuOSM = None
        qualOSM = None

    my_dictionary = {'yGoogle': yGoogle,'xGoogle': xGoogle, 'confGoogle': confGoogle, 'accuGoogle': accuGoogle, 'qualGoogle': qualGoogle, \
    'yBing': yBing, 'xBing': xBing, 'confBing': confBing, 'accuBing': accuBing, 'qualBing': qualBing, \
    'yHere': yHere, 'xHere': xHere, 'confHere': confHere, 'accuHere': accuHere, 'qualHere': qualHere, \
    'yOSM':yOSM,'xOSM': xOSM, 'confOSM': confOSM, 'accuOSM': accuOSM, 'qualOSM': qualOSM, \
    'dir_solicitada': dir_solicitada,'mensaje_alerta': mensaje_alerta}
    print my_dictionary
    #return render_to_response('app.html', context)  
    return render_to_response('app.html', {'dictionary': my_dictionary}, context_instance=RequestContext(request))                                                               
    #return HttpResponse(response_dict.value.xGoogle)
        
