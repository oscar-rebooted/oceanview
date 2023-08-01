let map;

async function initMap() {
    const {Map} = await google.maps.importLibrary('maps');
    
    map = new Map(document.getElementById('map'), {
        zoom: 8,
        center: {lat: 50, lng: 0},
    });
    fetchShipsAndDisplay();
}

async function fetchShipsAndDisplay() {
    const response = await fetch('http://localhost:8000/ships');
    const ships = await response.json();

    ships.forEach(ship => {
        const position = {lat: ship.Latitude, lng: ship.Longitude};
        const rotation = ship.TrueHeading;
        const icon = {
            path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
            scale: 5,
            rotation: rotation, // Rotate the symbol
            fillColor: '#90EE90',
            strokeColor: '#378E37',
            fillOpacity: 1,
            strokeWeight: 1,
        };
        new google.maps.Marker({
            position: position, // Your marker position
            map: map, // Your map instance
            icon: icon
        });
    });
}