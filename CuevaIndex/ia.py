import numpy as np 
import pandas as pd
#Load the data
import ccxt
exchange = ccxt.binanceusdm()
exchange.fetch_tickers()
bars = exchange.fetch_index_ohlcv('BTC/USDT', timeframe='1d')
df = pd.DataFrame(bars, columns=['timestamp','Open','High','Low','Price','Volume'])
df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df.loc[:, ['Date', 'Price']]
print(df)
#print(df)
#Store the data into the variable df
df.head(7)
#Remove the Date column
df.drop(['Date'], 1, inplace=True)
# a variable for predict 'n' days out in the future
prediction_days = 30
#create another column  shifted 'n' unit up
df['Prediction'] = df[['Price']].shift(-prediction_days)
#show the first 7 rows of the dataset
df.head(7)
#show the last 7 rows of new dataset
df.tail(7)
#create the independetn data set
#convert the dataframe to numpy aarray and drop the prediction column
X = np.array(df.drop(['Prediction'],1))
# remove the last 'n' rows where 'n' is the prediction_days
X = X[:len(df)-prediction_days]
#print(X)
# create the dependetn data set
#covert teh dataframe to a numpy array
Y= np.array(df['Prediction'])
# get all of tge values except the last 'n' rows
Y= Y[:-prediction_days]
#print(Y)
#split the data into 80% training and 20% testing
from sklearn.model_selection import train_test_split
X_Train, X_test, Y_train, Y_test=  train_test_split(X,Y, test_size=0.2)
#set the prediction_days_array equañ to the last 30 rows from the original data set
prediction_days_array= np.array(df.drop(['Prediction'],1))[-prediction_days:]
#print(prediction_days_array)

from sklearn.svm import SVR

#create and train the support Vector machine (regresion) using radial basis function
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00001)
svr_rbf.fit(X_Train, Y_train)
#test the model
svr_rbf_confidence = svr_rbf.score(X_test, Y_test)
#print("svr_rbf accuracy: ", svr_rbf_confidence)
#print the predicted values
svm_prediction = svr_rbf.predict(X_test)

#print(svm_prediction)
#print()
#print(Y_test)

#print the model predictions for the next 'n=30' days
svm_prediction = svr_rbf.predict(prediction_days_array)
print(svm_prediction)
#print()
#print the acttual price for the next 30 days

from datetime import datetime, timedelta
import calendar

last_day = datetime.now().replace(day=calendar.monthrange(datetime.now().year, datetime.now().month)[1]).strftime('%Y-%m-%d')

days = []
for i in range(prediction_days):
    day = (datetime.strptime(last_day, '%Y-%m-%d') + timedelta(days=i+1)).strftime('%Y-%m-%d')
    days.append(day)
    
df.loc[df.index[-prediction_days:], 'Prediction'] = pd.to_datetime(days)

print(df.tail(prediction_days))
import matplotlib.pyplot as plt

df.tail(prediction_days).plot(x='Prediction', y='Price')
plt.show()