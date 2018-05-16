#-*-coding:utf-8-*-

from flask import Flask, jsonify, render_template, Response
from flask_restful import Resource, Api, reqparse, abort
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


app = Flask(__name__)
api = Api(app)

# Read csv file
df = pd.read_csv("daily.csv", dtype={"DATE": np.str})
table = df.to_dict(orient="records")


def get_record_by_date(date):
 # Find record by date from the dataset
    for record in table:
        if record.get("DATE") == date:
            return record
    return None


def find_previous_year_in_record(date):
    # Find previous year in the record if a future date is given
    if get_record_by_date(date) == None:
        date = list(date)
        if date[3] != '0':
            date[3] = str(int(date[3]) - 1)  # change year
            date = ''.join(date)
            return find_previous_year_in_record(date)
        else:
            date[2] = str(int(date[2]) - 1)  # change year
            date[3] = '9'
            date = ''.join(date)
            return find_previous_year_in_record(date)
    else:
        return date


def get_seven_days_weather(date):
    # Get seven-day's weather by giving a date in the record
    records = []
    for day in range(7):
        records.append(get_record_by_date(date))
        date = datetime.strptime(date, '%Y%m%d') + timedelta(days=1)
        date = date.strftime('%Y%m%d')
    return records


def replace_to_current_date(date, records):
    # Replace previous weather with the current date
    forecast = []
    for record in records:
        forecast.append({"DATE": date, "TMAX": record["TMAX"], "TMIN": record["TMIN"]})
        date = datetime.strptime(date, '%Y%m%d') + timedelta(days=1)
        date = date.strftime('%Y%m%d')
    return forecast


parser = reqparse.RequestParser()
parser.add_argument("DATE", type=str, required=True, help="Invalid Date")
parser.add_argument("TMAX", type=float, required=True, help="Invalid Temperature")
parser.add_argument("TMIN", type=float, required=True, help="Invalid Temperature")


class Home(Resource):
    def get(self):
        # This is the homepage for the api
        return "This is Siqi's Weather API"


class WeatherList(Resource):

    def get(self):
        results = []
        for row in table:
            results.append({"DATE": row.get("DATE")})
        return Response(json.dumps(results), mimetype='application/json')

    def post(self):
        args = parser.parse_args()
        date, tmax, tmin = args["DATE"], args["TMAX"], args["TMIN"]
        table.append(args)
        return {'DATE': str(date)}, 201


class Weather(Resource):

    def get(self, date):
        record = get_record_by_date(date)
        if record == None:
            abort(404)
        else:
            return jsonify(DATE=record["DATE"],
                           TMAX=record["TMAX"], TMIN=record["TMIN"])

    def delete(self, date):
        record = get_record_by_date(date)
        if record:
            table.remove(record)
        return {"message": "Deleted"}


class Forecast(Resource):

    def get(self, date):
        if get_record_by_date(date) == None:
            # find previous years weather
            previous_year = find_previous_year_in_record(date)
            records = get_seven_days_weather(previous_year)
            forecast = replace_to_current_date(date, records)
            return forecast
        else:
            # generate data based on previous day
            records = get_seven_days_weather(date)
            tmax, tmin = [], []
            for record in records:
                tmax.append(record['TMAX'])
                tmin.append(record['TMIN'])
            for record in records:
                record['TMAX'] = sum(tmax) / len(tmax)
                record['TMIN'] = sum(tmin) / len(tmin)
            return records



# add_resource function registers the routes with the framework using the given endpoint
api.add_resource(Home, "/")
api.add_resource(WeatherList, "/historical", "/historical/")
api.add_resource(Weather, "/historical/<string:date>")
api.add_resource(Forecast, "/forecast/<string:date>")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


