import os
execfile(os.path.join(os.environ['HOME'], '.pythonrc'))
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('max_rows', 30)

proj_dir = os.path.join(os.environ['HOME'], 'Energy/')
csv_dir = os.path.join(proj_dir, 'csv/')
image_dir = os.path.join(proj_dir, 'images/')

complete_frame = pd.read_csv(os.path.join(csv_dir, 'complete_data.csv'))
weekday_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][complete_frame['is_weekday']]
weekend_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][np.logical_not(complete_frame['is_weekday'])]

# TODO write a function for this.

agg_frame = weekday_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']].groupby('read_time').agg(['mean', 'std'])
lower_bound = agg_frame['gas_consumption', 'mean'] - agg_frame['gas_consumption', 'std']
lower_bound[lower_bound < 0] = 0.0

fig, ax1 = plt.subplots()
ax1.plot(agg_frame['gas_consumption', 'mean'], color='blue')
ax1.fill_between(agg_frame.index, y1=lower_bound, y2=agg_frame['gas_consumption', 'mean'] + agg_frame['gas_consumption', 'std'],
    color='blue', alpha=0.3)
ax1.set_ylabel('Gas Consumption (kWh)', fontsize='large', color='blue')

ax2 = ax1.twinx()
ax2.plot(agg_frame['temperature', 'mean'], color='red')
ax2.fill_between(agg_frame.index, y1=agg_frame['temperature', 'mean'] - agg_frame['temperature', 'std'],
    y2=agg_frame['temperature', 'mean'] + agg_frame['temperature', 'std'], color='red', alpha=0.3)
ax2.set_ylabel('Temperature (C)', fontsize='large', color='red')
plt.xticks(8*np.array(range(6))) # TODO autorotate the ticks, set grid on
plt.xlabel('Time', fontsize='large')
