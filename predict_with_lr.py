#!/usr/bin/env python

'''
Predict Sales as a historical median for a given store, day of week, and promo
This script scores 0.13888 on the public leaderboard on the original input dataset
'''

import pandas as pd
from sklearn.linear_model import LinearRegression

## original files
#train_file = '../input/train.csv'
#test_file = '../input/test.csv'

train_file = '../input/sampled/train.csv'
test_file = '../input/sampled/test.csv'
output_file = 'predictions.csv'

train = pd.read_csv(train_file)
test = pd.read_csv(test_file)

# remove rows with zero sales
# mostly days where closed, but also 54 days when not
train = train.loc[train.Sales > 0]

# remove NaNs from Open
# set to 1 the field 'open', for rows where it was blank
test.loc[ test.Open.isnull(), 'Open' ] = 1

# Linear regression: create X and Y
# following example from  http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb
columns = ['Store', 'DayOfWeek', 'Promo']

X = train[columns]
y = train.Sales

lm = LinearRegression()
lm.fit(X,y)

print "Linear regression coeffs"
print lm.intercept_
print zip(columns, lm.coef_)

predicted_sales = lm.predict(test[columns])
assert(len(predicted_sales) == len(test))
test['Sales'] = predicted_sales
test.loc[ test.Open == 0, 'Sales' ] = 0.0

test[[ 'Id', 'Sales' ]].to_csv( output_file, index = False )
