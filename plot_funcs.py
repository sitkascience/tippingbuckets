from matplotlib.dates import DateFormatter, YearLocator, MonthLocator, DayLocator, HourLocator
import matplotlib.pyplot as plt

def format_xticks(ax):
    # format the x ticks
#    print("     Formatting xticks...")
    months = MonthLocator()
    days = DayLocator()
    hours = HourLocator(byhour=[0,12,24])
    hours2 = HourLocator(byhour=[0,2,4,6,8,10,12,14,16,18,20,22,24])
#    hours = HourLocator(byhour=[0,6])
#    hours_each = HourLocator() # Find all hours
    dateFmt = DateFormatter('%b-%d\n%H:%M') # Tick label format style
#    dateFmt = DateFormatter('%b-%d') # Tick label format style
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(dateFmt) # Set the x-axis labels
    ax.xaxis.set_minor_locator(hours2)
    plt.xticks(rotation=30)
    return ax

def save_plot(ax, plt, start_time, end_time, legend_loc, title, ylabel, plot_type):
    ax.legend(loc=legend_loc, prop={'size': 7})
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig("/Users/CoraJune/Documents/GitHub/sitkaPrecip/figures/" + plot_type + '_' + start_time + '_' + end_time + '.png', format='png')

def make_bar_chart():
    pass
