
function add_map_point(lon, lat,radio,nombre) {
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
    
//---------------------circle WITH the point before--------------------------------------------------------------------------------------------------------- 
    

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




//------------------------------------------ICONO CON TEXTO EH IMAGEN-----------------------------------------------------------------------------------------------------------
 


var mapVectorSource = new ol.source.Vector({
    features: []
});
var mapVectorLayer = new ol.layer.Vector({
    source: mapVectorSource
});
map.addLayer(mapVectorLayer);

function makeMovable(feature) {
    var modify = new ol.interaction.Modify({
        features: new ol.Collection([feature])
    });

    feature.on('change',function() {
        console.log('Feature Moved To:' + this.getGeometry().getCoordinates());
    }, feature);
    return modify;
}

function createMarker(location, style){
    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(location)
    });
    iconFeature.setStyle(style);

    return iconFeature
}

iconStyle = [
    new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
            anchor: [0.5, 1],
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            src: 'https://openlayers.org/en/v3.20.1/examples/data/icon.png',  //EL ICONO ELEGIDO
        }))
    }),
    new ol.style.Style({  
        text: new ol.style.Text({
            text: nombre,
            offsetY: -55,               //MOVEMOS EL TEXTO ARRIBA O ABAJO
            fill: new ol.style.Fill({
                color: '#bf1d94'        //COLOR DEL TEXTO
            })
        })
    })
];
var marker = createMarker(ol.proj.transform([parseFloat(lon), parseFloat(lat)], 'EPSG:4326', 'EPSG:3857'), iconStyle);
mapVectorSource.addFeature(marker);
var modifyInteraction = makeMovable(marker);
map.addInteraction(modifyInteraction);



// var popup = new ol.Overlay.Popup();
// map.addOverlay(popup);
// popup.show(evt.coordinate, '<div><h2>Coordinates</h2><p>' + coor + '</p></div>');
}







function observaciones()
{
    //------------------------------------POLYGON-----------------------------------------------------------------------------------------------------------------

// A ring must be closed, that is its last coordinate
// should be the same as its first coordinate.

var ring = [
    //      [0]                     [1]                     [2]                   [3]                     [4]   
    [-8.944501, 37.01262],[0.224361,38.7532131],[0.77489,37.5994],[ -8.83798,35.8064677], [-8.944501, 37.01262]
];
  
// A polygon is an array of rings, the first ring is
// the exterior ring, the others are the interior rings.
// In your case there is one ring only.
var polygon = new ol.geom.Polygon([ring]);

// Create feature with polygon.
var feature = new ol.Feature(polygon);
polygon.transform('EPSG:4326', 'EPSG:3857');
// Create vector source and the feature to it.
var vectorSource = new ol.source.Vector();
vectorSource.addFeature(feature);

// Create vector layer attached to the vector source.
var vectorLayer = new ol.layer.Vector({
  source: vectorSource,
  style: new ol.style.Style({
     fill: new ol.style.Fill({ color: 'rgba(255, 255, 0, 0.2)', weight: 8 }),  //no que lo rellene
    stroke: new ol.style.Stroke({ color: '#ff0000', width: 3 })
})
});

// Add the vector layer to the map.
map.addLayer(vectorLayer);

}







   


