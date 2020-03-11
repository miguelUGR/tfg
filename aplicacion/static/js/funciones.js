
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
//---------------------circle WITH the point before--------------------------------------------------------------------------------------------------------- 
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


//------------------------------LINE--------------------------------------------------------------------------------------------------------------------------
    var points = [ [-3.69686, 37.115879], [-3.564337, 37.171161] ];

    for (var i = 0; i < points.length; i++) {
        points[i] = ol.proj.transform(points[i], 'EPSG:4326', 'EPSG:3857');
    }

    var featureLine = new ol.Feature({
        geometry: new ol.geom.LineString(points)
    });

    var vectorLine = new ol.source.Vector({});
    vectorLine.addFeature(featureLine);

    var vectorLineLayer = new ol.layer.Vector({
        source: vectorLine,
        style: new ol.style.Style({
            fill: new ol.style.Fill({ color: '#0026ff', weight: 8 }),
            stroke: new ol.style.Stroke({ color: '#0026ff', width: 4 })
        })
    });

    map.addLayer(vectorLineLayer);


//------------------------------------POLYGON-----------------------------------------------------------------------------------------------------------------

// A ring must be closed, that is its last coordinate
// should be the same as its first coordinate.

var ring = [
    //      [0]                     [1]                     [2]                   [3]                     [4]   
    [-4.056662, 37.235149],[-3.661154,37.261385],[-3.773764,37.086306],[ -4.144553,37.077541], [-4.056662, 37.235149]
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
            text: "Wow such label",
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

}

   


