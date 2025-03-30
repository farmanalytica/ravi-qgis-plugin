import requests
import json
import pandas as pd
from datetime import datetime, timedelta

def open_nasapower(latitude, longitude, start, end):

    print(f"Latitude: {latitude}, Longitude: {longitude}")
    print(f"Start date: {start}, End date: {end}")
    print("Opening NASA POWER data for the selected location...")

    start_date = datetime.strptime(str(start).split()[0], "%Y-%m-%d")
    end_date = datetime.strptime(str(end).split()[0], "%Y-%m-%d")

    # Adjust the start date to the first day of the month
    new_start = start_date.replace(day=1).strftime("%Y%m%d")
    
    # Adjust the end date to the last day of the month
    new_end = (end_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    new_end = new_end.strftime("%Y%m%d")
    
    # Print the adjusted start and end dates for debugging
    print(new_start, new_end)

    # Request precipitation, minimum temperature, and maximum temperature
    base_url = (f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR,T2M_MIN,T2M_MAX&community=RE&longitude={longitude}&latitude={latitude}&start={new_start}&end={new_end}&format=JSON")
    api_request_url = base_url.format(longitude=longitude, latitude=latitude)
    response = requests.get(url=api_request_url, verify=True, timeout=1000)
    content = json.loads(response.content.decode('utf-8'))
    data = content['properties']['parameter']

    # Remove dates with -999.0 from the raw data
    for param in data:
        dates_to_remove = [date for date, value in data[param].items() if value == -999.0]
        for date in dates_to_remove:
            del data[param][date]

    # Create DataFrames for each parameter
    df_precipitation = pd.DataFrame.from_dict(data['PRECTOTCORR'], orient='index', columns=['Precipitation'])
    df_min_temp = pd.DataFrame.from_dict(data['T2M_MIN'], orient='index', columns=['Min Temperature'])
    df_max_temp = pd.DataFrame.from_dict(data['T2M_MAX'], orient='index', columns=['Max Temperature'])

    # Combine all DataFrames into a single DataFrame
    df_combined = pd.concat([df_precipitation, df_min_temp, df_max_temp], axis=1)
    df_combined[df_combined < 0] = 0  # Replace negative values with 0

    # Remove rows with missing or NaN values
    df_combined = df_combined.dropna()

    # Convert the index to datetime
    df_combined.index = pd.to_datetime(df_combined.index, format='%Y%m%d')
    daily_data = df_combined.reset_index().rename(columns={'index': 'Date'}).copy()

    # Resample the data to monthly frequency and sum the precipitation
    monthly_precipitation = df_combined['Precipitation'].resample('M').sum()
    df_nasa = monthly_precipitation.to_frame()

    print("NASA POWER data loaded successfully.")
    return df_nasa, daily_data
