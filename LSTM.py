import numpy as np
from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from pandas import Series
from pandas import concat
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from math import sqrt

#date-time parsing function for loading the dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

#transform data into supervised learning data format so that input as data point x (i) will be labeled as data point x (i + 1)
def superviseds (data,lag=1) :
    df = DataFrame(data)
    cl = [df.shift(i) for i in range(1,lag+1)]
    cl.append(df)
    df = concat(cl, axis=1)
    df.fillna(0, inplace=True)
    return df

#transform data into stationary series
def difference (x_train , interval = 1 ):
    diff= list()
    for i in range(interval, len(x_train)):
        val = x_train [i]-x_train[i-interval]
        diff.append(val)
    return Series(diff)

#inverse stationary series
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

#Convert values of data in the range (-1,1)
def scale (x_train,x_test ):
    scaler=MinMaxScaler(feature_range=(-1,1)).fit(x_train)
    x_train = x_train.reshape(x_train.shape[0],x_train.shape[1])
    train_scaler=scaler.transform(x_train)
    x_test=x_test.reshape(x_test.shape[0],x_train.shape[1])
    test_scaler=scaler.transform(x_test)
    return scaler , train_scaler, test_scaler

#Reverse the values ​​in the range (-1, 1) to the original data
def inverse_scale(scale,X,value):
    a=[x for x in X]+[value]
    a=np.array(a)
    a=a.reshape(1,len(a))
    inverse= scale.inverse_transform(a)
    return inverse[0,-1]

#Training and return model with MSE loss funcition  and ADAM optimization algorithm
def fit_lstm(train, batch_size, nb_epoch, neurons):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
		model.reset_states()
	return model

#Use the model to predict values
def predict_LSTM (model , batch_size, X):
    X=X.reshape(1,1,len(X))
    yhat=model.predict (X,batch_size=batch_size)
    return yhat[0,0]

#load data
series = read_csv('Shampo_sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
x=series.values
#Standardized input data
diff_x=difference(x,1)
supervised= superviseds(diff_x,1)
supervised_values=supervised.values
train,test=supervised_values[0 :-12],supervised_values[-12:]
scale,train_scale,test_scale= scale(train,test)
#train
model = fit_lstm(train_scale,1,3000,4)
train_reshape= train_scale[:,0].reshape(len(train_scale),1,1)
#predict
model.predict(train_reshape,batch_size=1)

predictions=list()
for i in range (len(test_scale)):
    X=test_scale[i,0:-1]
    y=test_scale[i,-1]
    yhat = predict_LSTM(model , 1,X)
    yhat = inverse_scale(scale,X,yhat)
    yhat = inverse_difference(x, yhat, len(test_scale) + 1 - i)
    predictions.append(yhat )
    expected= x[len(train)+i+1]
    print ('moth=%d,predict=%f,expect=%f' %(i+1,yhat,expected))

rmse=sqrt(mean_squared_error(x[-12:],predictions))
print ('RMSE :',rmse)
plt.plot(x[-12:])
plt.plot(predictions)
plt.show()
