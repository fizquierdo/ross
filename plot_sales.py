#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd

# Input train set
train_file = '../input/train.csv'
train = pd.read_csv(train_file)

# Get an initial idea of what info is there
print train.describe()

rows = 2
cols = 2
fig = plt.figure()

# Distribution of sales (no matter which store they come from) 
sales = train['Sales']

ax1 = fig.add_subplot(rows, cols, 1)
ax1.hist(list(sales), bins=100)
ax1.set_title("Number of sales from {} data points".format(len(sales)))
ax1.set_xlabel('Sales')

# Distribution of customers (no matter which store they come from) 
customers = train['Customers']

ax2 = fig.add_subplot(rows, cols, 2)
ax2.hist(list(customers), bins=100)
ax2.set_title("Number of customers from {} data points".format(len(customers)))
ax2.set_xlabel('Customers')

# sales per number of customers
ax3 = fig.add_subplot(rows, cols, 3)
n = 2000
ax3.plot(customers[:n], sales[:n], '.', alpha=0.5)
ax3.set_xlabel('customers')
ax3.set_ylabel('sales')
ax3.set_title('Sales per customer on first {} data points'.format(n))

plt.show()

# the days that the shop is closed should not count
# each shop may have a different behaviour, maybe build clusters of shops?
