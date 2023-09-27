#Author: Chetan Kumar ckumaronline@gmail.com
#Recommended Opportunities ML framework
#To do: PEP 8 format, descriptive comments, g3 compatible
#y = 'is_accepted2'
#x = present_impact_surfaced_start', 'accepted_same_gt_product_previous_Q', 'product_group'
#lcs_us_eng_chi_01_edu_q117_data train_test_split = 0.5
#ML algorithms tested: decision tree, logistic regression, random forest

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats
from pylab import *
import sys
import pydot  

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals.six import StringIO

if __name__ == "__main__":
#chi_01_edu_q117_product_group_impact_start
	chi_01_edu_q117_product_group_impact_start = pd.read_csv('/Users/kumarchetan/Documents/workcode/ropps/data/lcs_us_eng_chi_01_edu_q117_data_product_group_present_impact_surfaced_start.csv')
	print 'chi_01_edu_q117_product_group_impact_start'
#dictionary for creating categorical variables features
	d = {'Adopt': 0, 'Expand': 1, 'Optimize': 2}
	chi_01_edu_q117_product_group_impact_start['intent'] = chi_01_edu_q117_product_group_impact_start['intent'].map(d)
	d = {'Global Performance': 0, 'Global Brand': 1, 'Custom Lead List': 2}
	chi_01_edu_q117_product_group_impact_start['product_segment'] = chi_01_edu_q117_product_group_impact_start['product_segment'].map(d)
	d = {'Display': 1, 'Search': 2, 'Video': 3}
	chi_01_edu_q117_product_group_impact_start['product_group'] = chi_01_edu_q117_product_group_impact_start['product_group'].map(d)

#OLS regression accepted vs present_impact_surfaced_start + accepted_same_gt_product_previous_Q + product_group
	X = chi_01_edu_q117_product_group_impact_start[['present_impact_surfaced_start', 'accepted_same_gt_product_previous_Q', 'product_group']]
	y = chi_01_edu_q117_product_group_impact_start[['is_accepted2']]
#not adding a constant setting intercept = 0
	est = sm.OLS(y, X).fit()
	print "OLS regression chi_01_edu_q117_product_group_impact_start accepted vs present_impact_surfaced_start + accepted_same_gt_product_previous_Q + product_group"
	print est.summary()
	print 'r squared: ', est.rsquared
	print 'p value: ', est.pvalues
	print 'params: ', est.params
	print 'params[0]: ', est.params[0]
	print 'params[1]: ', est.params[1]
	print 'params[2]: ', est.params[2]
	print '\n'

#decision tree predicting accept vs product_group + present_impact_surfaced_start + accepted_same_gt_product_previous_Q
	features = list(chi_01_edu_q117_product_group_impact_start[['product_group', 'present_impact_surfaced_start', 'accepted_same_gt_product_previous_Q']])
	print 'decision tree predicting accept vs product_group + present_impact_surfaced_start + accepted_same_gt_product_previous_Q'
	print 'features for predicting accept'
	print features
	print '\n'

	y = chi_01_edu_q117_product_group_impact_start['is_accepted2']
	X = chi_01_edu_q117_product_group_impact_start[features]
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X,y)

#Predict accept classification of | product_group = 2 search | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 1
	print 'Predict using Decision Tree classifier accept classification of | product_group = 2 search | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 1 | predict accept = ', clf.predict([[2, 1, 1]])
#...and | product_group = 2 search | present_impact_surfaced_start = 0 | accepted_same_gt_product_previous_Q = 1
	print 'Predict using Decision Tree classifier accept classification of | product_group = 2 search | present_impact_surfaced_start = 0 | accepted_same_gt_product_previous_Q = 1 | predict accept = ', clf.predict([[2, 0, 1]])
#...and | product_group = 1 display | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 1
	print 'Predict using Decision Tree classifier accept classification of | product_group = 1 display | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 1 | predict accept = ', clf.predict([[1, 1, 1]])
#...and | product_group = 3 video | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 0
	print 'Predict using Decision Tree classifier accept classification of | product_group = 3 video | present_impact_surfaced_start = 1 | accepted_same_gt_product_previous_Q = 0 | predict accept = ', clf.predict([[3, 1, 0]])
	print 'try live [2, 1, 1] = ', clf.predict([[2, 1, 1]])
	print '\n'

#decision tree visualization
	from sklearn.externals.six import StringIO
	import pydot
	dot_data = StringIO()
	tree.export_graphviz(clf, out_file=dot_data, feature_names=features)
	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	graph.write_pdf("chi_01_edu_q117_product_group_impact_start_decision_tree_2.pdf")

#decision tree prediction accuracy
#replaced sklearn.model_selection instead of sklearn.cross_validation no more deprecation warning
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

	from sklearn import tree
	my_classifier = tree.DecisionTreeClassifier()
	my_classifier.fit(X_train, y_train)
	predictions = my_classifier.predict(X_test)
	print 'decision tree classification predictions'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'decision tree prediction accuracy score'
	print accuracy_score(y_test, predictions)
	print '\n'

#logistic regression predicition accuracy
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

	from sklearn.linear_model import LogisticRegression
	my_classifier = LogisticRegression()
	my_classifier.fit(X_train, y_train)
	print 'logistic regression model'
	print(my_classifier)
	print 'logistic regression coefficients'
	print my_classifier.coef_
	print 'logistic regression intercept'
	print my_classifier.intercept_
	predictions = my_classifier.predict(X_test)
	print 'logisitic regression classification predictions'
	print predictions
	
	from sklearn.metrics import accuracy_score
	print 'logisitic regression prediction accuracy score'
	print accuracy_score(y_test, predictions)
	print '\n'

#random forest predicition accuracy
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

	from sklearn.ensemble import RandomForestClassifier
#n_jobs parameter parallelizes training of random forest
	my_classifier = RandomForestClassifier(n_jobs=3, verbose=3)
	my_classifier.fit(X_train, y_train)
	predictions = my_classifier.predict(X_test)
	print 'random forest classification predictions'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'random forest prediction accuracy score'
	print accuracy_score(y_test, predictions)