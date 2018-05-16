# Weather-API

## What is this?

This is a REST API to host weather information in Cincinnati. In RESTful applications, resources can be manipulated using a fixed set of four create, read, update, delete operations: PUT, GET, POST, and DELETE.


## Dataset

The dataset 'daily.csv' is the daily weather data for Cincinnati in last three years. It has three columns:
* DATE: YYYYMMDD format
* TMAX: Daily Max Temperature
* TMIN: Daily Min Temperature

## Usage

### Get all historical data (GET Method)
End point: `</historical/>`

Response - HTTP 200

```
[{"DATE": "20130101"},
{"DATE": "20130102"},
{"DATE": "20130103"},
...
{"DATE": "20170115"}]
```

### Add weather data for a particular day (POST Method)
End point: `</historical/>`

For example:
`</historical/>` with data `{"DATE": "20130101", "TMAX": 34.0, "TMIN": 26.0}` will give a HTTP 201 code with response `{"DATE": "20130101"}`.

### Get weather information for a particular day (GET Method)
End point: `</historical/dateYYYYMMDD>`

If the given date is in the dataset, the historical record will be returned. If the date is not in the dataset, a 404 error code will be given.
For example: 

1. `</historical/20130101>`  

Response - HTTP 200

```
{"DATE": "20130101", "TMAX": 34.0, "TMIN": 26.0}
```

2. `</historical/99990101>`  
HTTP Error code 404

### Delete data for a particular day (DELETE Method)
End point: `</historical/dateYYYYMMDD>`

Response HTTP 200 if the date is in the dataset and Response HTTP 400 if not.

### Predict weather for next 7 days (GET Method)
End point: `</forecast/dateYYYYMMDD>`

For example: `</forecast/20130101>`  

Response - HTTP 200

```
[{"DATE": "20130101", "TMAX": 34.0, "TMIN": 26.0},
{"DATE": "20130102", "TMAX": 29.5, "TMIN": 15.0},
{"DATE": "20130103", "TMAX": 34.5, "TMIN": 12.0},
{"DATE": "20130104", "TMAX": 36.5, "TMIN": 23.0},
{"DATE": "20130105", "TMAX": 41.0, "TMIN": 19.0},
{"DATE": "20130106", "TMAX": 40.0, "TMIN": 28.0},
{"DATE": "20130107", "TMAX": 39.5, "TMIN": 19.0}]
```
