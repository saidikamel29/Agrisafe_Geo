import ee
ee.Authenticate()
ee.Initialize()

import ee
from flask import Flask, jsonify

ee.Initialize()

app = Flask(__name__)


# Route: Rainfall Map
@app.route("/rainfall")
def rainfall():

    # 1. Tipaza geometry
    admin = ee.FeatureCollection("FAO/GAUL/2015/level1")

    tipaza = admin \
        .filter(ee.Filter.eq('ADM0_NAME', 'Algeria')) \
        .filter(ee.Filter.eq('ADM1_NAME', 'Tipaza')) \
        .geometry()

    # 2. CHIRPS rainfall dataset
    chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")

    # 3. Time period
    start = "2023-01-01"
    end = "2023-12-31"

    # 4. Rain calculation (total rainfall)
    rain = chirps \
        .filterDate(start, end) \
        .sum() \
        .clip(tipaza)

    # 5. Visualization
    vis = {
        "min": 0,
        "max": 800,
        "palette": ["white", "lightblue", "blue", "darkblue"]
    }

    # 6. Convert to tile layer (IMPORTANT for frontend)
    map_id = rain.getMapId(vis)

    return jsonify({
        "tile_url": map_id["tile_fetcher"].url_format,
        "min": 0,
        "max": 800,
        "unit": "mm"
    })


# Run server

if __name__ == "__main__":
    app.run(debug=True)