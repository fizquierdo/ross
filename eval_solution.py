#!/usr/bin/env python

'''
Evaluate the solution
'''

import pandas as pd

solution_file = '../input/sampled/test_solution.csv'
submission_file = 'predictions.csv'

solution = pd.read_csv(solution_file)
submission = pd.read_csv(submission_file )

assert(len(solution) == len(submission))
