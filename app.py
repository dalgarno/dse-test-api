from flask import Flask
from flask_restx import Resource, Api

from pathlib import Path
import json

app = Flask(__name__)
api = Api(app)

COUNTRY_PATH = Path('./country_data.json')
COUNTRY_DATA = json.loads(COUNTRY_PATH.read_text())

COUNTRY_CODES = set()
PER_COUNTRY_DATA = {}

for entry in COUNTRY_DATA:
    if 'Country_code' not in entry:
        continue
    country_code = entry['Country_code']
    COUNTRY_CODES.add(country_code)
    if country_code not in PER_COUNTRY_DATA:
        PER_COUNTRY_DATA[country_code] = [entry]
    else:
        PER_COUNTRY_DATA[country_code].append(entry)

COUNTRY_CODES = sorted([c for c in COUNTRY_CODES])


@api.route('/country_codes')
class CountryCodes(Resource):
    def get(self):
        return COUNTRY_CODES


@api.route('/country/<string:country_code>')
class Country(Resource):
    def get(self, country_code):
        if country_code not in PER_COUNTRY_DATA:
            return {'message': f'Country code {country_code} not found!'}, 404
        return PER_COUNTRY_DATA[country_code]



if __name__ == '__main__':
    app.run()