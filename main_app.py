from flask import Flask, request, jsonify
from iris import load_cube, Constraint
from iris.analysis import Linear
from datetime import datetime

app = Flask(__name__)

# Add a route for precipitation
@app.route('/precipitation')
def precipitation():
    # Parse request
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')

    # Open relevant cube
    cube = load_cube(f'{date.year}.nc', 'Total precipitation').extract(Constraint(time=date))

    # Interpolate to requested coordinates
    precip = 1000.0*cube.interpolate([('latitude', lat), ('longitude', lon)], Linear()).data

    # Return result
    return jsonify(precip)

if __name__ == '__main__':
    app.run(port='5002')
