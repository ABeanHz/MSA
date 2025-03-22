# -*- coding: utf-8 -*-
"""
@author: Alison Bean de Hernandez
Purpose: Find the min and max temperatures for 16 selected cities using Open Weather Map
Created: 07/06/24
"""


# Read in Libraries
import pprint
import requests
import sys
import pandas as pd
import os 

print(os.getcwd()) ### Check where files are being saved

#~~~~~~~~~~~~~BASIC SUMMARY OF FILE CONTENTS~~~~~~~~~~~~~~~~~~#
#   Section 1. Create a function that can be used to read-in different cities from the OpenweatherMap and export a dataframe of daily mins and max celsius temps
#           - Use API to get lat and lon data by city
#           - Use the lat and lon to use an API to pull the 5-day weather forecast
#           - Extract JSON data and normalize into pandas dataframe
#           - Clean and reshape dataframe to have the min and max temperatures in celsius by city by day for each of the 16 cities 
#   Section 2. Create dataframe containing all 16 cities 
#           - Run the function on each of the 16 cities 
#           - Extract the 16 dfs
#           - Create one df with all cities
#   Section 3. Export to csv and format outputs to 2 decimal places



#~~~~~~~Background information~~~~~~~~#

api_key =  ### replace with your own 
 


# Selected Cities for Analysis
cities = [
    "Buenos Aires, Argentina", "Guangzhou, China", "Wichita, Kansas", "Niskayuna, New York",
    "Gwangmyeong, South Korea", "Taipei, Taiwan", "Nanaimo, British Columbia", "Chennai, India",
    "Barrington, Illinois", "Littleton, Colorado", "Peterhead, Scotland", "Vizag, India",
    "Des Moines, Iowa", "Beijing, China", "Killeen, Texas", "Morehead City, North Carolina"
]

#~~~~~~~Section 1~~~~~~~~#

# Geolocate the cities of interest to get its latitude and longitude, and pull the daily min and max temps
def get_city_weather(api_key, city): 
#~~~~~~~~~PART 1: Get the data from the web~~~~~~~~~~
    geo_URL = 'http://api.openweathermap.org/geo/1.0/direct'

    geo = f'{geo_URL}?q={city}&limit=5&appid={api_key}'
    resp = requests.get( geo )

    if resp.status_code != 200: # Failure?
        print( f'Error geocoding {city}: {resp.status_code}' )
        sys.exit( 1 )

# OpenWeatherMap returns a list of matching cities, up to the limit specified
# in the API call; even if you only ask for one city (limit=5), it's still
# returned as a 1-element list

    if len( resp.json() ) == 0: # No such city?
        print( f'Error locating city {city}; {resp.status_code}' )
        sys.exit( 2 )

    json = resp.json()
    
    if type( json ) == list: # List of cities?
        lat = json[ 0 ][ 'lat' ]
        lon = json[ 0 ][ 'lon' ]
    else: # Unknown city?
        print( f'Error, invalid data returned for city {city}, {resp.status_code}' )
        sys.exit( 3 )

# Use latitude and longitude to get its 5-day forecast in 3-hour
# blocks

    forecast_URL = 'http://api.openweathermap.org/data/2.5/forecast'
    forecast = f'{forecast_URL}?lat={lat}&lon={lon}&appid={api_key}'
    resp = requests.get( forecast )

    if resp.status_code != 200: # Failure?
        print( f'Error retrieving data: {resp.status_code}' )
        sys.exit( 4 )
# Pretty-print the resulting JSON forecast for the first 3 hour block
    print( f'{city}:' )
    data = resp.json()
    printer = pprint.PrettyPrinter( width=80, compact=True )
    printer.pprint( data[ 'list' ][ 0 ] )

#~~~~~~~~~PART 2: Select mins and maxes for daily temps~~~~~~~~~~
# Turn JSON into pandas df for easier data manipulation
    extract_JSON = pd.json_normalize(data['list'], max_level=1)
    #extract_JSON.head()
    
    # Selecting only the relevant columns from the JSON normalized step
    sel_cols= extract_JSON[['dt', 'dt_txt', 'main.temp', 'main.temp_min', 'main.temp_max']]
    sel_cols[['day', 'time']] = sel_cols['dt_txt'].str.split(' ', expand=True) ### Splitting on day and time to identify which day we are looking at
    
    # Marking each relevant day order from first to last 
    def_day= sel_cols[['day']].drop_duplicates()
    def_day['run']=1  ### intermediate variable to get number of day 
    def_day['day_block'] = def_day['run'].cumsum() ### Marking the days in order
    def_day = def_day.drop(columns = 'run') ### dropping intermediate variable
    print(def_day)
    print(type(def_day)) 
    
    day_df=sel_cols.merge(def_day, left_on='day', right_on ='day')  ### merging in the day label to the main dataset
    print(type(day_df))
    
    #Finding the maxes and mins by day based on the day_block label of 1 - 6 
    idx_max = day_df.groupby('day_block')['main.temp_max'].idxmax()
    max_temps_byday = day_df.loc[idx_max]
    max_temps_byday = max_temps_byday[['day_block', 'main.temp_max']]
    max_temps_byday = max_temps_byday.rename(columns={'main.temp_max':'day_Max'})
    
    print(type(max_temps_byday))
    print(max_temps_byday)
    
    idx_min = day_df.groupby('day_block')['main.temp_min'].idxmin()
    min_temps_byday = day_df.loc[idx_min]
    min_temps_byday = min_temps_byday[['day_block', 'main.temp_min']]
    min_temps_byday = min_temps_byday.rename(columns={'main.temp_min':'day_Min'})
    
    print(type(min_temps_byday))
    print(min_temps_byday)
    
    #Clean-up to contain just the mins and maxes for reshaping
    city_long = day_df.merge(min_temps_byday, left_on='day_block', right_on ='day_block') 
    city_long = city_long.merge(max_temps_byday, left_on='day_block', right_on ='day_block') 
    
    city_long = city_long[city_long.day_block > 1] ### filtering the data to tomorrow onward
    city_long['day_block'] = city_long.day_block - 1 ### relabeling tomorrow as the first day 
    city_long.head(10)  ### Qa/Qc
    
    
    # Selecting just one obs. for the min and mac by day. 
    city_long=city_long[['day_block', 'day_Min', 'day_Max']].drop_duplicates()
    city_long['City']=city ### add in the city name for proper labeling
    print(city_long)
    
    #   Reshape long to prepare for final reshape and convert to celsius
    pivot_long = pd.melt(city_long, id_vars=['City', 'day_block'], value_vars=['day_Min', 'day_Max'])
    pivot_long[['day', 'status']] = pivot_long['variable'].str.split('_', expand=True)
    pivot_long =pivot_long.sort_values(by=['day_block'])
    pivot_long['status'] = pivot_long['status'] + " "+ pivot_long['day_block'].astype(str) 
    pivot_long['celsius'] = pivot_long['value'] -  273.15  ### converting to celsius
    pivot_long = pivot_long.drop(columns = ['day', 'variable', 'day_block', 'value']) ### dropping intermediate variable for clean dataframe
    pivot_long['celsius'] = pivot_long['celsius'] 
    print(pivot_long)
    
    # Shaping the data wide to match the format of the assignment -- one row of data per city
    pivot_wide = pivot_long.pivot_table(index='City', columns='status', values='celsius')
    pivot_wide = pivot_wide.reset_index()
    pivot_wide["Min Avg"] = pivot_wide[['Min 1', 'Min 2', 'Min 3', 'Min 4']].mean(axis=1, skipna=True).round(decimals = 2) ### Assignment requirement to round two decimal places, have a cutoff
    pivot_wide["Max Avg"] = pivot_wide[['Max 1', 'Max 2', 'Max 3', 'Max 4']].mean(axis=1, skipna=True).round(decimals = 2)
    print(pivot_wide)
    pivot_wide.info()
    return(pivot_wide)


#~~~~~~~Section 2~~~~~~~~#

# Run function for all cities and combine results
city_weather_data = [get_city_weather(api_key, city) for city in cities]
final_df = pd.concat(city_weather_data, ignore_index=True)

# Display final DataFrame
print(final_df)