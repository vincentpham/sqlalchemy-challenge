# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import and_ # to join tables
import datetime as dt # in case i need to convert date time formatting


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# Save references to each table 
# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")

# date as the key
# prcp as the value

@app.route("/api/v1.0/<start>")

# def start(start):
    # try:
       #  dt.datetime.strptime(start, '%Y-%m-%d')
        # results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        # data = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
       #  return jsonify(data)
    # except ValueError:
       #  return jsonify({"error": "Invalid date format. Please use 'YYYY-MM-DD'."}), 400

def home():
    return "Welcome! Here are the available routes... :downemoji:"

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    
    data = {}
    for date, prcp in results:
        data[date] = prcp

    return jsonify(data)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    data = []
    
    for x in results:
        data.append(x[0])
        
    return jsonify(data)

# temperature observation stations route
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]
    recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_station_id).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= start_date).all()

    data = []
    for temp in results:
        data.append(temp[0])

    return jsonify(data)

# @app.route("/api/v1.0/tobs")
# def tobs():
    # Most active station ID
    # most_active_station_id = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]
    # recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_station_id).order_by(Measurement.date.desc()).first()[0]
    # start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Joining measurement and station tables
    # results = session.query(Measurement.tobs, Station.name, Station.latitude, Station.longitude).\
        # join(Station, Measurement.station == Station.station).\
        # filter(and_(Measurement.station == most_active_station_id, Measurement.date >= start_date)).all()

    # Processing the data as needed
    # data = [{"Temperature": temp, "Station Name": name, "Latitude": lat, "Longitude": lon} for temp, name, lat, lon in results]

    # return jsonify(data)


# start and end routes

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    data = {"Temperature Minimum": results[0][0], "Temperature Average": results[0][1], "Temeprature Max": results[0][2]}
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    data = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    return jsonify(data)

# Starting the app
if __name__ == "__main__":
    app.run(debug=True)
    
# defining queries for each of the routes