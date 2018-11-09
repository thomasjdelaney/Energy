"""
Script for reading in the complete_data, and making some graphs to present
the important information therein.

When editing, the following lines are useful:
    execfile(os.path.join(os.environ['HOME'], '.pythonrc'))
    pd.set_option('max_rows', 30)
"""
import sys
import os
import pandas as pd
import datetime as dt

proj_dir = os.path.join(os.environ['HOME'], 'Energy/')
py_dir = os.path.join(proj_dir, 'py/')
csv_dir = os.path.join(proj_dir, 'csv/')
image_dir = os.path.join(proj_dir, 'images/')

sys.path.append(py_dir)
from plottingfunctions import *

complete_frame = pd.read_csv(os.path.join(csv_dir, 'complete_data.csv'))
weekday_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][complete_frame['is_weekday']]
weekend_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][np.logical_not(complete_frame['is_weekday'])]
agg_frame = weekday_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']].groupby('read_time').agg(['mean', 'std'])

daily_frame = complete_frame[['read_date', 'gas_consumption', 'electricity_consumption', 'temperature']].groupby('read_date').agg(['sum', 'mean', 'std'])
daily_frame.index = [dt.datetime.strptime(dfi, '%Y-%m-%d')for dfi in daily_frame.index]

aggGasVsTemp(agg_frame)
sumConsumpVsTemp(daily_frame)
gasTempCorrelationPlot(daily_frame)

# TODO try to remove globals altogether.
