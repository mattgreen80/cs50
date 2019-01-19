
// Google map for about page
let map;

$(document).ready(function() {

    // Options for map
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    let options = {
        center: {lat: -36.8483, lng: 174.7671}, // Auckland, New Zealand
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: true,
       zoom: 10,
       zoomControl: true
   };

    // Make sure the map-canvas tag is actually present on the page (i.e. if on about page)
    if ($("#map-canvas").length > 0){
        //Get DOM node in which map will be instantiated
        let canvas = $("#map-canvas").get(0);
        // instantiate map
        map = new google.maps.Map(canvas, options);
    }

});