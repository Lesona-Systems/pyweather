import requests
from requests.exceptions import HTTPError
from configparser import ConfigParser

# parse secrets.ini for OpenWeather API key
def _get_api_key():
  config = ConfigParser()
  config.read('secrets.ini')
  return config['openweather']['api_key']

# define ASCII escape sequences for coloring terminal output
class colors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m' # ends coloration
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

# get current weather, throw exceptions for HTTP error & other Exceptions
try:
  get_current_weather = requests.get(weather_url)
  get_current_weather.raise_for_status()
  weather_data = get_current_weather.json()

except HTTPError as http_err:
  print(f'HTTP error occuperd: {http_err}')
except Exception as err:
  print(f'Other error occured: {err}')

# assign city, weather description, and temperature to values in returned weather data dict

def display_weather_info():
  city = weather_data['name']
  weather_description = weather_data['weather'][0]['description']
  temperature = weather_data['main']['temp']

  print(f'In {city}, the weather is currently {weather_description} with a temperature of ({temperature}°F).')

display_weather_info()