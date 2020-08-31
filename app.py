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