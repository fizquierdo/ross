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
#columns = ['Store', 'DayOfWeek', 'Promo']

def fit_lm(train, test, columns):
	# using the customers only improves if we cheat and use the true one, 
	# using the median it gets worse than if ignoring the Customers field
	#columns += ['Customers']
	X = train[columns]
	y = train.Sales
	lm = LinearRegression()
	lm.fit(X,y)
	#print "Linear regression coeffs"
	#print lm.intercept_
	#print zip(columns, lm.coef_)
	predicted_sales = lm.predict(test[columns])
	assert(len(predicted_sales) == len(test))
	test['Sales'] = predicted_sales
	return test

# the solution
df_solution = pd.DataFrame()

# create partitions of the data based on the day of the week
# each store needs its own partition too
for day in range(1,8):
	day_train = train.loc[train.DayOfWeek==day]
	day_test  = test.loc[test.DayOfWeek==day]
	num_stores = len(day_test['Store'].unique())
	print 'day', day, len(day_train), len(day_test)

	for store in range(1, num_stores + 1):
		day_store_train = day_train.loc[day_train.Store==store]
		day_store_test  = day_test.loc[day_test.Store==store]
		uniq_vals = day_store_test['Open'].unique()
		if len(uniq_vals) == 1 and uniq_vals[0] == 0:
			# special case where no training is required
			day_store_test['Sales'] = 0.0
		else:
			# just get the median for these days (we can predict the customers better)
			#day_store_test['Customers'] = day_store_train['Customers'].median()
			try: 
				columns = ['Promo', 'SchoolHoliday', 'StateHoliday']
				day_store_test = fit_lm(day_store_train, day_store_test, columns)
			except:
				# TODO check what is the trouble with the StateHoliday
				columns = ['Promo', 'SchoolHoliday']
				day_store_test = fit_lm(day_store_train, day_store_test, columns)

		df_solution = pd.concat([df_solution, day_store_test])

df_solution.loc[ df_solution.Open == 0, 'Sales' ] = 0.0
df_solution = df_solution.sort(['Id'])
df_solution[[ 'Id', 'Sales' ]].to_csv( output_file, index = False )
