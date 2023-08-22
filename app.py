# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import and_ # to join tables
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
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
Session = sessionmaker(bind=engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome! Here are the available routes<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>/api/v1.0/{{start_date}}</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>/api/v1.0/{{start_date}}/{{end_date}}</a><br/>"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session()
    
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    data = {date: prcp for date, prcp in results}
    
    session.close()
    return jsonify(data)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session()
    
    results = session.query(Station.station).all()
    data = [x[0] for x in results]
    session.close()
    return jsonify(data)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session()
    
    # finding the most active station
    most_active_station_id = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]
    
    # most recent date for the most active station
    recent_date = session.query(Measurement.date).filter(Measurement.station == most_active_station_id).order_by(Measurement.date.desc()).first()[0]
    
    # calculating the start date for the previous year of data
    start_date = dt.datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
   
   # query for temperature observations for the most active station for the previous year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= start_date).all()
    
    # extracting temperature observations and creating a JSON list
    data = [{"Date": date, "Temperature": temp} for date, temp in results]
    session.close()
    return jsonify(data)


# start and end routes

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session()
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    data = {"Temperature Minimum": results[0][0], "Temperature Average": results[0][1], "Temeprature Max": results[0][2]}
    
    session.close()
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session()
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    data = {"Temperature Minimum": results[0][0], "Temperature Average": results[0][1], "Temperature Max": results[0][2]}
    
    session.close()
    return jsonify(data)

# Starting the app
if __name__ == "__main__":
    app.run(debug=True)

