## Imports ###
from flask import Flask, render_template, request, redirect, url_for
from overpass_wrapper import overpy_extractor
import simplekml

## Global Variables ##
app = Flask(__name__)

bounded_box = [1.0, 1.0, 1.0, 1.0]

## Web Pages ##

# root webpage
@app.route("/")
@app.route('/box')
def bounding_box():
    return render_template("box.html")


# waypoint extractor and map drawer
@app.route('/drawMap')
def extract():
    global bounded_box
    op = overpy_extractor(bounded_box)
    coord_dict = []
    coord_dict = op.extract()
    # error handler for not enough informations selected
    if coord_dict == 101:
        return redirect(url_for("error101"))
    elif coord_dict == 102:
        return redirect(url_for("error102"))
    else:
        draw_array = []
        print("coord_dict")
        print(coord_dict)
        # converting coord_dict into the format need for route rendering
        for i in range(0, len(coord_dict) - 1):
            line = [[str(coord_dict[i][1]), str(coord_dict[i][0])],
                    [str(coord_dict[i + 1][1]), str(coord_dict[i + 1][0])]]
            draw_array.append(line)
        return render_template("drawer.html", draw_array=draw_array, bbox=bounded_box)


# error renderer
@app.route('/error101')
def error101():
    return render_template("error101.html")

# error renderer
@app.route('/error102')
def error102():
    return render_template("error102.html")


## Request Handler ##
# request handler for bounded_box info
@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    data = request.json
    bbox = data[0]
    global bounded_box  # n w s e
    # important ordering converting open layers to overpass ready bbox
    bounded_box = [bbox['min_y'], bbox['min_x'], bbox['max_y'], bbox['max_x']]  # DO NOT ALTER
    return ''

@app.route('/convertCoordsToKML', methods=['POST'])
def convertCoordsToKML():
    kml = simplekml.Kml()
    data = request.get_json()
    coords = data['array']

    coords = [(i, j, 20) for i,j in coords]

    for i, coord in enumerate(coords):
        kml.newpoint(name=str(i), coords=[coord])  # lon, lat, optional height
    response = kml.kml()
    return response


## App Handler ##
# function that starts web app
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
