import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

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

#get a sample of the data
sample = train_data.sample(n=10000, random_state=64)

def add_jitter(arr):
    return arr + (np.random.random(len(arr))-0.5)*arr.std()*0.1

pickup_hour = np.array([dt.strptime(x, '%Y-%m-%d %H:%M:%S').hour for x in sample['pickup_datetime'].values])

#plot data
import tkinter as tk
window = tk.Tk() #This opens a window
screen_x = np.floor(window.winfo_screenmmwidth()/25.4)
screen_y = np.floor(window.winfo_screenmmheight()/25.4)
window.destroy() #This destroys the extra window

plt.figure(figsize=[screen_x*0.75, screen_y*0.75])
plt.plot(add_jitter(pickup_hour), np.log(sample['trip_duration'].values), 'r.')
plt.xticks(np.arange(24))
plt.xlabel('Hour of Pickup')
plt.ylabel('Log of Trip Duration')
plt.title('Trip Duration by Pickup Hour')
#plt.rcParams["figure.figsize"]=[screen_x*0.75, screen_y*0.75]
plt.show()

#Tackle the problem with a random forest
import sklearn.ensemble

#create classifier
rf_classifier = sklearn.ensemble.RandomForestRegressor(n_jobs=2, n_estimators=100)

#train classifier
rf_classifier.fit(sample[['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude']], sample['trip_duration'])

#get score on training dataset
rf_benchmark = rf_classifier.score(sample[['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude']],\
                                    sample['trip_duration'])

#get predictions on test dataset
rf_predictions = rf_classifier.predict(test_data[['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude']])

#create submission .csv file
submission_file = pd.DataFrame(([x,y] for x,y in zip(test_data['id'],rf_predictions)), columns = ['id', 'trip_duration'])
submission_file.to_csv('submission_file.csv', index = False)
