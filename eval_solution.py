#!/usr/bin/env python

'''
Evaluate the solution
'''

import pandas as pd
import numpy as np

solution_file = '../input/sampled/test_solution.csv'
submission_file = 'predictions.csv'

solution = pd.read_csv(solution_file)
submission = pd.read_csv(submission_file )
# rename the Sales column in the prediction
submission=submission.rename(columns = {'Sales':'Sales_predicted'})

assert(len(solution) == len(submission))

# calculate the score metric defined in kaggle
# RMSPE = sqr_root( (1/n) * sum( ((y_i-y_pred)/(y_i))^2 ) )

evaluation = pd.merge(submission, solution, on = ['Id'], how = 'left' )

evaluation['diff'] = evaluation['Sales'] - evaluation['Sales_predicted']
evaluation['sqr_error'] = (evaluation['diff']/evaluation['Sales'])**2

def compute_rmspe(evaluation):
	# TODO investigate how to do this with apply directely in a dataframe
	# calculate the RMSPE
	sum_sqr_err = 0.0
	for sales,pred in zip(list(evaluation['Sales']),list(evaluation['Sales_predicted'])):
		if sales == 0:
			assert(pred==0.0) # would be nan after dividing by 0
		else:
			sum_sqr_err += (float(sales - pred)/float(pred))**2
	
	return np.sqrt(sum_sqr_err/float(len(evaluation)))
	
print 'Distribution of the errors'
print evaluation.describe()
print 'RMSPE', compute_rmspe(evaluation)
