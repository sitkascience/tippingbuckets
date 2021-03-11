from soil_moisture_funcs import *
from plot_funcs import *
import matplotlib.pyplot as plt

dat = read_sm_data('/Users/CoraJune/Documents/GitHub/sitkaPrecip/test40.csv', '2020-08-10 00:00:0000', '2020-08-17 00:00:0000')

dat['tAM_conv'] = pd.DataFrame(convert_analog_sm(dat.tAM))
dat['tBM_conv'] = pd.DataFrame(convert_analog_sm(dat.tBM))
dat['tCM_conv'] = pd.DataFrame(convert_analog_sm(dat.tCM))

fig, ax1 = plt.subplots()
p1 = dat.plot(kind='line',x='datetime', y=['tAM_conv', 'tBM_conv','tCM_conv'], ax=ax1)

ax1.set(ylabel="Volume of Water / Volume of Soil")
ax1.set_title("Soil Moisture")
leg = ax1.legend(loc="upper left", prop={'size': 6},
            ncol=2, shadow=False, fancybox=False)
format_xticks(p1)
plt.tight_layout()
plt.show()
