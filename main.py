from flask import Flask, request
import requests
import json
from dateutil import parser
from datetime import datetime

app = Flask(__name__)


def is_date_valid(date, count_days_back):
    parsed_date = parser.parse(date)
    time_delta = datetime.now() - parsed_date
    return time_delta.days <= count_days_back


def get_max_values(key, country):
    if not isinstance(country, str):
        return {}
    response = requests.get(
        'https://disease.sh/v3/covid-19/gov/{country}?allowNull=true'.format(country=country.lower()))
    data = json.loads(response.content)
    count_days_back = 30
    max_cases = -1
    date = None
    for entitiy in data['data']['timeline']:
        # TODO: run backwards
        if not is_date_valid(entitiy['date'], count_days_back):
            continue

        if entitiy[key] > max_cases:
            max_cases = entitiy[key]
            date = entitiy['date']
    return dict(Value=max_cases, date=date, country=country, method=key)


@app.route('/status')
def get_status():
    return {'status': 'success'}


@app.errorhandler(404)
def not_found(e):
    return {}


@app.route('/newCasesPeak')
def get_newCasesPeak():
    country = request.args.get('country')
    max_positive_tests = get_max_values('newPositiveTests', country)
    return max_positive_tests


@app.route('/newDeathPeak')
def get_newDeathPeak():
    country = request.args.get('country')
    max_deaths = get_max_values('newDeaths', country)
    return max_deaths


@app.route('/newRecoveredPeak')
def get_newRecoveredPeak():
    country = request.args.get('country')
    max_recovery = get_max_values('newlyRecovered', country)
    return max_recovery


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
