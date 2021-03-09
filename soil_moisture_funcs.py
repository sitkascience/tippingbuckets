import pandas as pd
import pytz

#def read_sm_data(file_path, start_datetime, end_datetime):
#    sm_dat = pd.read_csv(file_path, header=4)
#    sm_dat.columns = ['name','instance','dateString','time','packetNumber',
#            'S0temp','S0cap','S1temp','S1cap','S2cap','S2cap','M4pressure',
#            'M4temp','M5pressure','M5temp','S7temp','S7humid','vbat','tAM',
#            'tAT','tBM','tBT','tCM','tCT','tip','accel','rssi',' ']

def read_sm_data(file_path, start_datetime, end_datetime):
    sm_dat = pd.read_csv(file_path, header=4)
    sm_dat.columns = ['name','instance','dateString','time','packetNumber',
            'S0temp','S0cap','S1temp','S1cap','S2cap','S2cap','M4_pressure',
            'M4temp','M5_pressure','M5temp','S7temp','S7humid','vbat','tAM',
            'tAT','tip','accel','rssi',' ']

    # merge date column with time column to make a new datetime colume
    datetime = pd.to_datetime(sm_dat['dateString'].apply(str)+' '+sm_dat['time'])
    sm_dat['datetime'] = datetime   # add datetime column to df

    start_date = start_datetime
    end_date = end_datetime

    mask = (sm_dat['datetime'] >= start_datetime) & (sm_dat['datetime'] <=
            end_datetime)
    sm_sub = sm_dat.loc[mask]
    print("SM SUB")
    print(sm_sub.datetime)

#    df[ts] = [datetime.fromtimestamp(x) for x in df[ts]]
    return sm_sub

    

def convert_analog_sm(data):
        vwvs = (3.879*10E-4)*data-0.6956
        return vwvs