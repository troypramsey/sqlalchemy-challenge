# INITIAL SETUP

# Importing dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Build database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

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
def precipitation():
    session = Session(engine)
    
    results = session.query(Measurement.date, func.sum(Measurement.prcp).label('precipitation')).filter(Measurement.date >= '2016-08-23').group_by(Measurement.date)
    
    session.close()
    
    all_results = list(np.ravel(results))
    
    return jsonify(all_results)