$(document).ready(function(){
  lat_sc = 0
  lng_sc = 0
  id_geo.innerHTML = ''
  map = ""
  res_data = null
  //Function to load address list to geocode
  getAddressList();
  $('#dir_seleccionada2').hide();
  $('#lbl_dir_seleccionada').hide();
  $('#btnGeocoding').hide();
  $("#answerbtn").prop("disabled",true);
  $("#btnUserPoint").prop("disabled",true);
  $("#btnCancel").prop("disabled",true);
  $("#btnGooglePoint").prop("disabled",true);
  $("#btnBingPoint").prop("disabled",true);
  $("#btnHerePoint").prop("disabled",true);
  $("#btnOSMPoint").prop("disabled",true);
  longFinal.innerHTML = ''
  latFinal.innerHTML = ''
  //MAPA - utilizando Mapbox.js y Leaflet//
  //token para acceder a Tile de Mapbox.
  L.mapbox.accessToken = '{{mapbox_api}}';
     
  map = L.mapbox.map('map', null).setView([40.3, -4], 5);

  //CAPAS BASE//
  // WMS CartoCiudad
  var CartoCiudad = L.tileLayer.wms("http://www.cartociudad.es/wms-inspire/direcciones-ccpp?", {
        layers: ['DivisionTerritorial', 'CodigoPostal', 'FondoUrbano','Vial','Portal'],
        format: 'image/png',
        transparent: true,
        maxZoom: 25,           
        attribution: "CartoCiudad © Instituto Geográfico Nacional de España"
      }); 

  //Las opciones para las capas de Google: SATELLITE, ROADMAP, HYBRID o TERRAIN 
  var gglh = new L.Google('HYBRID');
  var ggst = new L.Google('ROADMAP');

  var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 25})

  //var mapbox_streets = L.mapbox.tileLayer('https://api.mapbox.com/v3/mapbox.streets')
  //var mapbox_outdoors = L.mapbox.tileLayer('examples.ik7djhcc')
  var mapbox_sat = L.mapbox.tileLayer('mapbox.satellite')

  var bing = new L.BingLayer('{{bing_api}}');   

  var baseMaps = {
          // "CartoCiudad Portales": CartoCiudad,
          "OpenStreetMap": osm,
          //"Mapbox Calles": mapbox_streets,
          //"Mapbox Topográfico": mapbox_outdoors,
          "Mapbox Satélite": mapbox_sat,
          "Google Satélite": gglh,
          "Google Maps": ggst,
          "Bing Maps": bing,
        };

  digitize_coord = new L.FeatureGroup();
  map.addLayer(digitize_coord);

  map.on('draw:created', function (e) {
        
        var type = e.layerType,
        layer = e.layer;
        digitize_coord.addLayer(layer);

        if (type === 'marker') {
            layer.bindPopup('location suggested!');
            layer.on('dragend', ondragend);
        // Set the initial marker coordinate on load.
        ondragend();
        function ondragend() {
            m = layer.getLatLng();
            longFinal.innerHTML =  m.lng 
            latFinal.innerHTML = m.lat
            lng_sc = String(m.lng.toFixed(6))
            lat_sc = String(m.lat.toFixed(6))
                    }
                }
          });
  
  $("#btnUserPoint").click(function(){

        id_geo.innerHTML = 0

        map.addLayer(digitize_coord);

        var markerDrawer = new L.Draw.Marker(map);     
        markerDrawer.enable();  
            });

  map.addControl(L.mapbox.geocoderControl('mapbox.places', {
          autocomplete: true
      }));
  var editControl = new L.Control.Draw({
              draw: false,
              edit: {
                  featureGroup: digitize_coord
                  }
              }).addTo(map);

  L.control.scale().addTo(map);
  L.control.layers(baseMaps).addTo(map);
  map.addLayer(ggst);  
  //Maps script ends

  $('#listDirecciones').click(function(e){
    //alert($(e.target).text());
    $('#dir_seleccionada2').show();
    $('#lbl_dir_seleccionada').show();
    $('#btnGeocoding').show();
    $('#dir_seleccionada').val($(e.target).text());
    $('#dir_seleccionada2').val($(e.target).text());
  })

  $('#btnGeocoding').click(function getData(){
      //reload addresses
      $('#dir_seleccionada2').hide();
      $('#lbl_dir_seleccionada').hide();
      $('#btnGeocoding').hide();
      longFinal.innerHTML = ''
      latFinal.innerHTML =  ''
      console.log("getting geocoder's results...")
      // AJAX GET
      $.ajax({
            url : "/geocode/", // the endpoint
            type : "GET", // http method
            data: { my_address: $('#dir_seleccionada').val() }, 
            dataType : "json",
            beforeSend: function(){
                 $('#spinner_earth').show()
                    },
            complete: function(){
                 $('#spinner_earth').hide();
                       },
            success: handleData,
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#error_message').html("<div class='alert-box alert radius' data-alert>Oops! Try later please, we have encountered an error: "+errmsg+ 
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
              }

        });
    });
   
  function handleData(data) {

      digitize_coord.clearLayers();
      $("#answerbtn").prop("disabled",false);
      $("#btnUserPoint").prop("disabled",false);
      $("#btnCancel").prop("disabled",false);
      addGeoJsonLayer(data);
      addAttributesData(data);
      selectBestGeocoder(data);
      res_data=data
      console.log(res_data)
    }

    $('#btnCancel').click(function tryAnother(){
      //Aquí debería sumarle una respuesta nula a la dirección seleccionada
      res_data=null
      console.log(res_data)
      $("#answerbtn").prop("disabled",true);
      $("#btnUserPoint").prop("disabled",true);
      $("#btnCancel").prop("disabled",true);
      $("#btnGooglePoint").prop("disabled",true);
      $("#btnBingPoint").prop("disabled",true);
      $("#btnHerePoint").prop("disabled",true);
      $("#btnOSMPoint").prop("disabled",true);
      $("#results_table td").remove()
      $('#g_barText').html('');
      $('#b_barText').html('');
      $('#h_barText').html('');
      $('#o_barText').html('');
      $("#direccion_sol").html('');
      $('#listDirecciones tr').remove();
      getAddressList();
      longFinal.innerHTML = ''
      latFinal.innerHTML = ''
      id_geo.innerHTML = ''
      map.setView(new L.LatLng(40.3, -4),5);
      geocoder_points.clearLayers();
      if (map.hasLayer(digitize_coord)){
        digitize_coord.clearLayers();
      }
    });

});
//Onload page function ends here
function getAddressList(){
  console.log("getting address to crowdgeolocate...")

  // AJAX GET
  $.ajax({
        url : "/get-address/", // the endpoint
        type : "GET", // http method
        data: { task_id: {{object.pk}} },
        dataType : "json",
        beforeSend: function(){
                 $('#spinner_earth').show()
                    },
        complete: function(){
                 $('#spinner_earth').hide();
                       },
        // handle a successful response
        success : function(data) {
          $.each(data, function(i,val){
          //$('#listDirecciones').append('<option value=" ' + val.domicilio +' "><a href="">'+ val.domicilio + '</a></option>');

          $('#listDirecciones').append('<tr class="warning" ><td><span style="color:blue;font-weight:bold;font-size:11px">' + val + '</span></td></tr>');

          });
            console.log("success"); // another sanity check  
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#error_message').html("<div class='alert-box alert radius' data-alert>Oops! Try later please, we have encountered an error: "+errmsg+ 
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  }

  function addGeoJsonLayer(data){
       
       var geocoder_results = '{' + '"type":' + '"FeatureCollection",' +
        '"features":[ ';

          if (data.google_longitude != null && data.google_latitude != null){
              geocoder_results = geocoder_results + 

            '{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.google_longitude + ',' + data.google_latitude + ']},' +
              '"properties":{' + '"title":' + '"Google Maps",' + ' "description":' + '"lat: ' + data.google_latitude + ', lng: ' + data.google_longitude + '"' + ',' + ' "marker-color":' +  ' "#F90101" }}';
              }

          if (data.bing_longitude != null && data.bing_latitude != null){

            if(data.google_longitude == null){ 
              geocoder_results = geocoder_results + 
              '{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.bing_longitude + ',' + data.bing_latitude + ']},' +
              '"properties":{' + '"title":' + '"Bing Maps",' + ' "description":' + '"lat: ' + data.bing_latitude + ', lng: ' + data.bing_longitude + '"'  + ',' + ' "marker-color":' +  ' "#FFAC00" }}';
              } else {
               geocoder_results = geocoder_results + 
              ',{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.bing_longitude + ',' + data.bing_latitude + ']},' +
              '"properties":{' + '"title":' + '"Bing Maps",' + ' "description":' + '"lat: ' + data.bing_latitude + ', lng: ' + data.bing_longitude + '"'  + ',' + ' "marker-color":' +  ' "#FFAC00" }}';
            }
          }

          if (data.here_longitude != null && data.here_latitude != null){
            if(data.google_longitude == null && data.bing_longitude == null){ 
              geocoder_results = geocoder_results + 
              '{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.here_longitude + ',' + data.here_latitude + ']},' +
              '"properties":{' + '"title":' + '"Here Maps",' + ' "description":' + '"lat: ' + data.here_latitude + ', lng: ' + data.here_longitude + '"'  + ',' + ' "marker-color":' +  ' "#0D2B81" }}';
              } else {
                geocoder_results = geocoder_results + 
                ',{' + '"type":' + '"Feature",' + 
                '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.here_longitude + ',' + data.here_latitude + ']},' +
                '"properties":{' + '"title":' + '"Here Maps",' + ' "description":' + '"lat: ' + data.here_latitude + ', lng: ' + data.here_longitude + '"'  + ',' + ' "marker-color":' +  ' "#0D2B81" }}';
              }
            }

          if (data.osm_longitude != null && data.osm_latitude != null){
            if(data.google_longitude == null && data.bing_longitude == null && data.here_longitude == null){
              geocoder_results = geocoder_results + 
              '{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.osm_longitude + ',' + data.osm_latitude + ']},' +
              '"properties":{' + '"title":' + '"OSM",' + ' "description":' + '"lat: ' + data.osm_latitude + ', lng: ' + data.oms_longitude + '"'  + ',' + ' "marker-color":' +  ' "#2E2B2E" }}';
            } else {
              geocoder_results = geocoder_results + 
              ',{' + '"type":' + '"Feature",' + 
              '"geometry":{' + '"type":' + '"Point",' + '"coordinates":[' + data.osm_longitude + ',' + data.osm_latitude + ']},' +
              '"properties":{' + '"title":' + '"OSM",' + ' "description":' + '"lat: ' + data.osm_latitude + ', lng: ' + data.oms_longitude + '"'  + ',' + ' "marker-color":' +  ' "#2E2B2E" }}';
              }
            }
 
          geocoder_results = geocoder_results + ']}';
          console.log(geocoder_results)
          var geojson_res = JSON.parse(geocoder_results);
          console.log(geojson_res);
          geocoder_points = map.featureLayer.setGeoJSON(geojson_res);
          //Fit the map to the bounds.
          map.fitBounds(geocoder_points);


    }

  function addAttributesData(data){

        $("#results_table td").remove()
        $("#direccion_sol").html(data.address_requested);
        $("#user_message").html(data.result_message);
        $("#user_message").fadeIn();
        setTimeout(function() { $("#user_message").fadeOut();}, 2000);
                        
    //Change color, value of the result's progress bars and display attributes data
        if (data.google_latitude != null ){
          $("#btnGooglePoint").prop("disabled",false);
          $("#results_table").find('#google_data')
                .append($('<td><h5><small><strong>' + '{% trans "Coordinates:" %}' + '</small></strong></h5><p>'+ data.google_latitude.toFixed(6) + ', ' + data.google_longitude.toFixed(6) + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Accuracy:" %}' + '</small></strong></h5><p>'+ data.google_accuracy + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Quality:" %}' + '</small></strong></h5><p>'+ data.google_quality + '</p></td>')
            );

        switch (data.google_confidence) {
          case 0:
          case 1:
          case 2:
          case 3:
              $('#confBarGoogle').css('width', data.google_confidence*10+'%').attr('aria-valuenow', data.google_confidence);
              $('#confBarGoogle').removeClass().addClass("progress-bar progress-bar-danger");
              $('#g_barText').html('{% trans "Confidence: " %}' + data.google_confidence);
              break;
          case 4:
          case 5:
          case 6:
          case 7:
              $('#confBarGoogle').css('width', data.google_confidence*10+'%').attr('aria-valuenow', data.google_confidence);
              $('#confBarGoogle').removeClass().addClass("progress-bar progress-bar-warning");
              $('#g_barText').html('{% trans "Confidence: " %}' + data.google_confidence);
              break;
          default:
              $('#confBarGoogle').css('width', data.google_confidence*10+'%').attr('aria-valuenow', data.google_confidence);
              $('#confBarGoogle').removeClass().addClass("progress-bar progress-bar-success");
              $('#g_barText').html('{% trans "Confidence: " %}' + data.google_confidence);
              break;
          }}
          else {
            $("#btnGooglePoint").prop("disabled",true);
            $('#g_barText').html('');
          }
      
        if (data.bing_latitude != null){
          $("#btnBingPoint").prop("disabled",false);
          $("#results_table").find('#bing_data')
                .append($('<td><h5><small><strong>' + '{% trans "Coordinates:" %}' + '</small></strong></h5><p>'+ data.bing_latitude.toFixed(6) + ', ' + data.bing_longitude.toFixed(6) + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Accuracy:" %}' + '</small></strong></h5><p>'+ data.bing_accuracy + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Quality:" %}' + '</small></strong></h5><p>'+ data.bing_quality + '</p></td>')
            );

        switch (data.bing_confidence) {
          case 0:
          case 1:
          case 2:
          case 3:
              $('#confBarBing').css('width', data.bing_confidence*10+'%').attr('aria-valuenow', data.bing_confidence);
              $('#confBarBing').removeClass().addClass("progress-bar progress-bar-danger");
              $('#b_barText').html('{% trans "Confidence: " %}' + data.bing_confidence);
              break;
          case 4:
          case 5:
          case 6:
          case 7:
              $('#confBarBing').css('width', data.bing_confidence*10+'%').attr('aria-valuenow', data.bing_confidence);
              $('#confBarBing').removeClass().addClass("progress-bar progress-bar-warning");
              $('#b_barText').html('{% trans "Confidence: " %}' + data.bing_confidence);
              break;
          default:
              $('#confBarBing').css('width', data.bing_confidence*10+'%').attr('aria-valuenow', data.bing_confidence);
              $('#confBarBing').removeClass().addClass("progress-bar progress-bar-success");
              $('#b_barText').html('{% trans "Confidence: " %}' + data.bing_confidence);
              break;
          }}

          else {
            $("#btnBingPoint").prop("disabled",true);
            $('#b_barText').html('');
          }
        
        if (data.here_latitude != null){
          $("#btnHerePoint").prop("disabled",false);
          $("#results_table").find('#here_data')
                .append($('<td><h5><small><strong>' + '{% trans "Coordinates:" %}' + '</small></strong></h5><p>'+ data.here_latitude.toFixed(6) + ', ' + data.here_longitude.toFixed(6) + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Accuracy:" %}' + '</small></strong></h5><p>'+ data.here_accuracy + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Quality:" %}' + '</small></strong></h5><p>'+ data.here_quality + '</p></td>')
            );

        switch (data.here_confidence) {
          case 0:
          case 1:
          case 2:
          case 3:
              $('#confBarHere').css('width', data.here_confidence*10+'%').attr('aria-valuenow', data.here_confidence);
              $('#confBarHere').removeClass().addClass("progress-bar progress-bar-danger");
              $('#h_barText').html('{% trans "Confidence: " %}' + data.here_confidence);
              break;
          case 4:
          case 5:
          case 6:
          case 7:
              $('#confBarHere').css('width', data.here_confidence*10+'%').attr('aria-valuenow', data.here_confidence);
              $('#confBarHere').removeClass().addClass("progress-bar progress-bar-warning");
              $('#h_barText').html('{% trans "Confidence: " %}' + data.here_confidence);
              break;
          default:
              $('#confBarHere').css('width', data.here_confidence*10+'%').attr('aria-valuenow',data.here_confidence);
              $('#confBarHere').removeClass().addClass("progress-bar progress-bar-success");
              $('#h_barText').html('{% trans "Confidence: " %}' + data.here_confidence);
              break;
          }}
          else {
            $("#btnHerePoint").prop("disabled",true);
            $('#h_barText').html('');
          }
       
        if (data.osm_latitude != null){
          $("#btnOSMPoint").prop("disabled",false);
          $("#results_table").find('#osm_data')
                .append($('<td><h5><small><strong>' + '{% trans "Coordinates:" %}' + '</small></strong></h5><p>'+ data.osm_latitude.toFixed(6) + ', ' + data.osm_longitude.toFixed(6) + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Accuracy:" %}' + '</small></strong></h5><p>'+ data.osm_accuracy + '</p></td>' + '<td><h5><small><strong>' + '{% trans "Quality:" %}' + '</small></strong></h5><p>'+ data.osm_quality + '</p></td>')
            );
        switch (data.osm_confidence) {
          case 0:
          case 1:
          case 2:
          case 3:
              $('#confBarOSM').css('width', data.osm_confidence*10+'%').attr('aria-valuenow', data.osm_confidence);
              $('#confBarOSM').removeClass().addClass("progress-bar progress-bar-danger");
              $('#o_barText').html('{% trans "Confidence: " %}' + data.osm_confidence);
              break;
          case 4:
          case 5:
          case 6:
          case 7:
              $('#confBarOSM').css('width', data.osm_confidence*10+'%').attr('aria-valuenow', data.osm_confidence);
              $('#confBarOSM').removeClass().addClass("progress-bar progress-bar-warning");
              $('#o_barText').html('{% trans "Confidence: " %}' + data.osm_confidence);
              break;
          default:
              $('#confBarOSM').css('width', data.osm_confidence*10+'%').attr('aria-valuenow', data.osm_confidence);
              $('#confBarOSM').removeClass().addClass("progress-bar progress-bar-success");
              $('#o_barText').html('{% trans "Confidence: " %}' + data.osm_confidence);
              break;
          }}
          else {
            $("#btnOSMPoint").prop("disabled",true);
            $('#o_barText').html('');
          }
    }
  
  function selectBestGeocoder(data){

          //If Google is selected
          $("#btnGooglePoint").click(function(){
            
              longFinal.innerHTML =  data.google_longitude
              latFinal.innerHTML =  data.google_latitude
              id_geo.innerHTML =  1

              });

          //If Bing is selected
          $("#btnBingPoint").click(function(){
            
              longFinal.innerHTML = data.bing_longitude
              latFinal.innerHTML =  data.bing_latitude
              id_geo.innerHTML =  2

              });

          //If Here is selected
          $("#btnHerePoint").click(function(){
            
              longFinal.innerHTML =  data.here_longitude
              latFinal.innerHTML =  data.here_latitude
              id_geo.innerHTML =  3

              });

          //If OSM is selected
          $("#btnOSMPoint").click(function(){
            
              longFinal.innerHTML = data.osm_longitude
              latFinal.innerHTML =  data.osm_latitude
              id_geo.innerHTML =  4

              });
    }

  /*function saveGeocodersData(data){*/
    //User send the results to database
    $("#answerbtn").click(function(event){

      event.preventDefault();
      if (id_geo.innerHTML == '') {
        alert("Please select one geocoder service on the results panel, as the best location for the input address");
      }
      else{
         console.log("task-data submitted!")  // sanity check
         answer_task_post();
      }
      // AJAX for posting
      function answer_task_post() {
          var None
          None = ''
          $("#user_message").html("we are sending the data...");
          $("#user_message").fadeIn();
          setTimeout(function() { $("#user_message").fadeOut();}, 3000);
          console.log("working...") // sanity check
          //console.log()

          $.ajax({
              url : "/save-answer/", // the endpoint
              type : "POST", // http method
              data : { task_id: {{object.pk}}, direccion_sol : res_data.address_requested, id_geo: $('#id_geo').text(), xGoogle : res_data.google_longitude , yGoogle: res_data.google_latitude, accuGoogle: res_data.google_accuracy , qualGoogle: res_data.google_quality, confGoogle: res_data.google_confidence, xBing : res_data.bing_longitude , yBing: res_data.bing_latitude, accuBing: res_data.bing_accuracy, qualBing: res_data.bing_quality, confBing: res_data.bing_confidence, xHere : res_data.here_longitude , yHere: res_data.here_latitude, accuHere: res_data.here_accuracy, qualHere: res_data.here_quality, confHere: res_data.here_confidence, xOSM : res_data.osm_longitude , yOSM: res_data.osm_latitude, accuOSM: res_data.osm_accuracy, qualOSM: res_data.osm_quality, confOSM: res_data.osm_confidence, csX: lng_sc, csY: lat_sc, csrfmiddlewaretoken: '{{ csrf_token }}' }, // data sent with the post request
              beforeSend: function(){
                 $('#spinner_earth').show()
                    },
              complete: function(){
                 $('#spinner_earth').hide();
                       },
              // handle a successful response
              success : function() {
                  $("#success").fadeIn();
                  setTimeout(function() { $("#success").fadeOut();}, 5000);
                  console.log("success"); // another sanity check
                  $("#answerbtn").prop("disabled",true);
                  $("#btnUserPoint").prop("disabled",true);
                  $("#btnCancel").prop("disabled",true);
                  $("#btnGooglePoint").prop("disabled",true);
                  $("#btnBingPoint").prop("disabled",true);
                  $("#btnHerePoint").prop("disabled",true);
                  $("#btnOSMPoint").prop("disabled",true);
                  $("#results_table td").remove()
                  $('#g_barText').html('');
                  $('#b_barText').html('');
                  $('#h_barText').html('');
                  $('#o_barText').html('');
                  $("#direccion_sol").html('');
                  $('#listDirecciones tr').remove();
                  getAddressList();
                  id_geo.innerHTML = ''
                  longFinal.innerHTML = ''
                  latFinal.innerHTML = ''
                  map.setView(new L.LatLng(40.3, -4),5);
                  geocoder_points.clearLayers();
                  if (map.hasLayer(digitize_coord)){
                    digitize_coord.clearLayers();
                  }
              },

              // handle a non-successful response
              error : function(xhr,errmsg,err) {
                  $('#error_message').html("<div class='alert-box alert radius' data-alert>Oops! Try later please, we have encountered an error: "+errmsg+ 
                      " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                  console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
              });
          };
    });

/*}*/

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
