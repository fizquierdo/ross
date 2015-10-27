#!/bin/sh
echo " ==== Splitting train / test dataset ===="
python sample_input.py
echo " ==== Median prediction benchmark  ===="
python predict_with_sales.py
echo " ==== Prediction with linear regression ===="
python predict_with_lr.py
echo " ==== Evaluate solution ====="
python eval_solution.py
