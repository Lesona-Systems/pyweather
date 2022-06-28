import requests
from requests.exceptions import HTTPError
from configparser import ConfigParser



def _get_api_key():
  config = ConfigParser()
  config.read('secrets.ini')
  return config['openweather']['api_key']

# get API key from secrets.ini
api_key = _get_api_key()

print('Get your local weather!')

user_zip = input('Enter your zip code: ')

# Form Geocoding API url
geo_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={user_zip},US&appid={api_key}"
# get and parse zip into lat/long for use in current weather API call
try:
  get_latlon = requests.get(geo_url)
  get_latlon.raise_for_status()
  geoResponse = get_latlon.json()

# throw HTTP error/exception on failure
except HTTPError as http_err:
  print(f'HTTP error occured: {http_err}')
except Exception as err:
  print(f'Other error occurred: {err}')

# assign returned json values to lat/long vars for OW API construction
lat = geoResponse.get('lat')
lon = geoResponse.get('lon')

# form OpenWeather weather API url

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

# get current weather
try:
  get_current_weather = requests.get(weather_url)
  get_current_weather.raise_for_status()
  weather = get_current_weather.json()

except HTTPError as http_err:
  print(f'HTTP error occuperd: {http_err}')
except Exception as err:
  print(f'Other error occured: {err}')

print(weather)