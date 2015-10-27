#!/usr/bin/env python

'''
Evaluate the solution
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

solution_file = '../input/sampled/test_solution.csv'
submission_file = 'predictions.csv'
median_file = 'median_predictions.csv'

solution = pd.read_csv(solution_file)

def eval_prediction(submission_file, solution):
	submission = pd.read_csv(submission_file )
	assert(len(solution) == len(submission))
	# rename the Sales column in the prediction
	submission=submission.rename(columns = {'Sales':'Sales_predicted'})

	evaluation = pd.merge(submission, solution, on = ['Id'], how = 'left' )
	
	# calculate the score metric defined in kaggle
	# RMSPE = sqr_root( (1/n) * sum( ((y_i-y_pred)/(y_i))^2 ) )
	evaluation['diff']      = evaluation['Sales'] - evaluation['Sales_predicted']
	evaluation['sqr_error'] = (evaluation['diff']/evaluation['Sales'])**2
	
	# some values are nan due to division by 0.0
	#rmspe = np.sqrt(np.sum(evaluation['sqr_error'])/float(len(evaluation)))
	evaluation.loc[evaluation.sqr_error.isnull(), 'sqr_error' ] = 0.0
	rmspe = np.sqrt(np.mean(evaluation['sqr_error']))
	return (evaluation, rmspe)

evaluation, rmspe = eval_prediction(submission_file, solution)
median_evaluation, median_rmspe = eval_prediction(median_file, solution)
	
print 'Distribution of the errors (Linear Regression)'
print evaluation.describe()
print 'RMSPE', rmspe
print 'Distribution of the errors (Grouped median)'
print median_evaluation.describe()
print 'Median-based RMSPE', median_rmspe

plt.figure();
evaluation['diff'].hist(bins=200, label='lr', alpha=0.5)
median_evaluation['diff'].hist(bins=200, label='grouped median', alpha=0.5)
plt.title('Distribution of difference')
plt.legend()
plt.show()

# Detailed analysis
'''
evaluation['sqr_error'].hist(bins=200)
plt.title('Distribution of square error')
plt.show()
evaluation['sqr_error'].plot(kind='box', title='distribution of square error')
plt.show()
evaluation['sqr_error'].cumsum().plot(title='cumsum of sqr err', label='std')
threshold = np.percentile(list(evaluation['sqr_error']), 99)
# eliminate the worst 1% of the error
evaluation.loc[evaluation.sqr_error > threshold, 'sqr_error'] = 0.0
evaluation['sqr_error'].cumsum().plot(label='without worst 1% error')
plt.legend(loc='upper left')
plt.show()
'''
