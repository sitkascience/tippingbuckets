# Author: Cora Siebert
# Date: 10/15/2020
# This script queries data from MesoWest and stores the data in a JSON
# file. It then plots accumulated rainfall over time and rainfall rate over time.
from matplotlib.dates import date2num
from MesoPy import Meso
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


# please specify stations and time period of interest here
stations = 'pmja2, pmma2, pmpa2, pmga2, pmaa2, pmia2, pmda2, pmba2, pmea2, pmfa2, pasi'

# time in UTC, please
start_time_raw = '202010251900' # date format YYYMMDDHHMM
end_time_raw = '202010261900'
time_option = 'utc'

# cora's token to access the data
my_token = 'dd3ed5a81d5840e1bf7b94f34117785e'

# convert raw times to formatted times.
## This should probably be its own function. It is only here 
## so that it start_time_raw can be used for querying usgs data, too
start_time_formatted = start_time_raw[:4] + '-' + start_time_raw[4:6] + '-' + start_time_raw[6:8] + 'T' + start_time_raw[8:10] + ':' + start_time_raw[10:]
end_time_formatted = end_time_raw[:4] + '-' + end_time_raw[4:6] + '-' + end_time_raw[6:8] + 'T' + end_time_raw[8:10] + ':' + end_time_raw[10:]

query_data = input("Would you like to query new data? (y/n): ")

# if the user wants to query new data (which counts towards the 3E6 hour allotment),
if query_data == 'y':
    # query MesoWest data
    m = Meso(token=my_token)
    print("     Querying MesoWest data...")
    all_meso_data = m.timeseries(stid=stations, start=start_time_raw,
            end=end_time_raw, obtimezone=time_option)
    with open('/Users/CoraJune/Documents/GitHub/sitkaPrecip/all_meso_data.json', 'w') as fp:
        print("     Writing MesoWest data to file...")
        json.dump(all_meso_data, fp, indent=2) # use `json.loads` to do the reverse

# if the user doesn't want to query new data, use the existing data file.
if query_data == 'n':
    print("     Opening MesoWest data...")
    with open('/Users/CoraJune/Documents/GitHub/sitkaPrecip/all_meso_data.json', 'r') as fp:
        all_meso_data = json.load(fp)


fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()

unix_epoch = datetime(1970,1,1)
count = 0
for station in all_meso_data['STATION']:
    print("\n{}".format(station['NAME']))
    if 'USCRN' in station['NAME']:
        precip_nans = get_precip(station,all_meso_data)
        dates_nans = get_datetime(station,all_meso_data)
        dates, precip = filter_nans(station,dates_nans, precip_nans)
        print(station['NAME'])
        print(precip[0])
        s_list[count] = precip_final
    if station['NAME'] == 'Sitka - Sitka Airport':
        print("\n------- {} --------".format(station['NAME']))
        all_precip = get_precip(station,all_meso_data)
        dates = get_datetime(station,all_meso_data)
        dates_list=[]
        precip_list=[]
        for date, rain, in zip(dates, all_precip):
            # some time further back the reset time was the 55th minute of every hour
            # that means this algorithm will not work for all cases, and MUST be rewritten
            if date.minute == 53:
                dates_list.append(date)
                precip_list.append(rain)
        dates = np.array(dates_list)
        precip_final = np.array(precip_list)
        precip_final = [i * 25.4 for i in precip_final]
        total_precip = max(precip_final)
        print("Total precip: {} mm".format(total_precip))
        print("Total precip: {} in".format(total_precip/25.4))
#        s_list[count] = list(zip(dates,precip_final))
##        print(s_list[count])
#        count += 1
        ls = '--'
    elif station['NAME'].endswith("MESONET") or station['NAME'] == 'SAWMILL CREEK NEAR SITKA 4E':
        print("\n------- {} --------".format(station['NAME']))
        # first let's just get the raw data
        precip = get_precip(station,all_meso_data)
        dates = get_datetime(station,all_meso_data)
        # now let's filter out the nans
        dates, precip = filter_nans(station,dates, precip)
        # now let's clean it up a bit more by making sure there aren't
        # station resets or anything in our data set
        precip_final = clean_data(precip)
        precip_final_in = [i / 25.4 for i in precip_final]
        total_precip = max(precip_final)    # max precip!
        # zip together dates and precip for each station and store for later use
#        s_list[count] = list(zip(dates,precip_final))
#        if max_precip_len <= len(precip_final):
#            max_precip_len = len(precip_final)
        print("Total precip: {} in".format(total_precip/25.4))
        print("Total precip: {} mm".format(total_precip))
#        count += 1
        ls = '-'
    else:
        print("    I don't know this station.")
        pass
        # plot the accumulated rainfall data
    ax.plot(dates, precip_final, label=station['NAME'], linestyle = ls)
    format_xticks(ax)
    ax.set_ylabel("Cumulative Rainfall (mm)")
    ax.set_title("Cumulative Rainfall")
    legend = ax.legend(loc='upper left', prop={'size':5})
#    plt.savefig('/Users/CoraJune/Documents/GitHub/sitkaPrecip/tester/all_tb_cumu.png', bbox_inches='tight')


    # now let's calculate rainfall rate
    # convert datetime to seconds from UNIX epoch
    dates_secs = [(dtime - unix_epoch).total_seconds() for dtime in dates]
    # then convert seconds from UNIX epoch to hours
    date_hrs = [(dtime/3600) for dtime in dates_secs]
    # calculate gradient of precip data
    dy = np.gradient(precip_final)
    # calculate gradient of dates (hours from UNIX epoch)
    dt = np.gradient(date_hrs)
    # calculate rainfall rate
    dydt_mm = dy/dt
    dydt_in = [i / 25.4 for i in dydt_mm]
    print("Max rate: {} in/hr".format(max(dydt_in)))
    print("Max rate: {} mm/hr".format(max(dydt_mm)))

    # plot the rainfall rate
#    fig1.set_size_inches(12, 8)
    ax1.plot(dates, dydt_mm, label=station['NAME'], linestyle = ls)
    format_xticks(ax1)
    ax1.set_title("Rainfall Rate")
    ax1.set_ylabel("Rainfall Rate (mm/hr)")
    legend = ax1.legend(loc='upper center', prop={'size':6})
    plt.xticks(rotation=30)
#    plt.savefig('/Users/CoraJune/Documents/GitHub/sitkaPrecip/tester/light_all_tb_rate.png',
#    ¦   ¦   dpi = 400, bbox_inches='tight')
format_xticks(ax)
format_xticks(ax1)

plt.show()

