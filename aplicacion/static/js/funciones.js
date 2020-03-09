
function add_map_point(lon, lat,radio) {
    var vectorLayer = new ol.layer.Vector({
    source:new ol.source.Vector({
    features: [new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.transform([parseFloat(lon), parseFloat(lat)], 'EPSG:4326', 'EPSG:3857')), // Esas cordenadas se las pongo a mano, que es donde estan todos los restaurantes, en NEW YORK,ojo con el orden de lat y lng
    })]
    }),
    style: new ol.style.Style({
    image: new ol.style.Icon({
    anchor: [0.5, 0.5],
    anchorXUnits: "fraction",
    anchorYUnits: "fraction",
    src: "https://upload.wikimedia.org/wikipedia/commons/e/ec/RedDot.svg"
    })
    })
    });
   
    map.addLayer(vectorLayer);

    var layer = new ol.layer.Vector({
        source:new ol.source.Vector({
        features: [new ol.Feature({
        geometry: new ol.geom.Circle(ol.proj.transform([parseFloat(lon), parseFloat(lat)], 'EPSG:4326', 'EPSG:3857'), parseFloat(radio)), // Esas cordenadas se las pongo a mano, que es donde estan todos los restaurantes, en NEW YORK,ojo con el orden de lat y lng
        })]
        }),
        style: [
        new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'blue',
                width: 3
            }),
            fill: new ol.style.Fill({
                color: 'rgba(0, 0, 255, 0.1)'
            })
        })]

    });

    map.addLayer(layer);

    }

   


