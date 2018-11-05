import os
execfile(os.path.join(os.environ['HOME'], '.pythonrc'))
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import date2num
from scipy.stats import pearsonr

pd.set_option('max_rows', 30)

def aggGasVsTemp(agg_frame):
    lower_bound = agg_frame['gas_consumption', 'mean'] - agg_frame['gas_consumption', 'std']
    lower_bound[lower_bound < 0] = 0.0
    fig, ax1 = plt.subplots()
    ax1.plot(agg_frame.index, agg_frame['gas_consumption', 'mean'], color='blue')
    ax1.fill_between(agg_frame.index, y1=lower_bound, y2=agg_frame['gas_consumption', 'mean'] + agg_frame['gas_consumption', 'std'],
        color='blue', alpha=0.3)
    ax1.set_ylabel('Gas Consumption (kWh)', fontsize='large', color='blue')
    ax1.tick_params(axis='x', rotation=30)
    ax2 = ax1.twinx()
    ax2.plot(agg_frame.index, agg_frame['temperature', 'mean'], color='red')
    ax2.fill_between(agg_frame.index, y1=agg_frame['temperature', 'mean'] - agg_frame['temperature', 'std'],
        y2=agg_frame['temperature', 'mean'] + agg_frame['temperature', 'std'], color='red', alpha=0.3)
    ax2.set_ylabel('Temperature (C)', fontsize='large', color='red')
    plt.xticks(6*np.array(range(8)))
    plt.xlim(agg_frame.index[0], agg_frame.index[-1])
    plt.xlabel('Time', fontsize='large')
    plt.title('Aggregated Weekday Gas Consumption vs Temperature', fontsize='large')
    plt.tight_layout()

def sumConsumpVsTemp(daily_frame):
    daily_nums = date2num(daily_frame.index)
    fig, ax1 = plt.subplots()
    ax1.bar(daily_nums-0.4, daily_frame['gas_consumption', 'sum'], width=0.4, color='blue', align='center', label='Gas', alpha=0.6)
    ax1.bar(daily_nums, daily_frame['electricity_consumption', 'sum'], width=0.4, color='green',align='center', label='Electricity', alpha=0.6)
    ax1.xaxis_date()
    ax1.set_ylabel('Consumption (kWh)', fontsize='large')
    ax1.tick_params(axis='x', rotation=30)
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(daily_frame.index, daily_frame['temperature', 'mean'], color='red')
    ax2.fill_between(daily_frame.index, y1=daily_frame['temperature', 'mean'] - daily_frame['temperature', 'std'],
        y2=daily_frame['temperature', 'mean'] + daily_frame['temperature', 'std'], color='red', alpha=0.3)
    ax2.set_ylabel('Avg Temperature (C)', fontsize='large', color='red')
    plt.xlim(daily_nums[0], daily_nums[-1])
    plt.title('Total Consumption vs Average Temperature', fontsize='large')
    plt.tight_layout()

def gasTempCorrelationPlot(daily_frame):
    daily_gas = daily_frame['gas_consumption', 'sum']
    daily_elec = daily_frame['electricity_consumption', 'sum']
    daily_temp = daily_frame['temperature', 'mean']
    gas_p_corr_coeff, gas_p_value = pearsonr(daily_gas, daily_temp)
    elec_p_corr_coeff, elec_p_value = pearsonr(daily_elec, daily_temp)
    fig = plt.scatter(daily_gas, daily_temp)
    plt.scatter(daily_elec, daily_temp)
    plt.xlabel('Total daily power consumption (kWh)')
    plt.ylabel('Mean daily temperature (C)')
    plt.text(0.8, 0.82, r'Gas $\rho = $' + str(round(gas_p_corr_coeff, 3)), ha='center', va='center', transform=fig.axes.transAxes)
    plt.text(0.8, 0.75, r'Gas p value = ' + str(round(gas_p_value, 3)), ha='center', va='center', transform=fig.axes.transAxes)
    plt.text(0.8, 0.68, r'Electricity $\rho = $' + str(round(elec_p_corr_coeff, 3)), ha='center', va='center', transform=fig.axes.transAxes)
    plt.text(0.8, 0.61, r'Electricity p value = ' + str(round(elec_p_value, 3)), ha='center', va='center', transform=fig.axes.transAxes)

proj_dir = os.path.join(os.environ['HOME'], 'Energy/')
csv_dir = os.path.join(proj_dir, 'csv/')
image_dir = os.path.join(proj_dir, 'images/')

complete_frame = pd.read_csv(os.path.join(csv_dir, 'complete_data.csv'))
weekday_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][complete_frame['is_weekday']]
weekend_frame = complete_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']][np.logical_not(complete_frame['is_weekday'])]
agg_frame = weekday_frame[['read_time', 'gas_consumption', 'electricity_consumption', 'temperature']].groupby('read_time').agg(['mean', 'std'])

daily_frame = complete_frame[['read_date', 'gas_consumption', 'electricity_consumption', 'temperature']].groupby('read_date').agg(['sum', 'mean', 'std'])
daily_frame.index = [dt.datetime.strptime(dfi, '%Y-%m-%d')for dfi in daily_frame.index]
