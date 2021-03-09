import numpy as np
from datetime import datetime,timedelta


def get_datetime(station,all_data):
    try:
        dates = np.array([datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%SZ') for dtime in station['OBSERVATIONS']['date_time']])
        dates = (dates + timedelta(hours=-8)).tolist()
#        dates = [datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S-0800') for dtime in station['OBSERVATIONS']['date_time']]

    except:
#        dates = [datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S-0900') for dtime in station['OBSERVATIONS']['date_time']]
        dates = np.array([datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S+0000') for dtime in station['OBSERVATIONS']['date_time']])
        dates = (dates + timedelta(hours=-8)).tolist()
#        print(f"        Datetime format is '%Y-%m-%dT%H:%M:%S+0000'.")
    return dates

def calculate_airport_precip(station, all_data):
    precip_nan = (np.array(station['OBSERVATIONS']['precip_accum_one_hour_set_1'], dtype = float)) * 0.03937 
    precip_nonan = np.nan_to_num(precip_nan)
    precip = np.empty(len(precip_nonan))
    precip[0] = precip_nonan[0]
    for ii in range(1, len(precip_nonan)):
        if precip_nonan[ii] == 0.0:
            precip[ii] = precip[ii-1]
        elif precip_nonan[ii] < precip_nonan[ii-1]:
            precip[ii] = precip_nonan[ii] + precip[ii-1]
        else:
            precip[ii] = precip_nonan[ii] - precip_nonan[ii-1] + precip[ii-1]
    return precip

"""
#THIS IS THE ORIGINAL FUNCTION THAT SEEMS NOT TO START ACCUMULATED RAINFALL AT ZERO
def get_precip(station, all_data):
#    if station['NAME'].endswith("MESONET") or station['NAME'].endswith("4E"):
    if station['NAME'].endswith("MESONET") or station['NAME'] == 'SAWMILL CREEK NEAR SITKA 4E':
        min_rain = min(np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float))
        # subtract min rainfall amt from each obs to start all data at zero
        precip = (np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float) - min_rain) * 0.03937
    elif station['NAME'] == 'Sitka - Sitka Airport':
        precip = calculate_airport_precip(station, all_data)
    elif station['NAME'] == 'USCRN SITE NEAR SITKA 1NE':
#        print(station['NAME'])
        min_rain = min(np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float))
        precip = (np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float) - min_rain) * 0.03937
    elif station['NAME'] == 'Harbor Mountain':
        min_rain = min(np.array(station['OBSERVATIONS']['precip_accum_fifteen_minute_set_1'], dtype = float))
        precip = (np.array(station['OBSERVATIONS']['precip_accum_fifteen_minute_set_1'], dtype = float) - min_rain) * 0.03937

    return precip

"""
def filter_nans(station,dates, precip):
    """ filter out data with nans """
#    print(f"     Removing NaNs from {station['NAME']}...")
    dates_list = [] # create empty list
    precip_list = []
    data = zip(dates, precip)
    # look through date and rain values saving values != nan
    for date, rain in data:
        if rain[~np.isnan(rain)]: 
            dates_list.append(date)
            precip_list.append(rain)
            dates = np.array(dates_list)
            precip = np.array(precip_list)
    return dates, precip

def clean_data(data):
    precip = []
    precip.append(data[0]-data[0])
    for ii in range(1, len(data-2)):
        if data[ii] >= data[ii-1]:
            precip.append(abs(data[ii] - data[0]))
        elif data[ii] == 0.0:
            precip.append((data[ii-1] - data[0]))
        elif data[ii] < precip[ii-1] and data[ii] != 0.0:
            precip.append(precip[ii-1] + data[ii])
        else:
            print("     Something is wrong, please carefully examine the data.")
    return precip


def get_precip(station, all_data):
#    if station['NAME'].endswith("MESONET") or station['NAME'].endswith("4E"):
    if station['NAME'].endswith("MESONET"):
        data = np.array([float(value) for value in station['OBSERVATIONS']['precip_accum_set_1']])
    if station['NAME'] == 'SAWMILL CREEK NEAR SITKA 4E':
        data = (np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float))
        print(station['OBSERVATIONS']['precip_accum_set_1'])
    elif station['NAME'] == 'Sitka - Sitka Airport':
        data = calculate_airport_precip(station, all_data)
    elif station['NAME'] == 'USCRN SITE NEAR SITKA 1NE':
#        data = np.array([float(value) for value in station['OBSERVATIONS']['precip_accum_set_1']])
        data = (np.array(station['OBSERVATIONS']['precip_accum_set_1'], dtype = float))
#    elif station['NAME'] == 'Harbor Mountain':
#        zeroth_precip = np.array(station['OBSERVATIONS']['precip_accum_fifteen_minute_set_1'])[0]
#        precip = (np.array(station['OBSERVATIONS']['precip_accum_fifteen_minute_set_1'], dtype = float) - zeroth_precip) * 0.03937 
    return data

 

def get_wind_direction(station, all_data):
    if station['NAME'] == 'Sitka - Sitka Airport':
        wind_dir_deg = (np.array(station['OBSERVATIONS']['wind_direction_set_1'], dtype = float)) 
        wind_speed = (np.array(station['OBSERVATIONS']['wind_speed_set_1'], dtype = float)) 
    elif station['NAME'] != 'Sitka - Sitka Airport':
        print("This station doesn't collect wind data.")
        wind_dir = None
        wind_speed = None
    return wind_dir_deg, wind_speed

def get_wind_data(station,all_data):
    if station['NAME'] == 'Sitka - Sitka Airport':
        wind_dir, wind_speed = get_wind_direction(station,all_data)
        V = wind_speed*np.rad2deg(np.cos(np.deg2rad(wind_dir)))
        U = wind_speed*np.rad2deg(np.sin(np.deg2rad(wind_dir)))
    return U, V, wind_dir, wind_speed


def make_datetime_list(first_datetime, length, tdelta):
    first = first_datetime
    delta = timedelta(minutes=tdelta)
    dates = list((first + delta * x for x in range(length)))
    return dates

import pytz 
def convert_utc_to_alaska(utc_datetime_array):
    # create both timezone objects
    old_timezone = pytz.timezone("Etc/UTC")
    new_timezone = pytz.timezone("America/Anchorage")
    local_datetime_array = []
    for utc_datetime in utc_datetime_array:
        # two-step process
        localized_timestamp = old_timezone.localize(utc_datetime)
        local_datetime_array.append(localized_timestamp.astimezone(new_timezone))
    return local_datetime_array
