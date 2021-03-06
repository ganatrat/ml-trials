from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from regression.example import load_sample_data_for_linear_regression

if __name__ == '__main__':
    df, forecast_col, forecast_out = load_sample_data_for_linear_regression()

    ##
    # features = X
    ##

    X = np.array(df.drop('label', 1))

    # scaling features...
    X = preprocessing.scale(X)

    X_lately = X[-forecast_out:]  # we don't have y - values for...
    X = X[:-forecast_out]

    ##
    # label = y
    ##

    # dropping data with no future data
    df.dropna(inplace = True)
    y = np.array(df['label'])

    # training and test data sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    classifier = LinearRegression()
    classifier.fit(X_train, y_train)  # training the classifier
    accuracy = classifier.score(X_test, y_test)
    print("'Linear Regression' accuracy: ", accuracy)

    forecast_set = classifier.predict(X_lately)
    # print("Forecast: ")
    # for v in forecast_set:
    #     print(f" - {v}")

    ##
    # plotting the data
    ##

    df['Forecast'] = np.nan
    # print(df.head())

    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day

    for i in forecast_set:
        next_date = datetime.fromtimestamp(next_unix)
        next_unix += one_day

        # print(next_unix, next_date, wit + [i])
        df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1)] + [i]

    style.use('ggplot')

    df['Adj. Close'].plot()
    df['Forecast'].plot()
    plt.legend(loc = 4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    # fname = f"../share/.transient/{datetime.now()}.png"
    # with open(fname, "x") as f:
    #     plt.savefig(fname)
