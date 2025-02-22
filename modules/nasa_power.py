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
    # start_date = datetime.strptime(str(start), "%Y-%m-%d")
    # end_date = datetime.strptime(str(end), "%Y-%m-%d")

    # Adjust the start date to the first day of the month
    new_start = start_date.replace(day=1).strftime("%Y%m%d")
    
    # Adjust the end date to the last day of the month
    new_end = (end_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    new_end = new_end.strftime("%Y%m%d")
    
    # Print the adjusted start and end dates for debugging
    print(new_start, new_end)


    base_url = (f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=RE&longitude={longitude}&latitude={latitude}&start={new_start}&end={new_end}&format=JSON")
    api_request_url = base_url.format(longitude=longitude, latitude=latitude)
    response = requests.get(url=api_request_url, verify=True, timeout=1000)
    content = json.loads(response.content.decode('utf-8'))
    df = pd.DataFrame.from_dict(content['properties']['parameter'])
    df[df < 0] = 0
    
    # Convert the index to datetime
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    daily_precipitation = df.reset_index().rename(columns={'index': 'Date'}).copy()
    

    # Resample the data to monthly frequency and sum the values
    monthly_sum = df.resample('M').sum()
    df_nasa = monthly_sum

    print("NASA POWER data loaded successfully.")
    return df_nasa, daily_precipitation
    
