from flask import Flask, request, jsonify, abort
from datetime import datetime
from netCDF4 import Dataset
from numpy import array_str, transpose
from scipy.interpolate import interp2d

app = Flask(__name__)

# Add a route for precipitation
@app.route('/precipitation')
def precipitation():
    # Parse request
    datestr = request.args.get('date')
    latstr = request.args.get('latitude')
    lonstr = request.args.get('longitude')

    # Validate input arguments
    if datestr == None or latstr == None or lonstr == None:
        abort(404)

    # Convert inputs
    date = datetime.strptime(datestr, '%Y-%m-%d')
    lat = float(latstr)
    lon = float(lonstr)

    # Open relevant dataset and extract variables/dimensions
    dataset = Dataset(f'{app.root_path}/data/{date.year}.nc')
    latitude = dataset.variables['latitude'][:]
    longitude = dataset.variables['longitude'][:]

    # Get index of requested day
    day = get_day_of_year(date)

    # Extract precipitation record for that day
    precip = transpose(dataset.variables['tp'][day,:,:])

    # Interpolate to requested coordinates
    interp_precip = interp2d(latitude, longitude, precip)

    # Return result
    return jsonify(interp_precip(lat, lon)[0])

def get_day_of_year(datetime_in):
    return (datetime_in - datetime(datetime_in.year, 1, 1)).days

if __name__ == '__main__':
    app.run(port='5002')
