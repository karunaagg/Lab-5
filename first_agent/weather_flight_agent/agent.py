import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools import google_search
# from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint







configuration = weatherapi.Configuration()
configuration.api_key['key'] = '5f98d8a9446b48ff9cf72108251109'
def weather_tool(q1:str, dt1:str)-> dict:
    """Returns the dictionary containing weather information.

    Args:
       
        q1 (str) : name of the city.
        dt1 (str) : date at which forecast is required.

    Returns:
        int: return the dictionary containing information about the maximum temperature, humidity and chances of rain.
    """

    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['key'] = 'Bearer'

    # create an instance of the API class
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
    q = q1 # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
    dt = dt1 # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format

    try:
        # Astronomy API
        api_response = api_instance.forecast_weather(q, dt)
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling APIsApi->astronomy: %s\n" % e)
    
    r1 = api_response['forecast']['forecastday'][0]['day']

    result = {'max_temp' : r1['maxtemp_c'], 'humidity' : r1['avghumidity'], 'rain_chance' : r1['daily_chance_of_rain']}
    
    
    return result

def flight_tool(city1:str, city2:str)-> dict:
    """Returns the dictionary containing flight information.

    Args:
       
        city1 (str) : name of the origin city.
        city2 (str) : name of the destination city.

    Returns:
        int: return the dictionary containing information about the time and price between 2 cities.
    """
    result = {'flight_time' : ['9 AM', '12 AM', '3 PM', '10 PM'], 'Price' : [6000, 8000, 70000, 10000]}
    return result




root_agent = Agent(
    name="Flight_agent",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful agent that will tell the information about the weather in a particular city when asked or when asked about the " \
        "flight between 2 city you can help in the flight timings and Pricw"
    ),
    instruction=("You are the weather expert agent that will provide the information about weather when asked using weather tool"
    "and if no date and city is given in propmt the consider city as delhi and date of today and similarly when somebody will ask you about"
    "flights between 2 cities you can help me in that also using flight tool and if somebody ask about both you can hangle the situation"
    "like a expert and help in the planning"),
    tools=[weather_tool, flight_tool],

)