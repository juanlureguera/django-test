var routeDetails = [];
var precio;
var tiempo;
var distancia;

function getDistancia(){
	return tiempo;
}
function getTiempo(){
	return distancia;
}
function getPrecio(){
	return precio;
}
function getRouteOrigin(){
	return routeDetails[0].formatted_address;
}
function getRouteDestinity(){
	return routeDetails[1].formatted_address;
}
function initMap( ) {

	var origin_place_id = null;
	var destination_place_id = null;
	var travel_mode = google.maps.TravelMode.DRIVING;
	var map = new google.maps.Map(document.getElementById('map2'), {

		mapTypeControl: false,
		center: {lat: 36.51284, lng: -6.28188},
		zoom: 11
	});

	var directionsService = new google.maps.DirectionsService;
	var directionsDisplay = new google.maps.DirectionsRenderer;
	directionsDisplay.setMap(map);

	var origin_input = document.getElementById('origin-input');
	var destination_input = document.getElementById('destination-input');
	var modes = document.getElementById('mode-selector');

	map.controls[google.maps.ControlPosition.TOP_LEFT].push(origin_input);
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(destination_input);
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(modes);

	var origin_autocomplete = new google.maps.places.Autocomplete(origin_input);
	origin_autocomplete.bindTo('bounds', map);
	var destination_autocomplete = new google.maps.places.Autocomplete(destination_input);
	destination_autocomplete.bindTo('bounds', map);


	function expandViewportToFitPlace(map, place) {
		if (place.geometry.viewport) {
			map.fitBounds(place.geometry.viewport);
		} else {
			map.setCenter(place.geometry.location);
			map.setZoom(17);
		}
	}

	origin_autocomplete.addListener('place_changed', function() {
		var place = origin_autocomplete.getPlace();
		routeDetails[0]=place;
		if (!place.geometry) {
			window.alert("Autocomplete's returned place contains no geometry");
			return;
		}
		expandViewportToFitPlace(map, place);

		// If the place has a geometry, store its place ID and route if we have
		// the other place ID
		origin_place_id = place.place_id;
		route(origin_place_id, destination_place_id, travel_mode,
		directionsService, directionsDisplay);
	});

	destination_autocomplete.addListener('place_changed', function() {
		var place = destination_autocomplete.getPlace();
		routeDetails[1]=place; 
		if (!place.geometry) {
			window.alert("Autocomplete's returned place contains no geometry");
			return;
		}
		expandViewportToFitPlace(map, place);

		// If the place has a geometry, store its place ID and route if we have
		// the other place ID
		destination_place_id = place.place_id;
		route(origin_place_id, destination_place_id, travel_mode,
		directionsService, directionsDisplay);
	});

	//Ruta
	function route(origin_place_id, destination_place_id, travel_mode,
	directionsService, directionsDisplay) {
		if (!origin_place_id || !destination_place_id) {
			return;
		}
		directionsService.route({
			origin: {'placeId': origin_place_id},
			destination: {'placeId': destination_place_id},
			travelMode: travel_mode
			}, function(response, status) {
				if (status === google.maps.DirectionsStatus.OK) {
				getDistance(routeDetails);
				directionsDisplay.setDirections(response);
			} else {
				window.alert('Directions request failed due to ' + status);
			}
		});
	}
	//Get distance beetwen two points
	function getDistance ( routeDetails ) {
		getDate(false);
		getHour();
		$('#modal-route').modal('show');
		//Origin pos
		var im = new google.maps.LatLng(routeDetails[0].geometry.location.lat(), routeDetails[0].geometry.location.lng());
		//Destination pos
		var goto = new google.maps.LatLng(routeDetails[1].geometry.location.lat(), routeDetails[1].geometry.location.lng());
		service = new google.maps.DistanceMatrixService();
		service.getDistanceMatrix(
		{
			origins: [im],
			destinations: [goto],
			travelMode: google.maps.TravelMode.DRIVING,
			avoidHighways: false,
			avoidTolls: false
		}, 
		callback
	);
	function callback(response, status) {        
		if ( status == "OK" ) {
			distancia = response.rows[0].elements[0].distance.value;
			jQuery("label[for='distance-label']").html( response.rows[0].elements[0].distance.text );
			tiempo = response.rows[0].elements[0].duration.value
			jQuery("label[for='duration-label']").html( response.rows[0].elements[0].duration.text );
			precio = response.rows[0].elements[0].distance.value/1000;
			precio = Math.round(precio*100)/100;
			console.log(precio)
			if( precio < 6){
			    precio = 6.00;
			}
			jQuery("label[for='price-label']").html( precio +"€");

		} else {
			alert( "Error: " + status );
		}
	}
	
}
var styles = [ {
	stylers: [
		{ hue: "#00ffe6" },
		{ saturation: -20 }
	]
},{
	featureType: "road",
	elementType: "geometry",
	stylers: [
		{ lightness: 100 },
		{ visibility: "simplified" }
	]
},{
	featureType: "road",
	elementType: "labels",
	stylers: [
		{ visibility: "off" }
	]
} ];
	map.setOptions({styles: styles});
}
