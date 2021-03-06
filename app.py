# INITIAL SETUP

# Importing dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Build database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflecting database using ORM
Base = automap_base()
Base.prepare(engine, reflect=True)

# Table variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask app build
app = Flask(__name__)

# APP ROUTING

# Homepage route
@app.route("/")
def homepage():
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>temperatures</a><br/>"
        f"<a href='/api/v1.0/<start>'>start_to_present</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>start_to_end</a><br/>")

# Precipitation summary route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(Measurement.date, func.sum(Measurement.prcp).label('precipitation')).filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).all()
    
    session.close()
    
    all_results = []
    for item in results:
        item_dict = {}
        item_dict[str(item[0])] = item[1]
        all_results.append(item_dict)
    
    return jsonify(all_results)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.station).all()
    
    session.close()
    
    all_results = list(np.ravel(results))
    
    return jsonify(all_results)

# Temperature route
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Station.station==Measurement.station).filter(Station.id == 7).filter(Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    all_results = []
    for item in results:
        item_dict = {}
        item_dict[str(item[0])] = item[1]
        all_results.append(item_dict)
    
    return jsonify(all_results)

@app.route("/api/v1.0/<start>")
def start_to_present(start):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
                            func.avg(Measurement.tobs)).filter(Station.station==Measurement.station).filter(Measurement.date >= start).all()
    
    session.close()
    
    all_results = []
    for item in results:
        item_dict = {}
        item_dict['TMIN'] = item[0]
        item_dict['TMAX'] = item[1]
        item_dict['TAVG'] = item[2]
        all_results.append(item_dict)
        
    return jsonify(all_results)

@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
                            func.avg(Measurement.tobs)).filter(Station.station==Measurement.station).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    all_results = []
    for item in results:
        item_dict = {}
        item_dict['TMIN'] = item[0]
        item_dict['TMAX'] = item[1]
        item_dict['TAVG'] = item[2]
        all_results.append(item_dict)
        
    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)