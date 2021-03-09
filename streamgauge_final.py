# Author: Cora Siebert
# Date: 10/15/2020
# This script queries data from USGS and stores the data in a JSON
# file. It then plots stream gauge discharge or height over time.
from matplotlib.dates import date2num
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import json
from matplotlib import rc
from plot_funcs import *
from wx_funcs import *
from hydro_funcs import *
from soil_moisture_funcs import *
import matplotlib.ticker as ticker
from statistics import mean
from collections import defaultdict
import pylab as pl
import collections
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

plt.rc('font', **font)



# time in UTC, please
start_time_raw = '202010251900' # date format YYYMMDDHHMM
end_time_raw = '202010261900'
time_option = 'utc'


# convert raw times to formatted times.
## This should probably be its own function. It is only here 
## so that it start_time_raw can be used for querying usgs data, too
start_time_formatted = start_time_raw[:4] + '-' + start_time_raw[4:6] + '-' + start_time_raw[6:8] + 'T' + start_time_raw[8:10] + ':' + start_time_raw[10:]
end_time_formatted = end_time_raw[:4] + '-' + end_time_raw[4:6] + '-' + end_time_raw[6:8] + 'T' + end_time_raw[8:10] + ':' + end_time_raw[10:]

query_data = input("Would you like to query new data? (y/n): ")

# if the user wants to query new data (which counts towards the 3E6 hour allotment),
if query_data == 'y':
    # query stream gauge data
    ir_gauge_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=15087700&startDT=' + start_time_formatted + '%2b0000&endDT=' + end_time_formatted + '%2b0000&parameterCd=00060,00065&siteStatus=all'
    print("     Querying Indian River data...")
    ir_data = requests.get(ir_gauge_url)
    print("     Converting IR data to JSON...")
    ir_dict = ir_data.json()
    with open('/Users/CoraJune/Documents/GitHub/sitkaPrecip/ir_data.json', 'w') as fp:
        print("     Writing IR data to file...")
        json.dump(ir_dict, fp, indent=2) # use `json.loads` to do the reverse
# if the user doesn't want to query new data, use the existing data file.
if query_data == 'n':
    print("     Opening IR data...")
    with open('/Users/CoraJune/Documents/GitHub/sitkaPrecip/ir_data.json', 'r') as fp:
        ir_dict = json.load(fp)

fig, ax = plt.subplots()
ir_dates, ir_discharge = get_IR_timeseries(ir_dict, 'discharge')
ax.plot(ir_dates, ir_discharge)
ax.set(ylabel="Discharge (cfs)")
ax.set_title("Indian River Discharge Rate")
format_xticks(ax)

plt.show()
