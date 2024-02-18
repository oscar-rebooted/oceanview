function initMap() {
    // The location of Uluru
    const uluru = {lat: -25.344, lng: 131.036};
    const direction = 180;
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: uluru
    });

    const marker = new google.maps.Marker({
        position: uluru, // Your marker position
        map: map, // Your map instance
        icon: {
            path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW, // Example using a predefined path
            // For custom SVG path, replace the value of 'path' with your SVG path commands as a string.
            scale: 5,
            rotation: 256, // Rotate the symbol
            fillColor: '#90EE90',
            strokeColor: '#378E37',
            fillOpacity: 1,
            strokeWeight: 1,
        }
    });
}