# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

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

# obtaining data
data = 

@app.route("/")
def home():
    return "Welcome! Here are the available routes... :downemoji:"

@app.route("/api/v1.0/precipitation")
def precipitation():
    # retrieving precipitation data
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    # retrieving stations data
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    # retrieving temperature observations data
    return jsonify(data)

@app.route("/api/v1.0/<start>")
def start(start):
    # retrieving temperature stats from start date
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # retrieving temperature stats from start to end date
    return jsonify(data)

# starting the app
if __name__ == "__main__":
    app.run(debug=True)