import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#Time up your execution
start_time = time.time()

#Load the data
train_data = pd.read_csv('../train.csv')
test_data = pd.read_csv('../test.csv')

#Take a look at the columns/features
train_column_names = list(train_data.axes[1])
print(train_column_names)
test_column_names = list(test_data.axes[1])
print(test_column_names)

#get a summary of the training data
train_data.describe(include='all') #by default, describe() only returns numerical columns.

#plot data
def add_jitter(arr):
    return arr + (np.random.random(len(arr))-0.5)*arr.std()*0.1

pickup_hour = np.array([dt.strptime(x, '%Y-%m-%d %H:%M:%S').hour for x in sample['pickup_datetime'].values])

window = plt.get_current_fig_manager().window
screen_x = np.floor(window.winfo_screenmmwidth()/25.4)
screen_y = np.floor(window.winfo_screenmmheight()/25.4)

plt.figure(figsize=[screen_x*0.75, screen_y*0.75])
plt.plot(add_jitter(pickup_hour), np.log(sample['trip_duration'].values), 'r.')
plt.xticks(np.arange(24))
plt.xlabel('Hour of Pickup')
plt.ylabel('Log of Trip Duration')
plt.title('Trip Duration by Pickup Hour')
plt.show()
