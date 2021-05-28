import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for Home Page...")
    return ("Welcome to my Home Page<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/'start'<br/>"
    f"/api/v1.0/'start'/'end'"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation_dict = {}
    precipitation_dict  = {date:prcp for date,prcp in results}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()

    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temperature():

    session = Session(engine)
    alt_result = session.query(Measurement.station).all()

    def most_frequent(List):
        counter = 0
        num = List[0]

        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i

        return num
    most_active_station = most_frequent(alt_result)
    most_active_station = list(most_active_station)
    most_active_station = most_active_station[0]

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date= list(most_recent_date)
    most_recent_date= most_recent_date[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')

    year_ago = most_recent_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.station,Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date <= most_recent_date).filter(Measurement.date >= year_ago).all()

    session.close()

    specific_tobs = list(np.ravel(results))
    return jsonify(specific_tobs)


if __name__ == "__main__":
    app.run(debug=True)
