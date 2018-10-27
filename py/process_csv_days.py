import os
execfile(os.path.join(os.environ['HOME'], '.pythonrc'))
import numpy as np
import pandas as pd
import glob

pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_rows', 30)

proj_dir = os.path.join(os.environ['HOME'], 'Energy/')
csv_dir = os.path.join(proj_dir, 'csv/')

raw_file_list = glob.glob(csv_dir + "EDFEnergy*.csv")
raw_data_frame = pd.concat((pd.read_csv(f) for f in raw_file_list), ignore_index=True)
raw_data_frame.columns = ['raw_read_datetime', 'electricity_consumption', 'ec_est', 'gas_consumption', 'gc_est']
raw_data_frame['read_datetime'] = pd.to_datetime(raw_data_frame['raw_read_datetime'], format='%d-%m-%Y %H:%M:%S')
raw_data_frame = raw_data_frame.sort_values('read_datetime')
raw_data_frame['read_date'] = raw_data_frame['read_datetime'].dt.date
raw_data_frame['read_time'] = raw_data_frame['read_datetime'].dt.time
raw_data_frame['read_weekday'] = raw_data_frame['read_datetime'].dt.weekday
raw_data_frame['is_weekday'] = [wd in [5,6] for wd in raw_data_frame['read_weekday']]
