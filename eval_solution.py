#!/usr/bin/env python

'''
Evaluate the solution
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

solution_file = '../input/sampled/test_solution.csv'
submission_file = 'predictions.csv'

solution = pd.read_csv(solution_file)
submission = pd.read_csv(submission_file )
# rename the Sales column in the prediction
submission=submission.rename(columns = {'Sales':'Sales_predicted'})

assert(len(solution) == len(submission))

evaluation = pd.merge(submission, solution, on = ['Id'], how = 'left' )

# calculate the score metric defined in kaggle
# RMSPE = sqr_root( (1/n) * sum( ((y_i-y_pred)/(y_i))^2 ) )
evaluation['diff']      = evaluation['Sales'] - evaluation['Sales_predicted']
evaluation['sqr_error'] = (evaluation['diff']/evaluation['Sales'])**2

# some values are nan due to division by 0.0
#rmspe = np.sqrt(np.sum(evaluation['sqr_error'])/float(len(evaluation)))
evaluation.loc[evaluation.sqr_error.isnull(), 'sqr_error' ] = 0.0
rmspe = np.sqrt(np.mean(evaluation['sqr_error']))
	
print 'Distribution of the errors'
print evaluation.describe()
print 'RMSPE', rmspe

plt.figure();
evaluation['diff'].hist(bins=200)
plt.title('Distribution of difference')
plt.show()
evaluation['sqr_error'].hist(bins=200)
plt.title('Distribution of square error')
plt.show()
evaluation['sqr_error'].plot(kind='box', title='distribution of square error')
plt.show()
evaluation['sqr_error'].cumsum().plot(title='cumulative sum of square error')
plt.show()
# to see all data points (takes very long)
#evaluation['sqr_error'].plot()
#plt.show()
