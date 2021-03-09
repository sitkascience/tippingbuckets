import numpy as np
from datetime import datetime, timedelta

def get_IR_timeseries(data, data_type):
    dates_list = []
    values_list = []
    if data_type == 'height':
        for dtime in range(len(data['value']['timeSeries'][1]['values'][0]['value'])-1):
            values_list.append(float(data['value']['timeSeries'][1]['values'][0]['value'][dtime]['value']))
            dates_list.append([datetime.strptime(data['value']['timeSeries'][1]['values'][0]['value'][dtime]['dateTime'],'%Y-%m-%dT%H:%M:%S.%f-08:00')])
    elif data_type == 'discharge':
        for dtime in range(len(data['value']['timeSeries'][0]['values'][0]['value'])-1):
            values_list.append(float(data['value']['timeSeries'][0]['values'][0]['value'][dtime]['value']))
            try:
                dates_list.append([datetime.strptime(data['value']['timeSeries'][0]['values'][0]['value'][dtime]['dateTime'],'%Y-%m-%dT%H:%M:%S.%f-08:00')])
            except:
                dates_list.append([datetime.strptime(data['value']['timeSeries'][0]['values'][0]['value'][dtime]['dateTime'],'%Y-%m-%dT%H:%M:%S.%f-09:00')])
    values = np.array(values_list)
    dates = np.array(dates_list)
    return dates, values




