#!/usr/bin/env python

'''
Predict Sales as a historical median for a given store, day of week, and promo
This script scores 0.13888 on the public leaderboard on the original input dataset
'''

import pandas as pd

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

# Group by triplets 
columns = ['Store', 'DayOfWeek', 'Promo']
medians = train.groupby( columns )['Sales'].median()
medians = medians.reset_index()

# each entry in the test dataset has a unique triplet ? 
# assign median to each row
test2 = pd.merge( test, medians, on = columns, how = 'left' )
assert( len( test2 ) == len( test ))

test2.loc[ test2.Open == 0, 'Sales' ] = 0
assert( test2.Sales.isnull().sum() == 0 )

test2[[ 'Id', 'Sales' ]].to_csv( output_file, index = False )
