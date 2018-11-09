import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import date2num
from scipy.stats import pearsonr

def addMeanTempAx(axis, frame, ylabel):
    axis.plot(frame.index, frame['temperature', 'mean'], color='red')
    axis.fill_between(frame.index, y1=frame['temperature', 'mean'] - frame['temperature', 'std'],
        y2=frame['temperature', 'mean'] + frame['temperature', 'std'], color='red', alpha=0.3)
    axis.set_ylabel(ylabel, fontsize='large', color='red')

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
    addMeanTempAx(ax2, agg_frame, 'Temperature (C)')
    plt.xticks(6*np.array(range(8)))
    plt.xlim(agg_frame.index[0], agg_frame.index[-1])
    plt.xlabel('Time', fontsize='large')
    plt.title('Aggregated Weekday Gas Consumption vs Temperature', fontsize='large')
    plt.tight_layout()
    plt.show(block=False)

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
    addMeanTempAx(ax2, daily_frame, 'Avg Temperature (C)')
    plt.xlim(daily_nums[0], daily_nums[-1])
    plt.title('Total Consumption vs Average Temperature', fontsize='large')
    plt.tight_layout()
    plt.show(block=False)

def gasTempCorrelationPlot(daily_frame):
    corr_frame = daily_frame.corr()
    gas_p_corr_coeff = corr_frame.loc['temperature','gas_consumption'].loc['mean', 'sum']
    elec_p_corr_coeff = corr_frame.loc['temperature','electricity_consumption'].loc['mean', 'sum']
    plt.figure()
    fig = plt.scatter(daily_frame['temperature', 'mean'], daily_frame['gas_consumption', 'sum'], label='Gas Power')
    plt.scatter(daily_frame['temperature', 'mean'], daily_frame['electricity_consumption', 'sum'], label='Electric Power')
    plt.ylabel('Total daily power consumption (kWh)')
    plt.xlabel('Mean daily temperature (C)')
    plt.text(0.8, 0.82, r'Gas $\rho = $' + str(round(gas_p_corr_coeff, 3)), ha='center', va='center', transform=fig.axes.transAxes)
    plt.text(0.8, 0.75, r'Electricity $\rho = $' + str(round(elec_p_corr_coeff, 3)), ha='center', va='center', transform=fig.axes.transAxes)
    plt.legend()
    plt.show(block=False)
