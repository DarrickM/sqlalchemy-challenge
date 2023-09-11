# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def welcome():

    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startEnd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query(measurement.prcp,
                            measurement.date).filter(measurement.date>='2016-08-23').order_by(measurement.date).all()

    session.close()
    
    precipitation = []
    for x in results:
        prcpData = {}
        prcpData["Date"] = x.date
        prcpData["Precipitation"] = x.prcp
        precipitation.append(prcpData)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(station.name).all()

    session.close()

    stationsA = list(np.ravel(results))

    return jsonify(stationsA)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    
    results = session.query((measurement.date),
                          measurement.tobs).filter(measurement.station=='USC00519281').order_by(measurement.date>='2016-08-23').all()
    
    session.close()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/start")
def start():
    
    startDate = input(f"Enter a start date.")


    session = Session(engine)

    results = session.query(func.min(measurement.tobs),
                            func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= startDate).all()

    session.close()

    tempStart = []

    for Tmin, Tave, Tmax in results:
        tempStartD = {}
        tempStartD["TMIN"] = Tmin
        tempStartD["TAVE"] = Tave
        tempStartD["TMAX"] = Tmax
        tempStart.append(tempStartD)

    return jsonify (tempStart)

@app.route("/api/v1.0/startEnd")
def startEnd():

    startDate = input(f"Enter start date.")
    endDate = input(f"Enter end date.")

    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= startDate).filter(measurement.date <= endDate).all()

    session.close()
    
    tempStartEnd = []

    for Tmin, Tave, Tmax in results:
        tempStartEndD = {}
        tempStartEndD["TMIN"] = Tmin
        tempStartEndD["TAVE"] = Tave
        tempStartEndD["TMAX"] = Tmax
        tempStartEnd.append(tempStartEndD)

    return jsonify (tempStartEnd)   

if __name__ == '__main__':
    app.run(debug=True)