"""
Script for reading in all the energy files and all the weather files.
Then joining the two together.

When editing including the following lines are useful
    execfile(os.path.join(os.environ['HOME'], '.pythonrc'))
    pd.set_option('max_rows', 30)
"""
import os
import numpy as np
import pandas as pd
import datetime as dt
import glob

proj_dir = os.path.join(os.environ['HOME'], 'Energy')
csv_dir = os.path.join(proj_dir, 'csv')

raw_file_list = glob.glob(csv_dir + "EDFEnergy*.csv") # requires naming convention
raw_data_frame = pd.concat((pd.read_csv(f) for f in raw_file_list), ignore_index=True)
raw_data_frame.columns = ['raw_read_datetime', 'electricity_consumption', 'ec_est', 'gas_consumption', 'gc_est']
raw_data_frame['read_datetime'] = pd.to_datetime(raw_data_frame['raw_read_datetime'], format='%d-%m-%Y %H:%M:%S')
raw_data_frame = raw_data_frame.sort_values('read_datetime')
raw_data_frame['read_date'] = raw_data_frame['read_datetime'].dt.date
raw_data_frame['read_time'] = raw_data_frame['read_datetime'].dt.time
raw_data_frame['read_weekday'] = raw_data_frame['read_datetime'].dt.weekday
raw_data_frame['is_weekday'] = [not(wd in [5,6]) for wd in raw_data_frame['read_weekday']]

weather_file_list = glob.glob(csv_dir + "bristol_weather_*.csv") # requires naming convention
weather_frame = pd.concat((pd.read_csv(f, parse_dates=[['DATE', 'TIME']]) for f in weather_file_list), ignore_index=True)

weather_frame.columns = ['read_datetime', 'temperature', 'gust_mph', 'direction', 'avg_mph', 'humidity_perc', 'baro_mb', 'trend_mb', 'daily_rain_mm', 'monthly_rain_mm', 'solar_power', 'uv', 'weather']
full_data_frame = raw_data_frame.merge(weather_frame, how='left', on='read_datetime')
full_data_frame = full_data_frame.fillna(method='ffill') # NB forward fill to fill nulls in weather data.

full_data_frame.to_csv(os.path.join(csv_dir, 'complete_data.csv'), index=False)
# TODO try to remove globals altogether.
