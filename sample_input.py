#!/usr/bin/env python

'''
Sample the train set to generate new test/train sets for local evaluation
'''

import pandas as pd

train_file = '../input/train.csv'
wdir = '../input/sampled/'

train = pd.read_csv( train_file )
threshold_date = '2015-06-01'
newtrain = train.loc[train.Date <= threshold_date] # 950,309
newtest  = train.loc[train.Date > threshold_date] # 66,900
assert (len(train) == len(newtrain) + len(newtest)) 

newtrain.to_csv(wdir+'train.csv')

print 'total set', len(train)
print 'new test set', len(newtest), len(newtest.loc[newtest.DayOfWeek==7])
print 'new train set', len(newtrain)

# New ids
ids = range(1,len(newtest)+1)

# Construct the known solution
df_solution = pd.DataFrame(ids, columns=['Id'])
df_solution['Sales'] = newtest['Sales']
assert(len(df_solution) == len(newtest))
df_solution.to_csv(wdir+'test_solution.csv', index = False)

# Construct the test dataset with the fields available
cols = ['Store','DayOfWeek','Date','Open','Promo','StateHoliday','SchoolHoliday']
# Add the Customers feature (not available in the real test dataset)
#cols += ['Customers']
df_newtest = pd.DataFrame(ids, columns=['Id'])
df_newtest[cols] = newtest[cols]
assert(len(df_newtest) == len(newtest))
df_newtest.to_csv(wdir+'test.csv', index = False)
