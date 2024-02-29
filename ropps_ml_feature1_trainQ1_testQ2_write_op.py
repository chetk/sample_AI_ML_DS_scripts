#Author: Chet K ckumar12@gmail.com
#Recommended Opportunities ML framework first feature train_q117 test_q217 write o/p
#To do: PEP 8 format, descriptive comments, g3 compatible
#y = 'is_accepted2'
#x = 'accepted_same_gt_product_previous_Q'
#lcs_us_eng_chi_01_edu_q117_q217_data_previous_Q train_test_split = 0.5 + train_q117 test_q217
#ML algorithms tested: decision tree, logistic regression, random forest

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats
from pylab import *
import sys
import pydot

from numpy import array
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals.six import StringIO  

if __name__ == "__main__":
#chi_01_edu_q117_q217
	chi_01_edu_q117_q217 = pd.read_csv('/Users/kumarchetan/Documents/workcode/ropps/data/lcs_us_eng_chi_01_edu_q117_q217_data_previous_Q.csv')
	print 'chi_01_edu_q117_q217'
#dictionary for creating categorical variables features
	d = {'Adopt': 0, 'Expand': 1, 'Optimize': 2}
	chi_01_edu_q117_q217['intent'] = chi_01_edu_q117_q217['intent'].map(d)
	d = {'Global Performance': 0, 'Global Brand': 1, 'Custom Lead List': 2}
	chi_01_edu_q117_q217['product_segment'] = chi_01_edu_q117_q217['product_segment'].map(d)
	chi_01_edu_q117_q217_only_q117 = chi_01_edu_q117_q217[chi_01_edu_q117_q217['current_Q'] == 'q117']
	print 'chi_01_edu_q117_q217_only_q117'
	print chi_01_edu_q117_q217_only_q117.head()
	chi_01_edu_q117_q217_only_q217 = chi_01_edu_q117_q217[chi_01_edu_q117_q217['current_Q'] == 'q217']
	print 'chi_01_edu_q117_q217_only_q217'
	print chi_01_edu_q117_q217_only_q217.head()

#OLS regression chi_01_edu_q117_q217_only_q117 accepted vs accepted_same_gt_product_previous_Q
	X = chi_01_edu_q117_q217_only_q117[['accepted_same_gt_product_previous_Q']]
	y = chi_01_edu_q117_q217_only_q117[['is_accepted2']]
#not adding a constant setting intercept = 0
	est = sm.OLS(y, X).fit()
	print "OLS regression chi_01_edu_q117_q217_only_q117 accepted vs accepted_same_gt_product_previous_Q"
	print est.summary()
	print 'r squared: ', est.rsquared
	print 'p value: ', est.pvalues
	print 'params: ', est.params
	print 'params[0]: ', est.params[0]
	print '\n'

#decision tree chi_01_edu_q117_q217_only_q117 predicting accept vs accepted_same_gt_product_previous_Q
	features = list(chi_01_edu_q117_q217_only_q117[['accepted_same_gt_product_previous_Q']])
	print 'decision tree chi_01_edu_q117_q217_only_q117 predicting accept vs accepted_same_gt_product_previous_Q'
	print 'features for predicting accept'
	print features
	print '\n'

	y = chi_01_edu_q117_q217_only_q117['is_accepted2']
	X = chi_01_edu_q117_q217_only_q117[features]
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X,y)

#Predict accept classification of | accepted_same_gt_product_previous_Q = 1
	print 'Predict using Decision Tree classifier accept classification of | accepted_same_gt_product_previous_Q = 1 | predict accept = ', clf.predict([[1]])
#...and | intent = 0 adopt | present_impact_surfaced = 1 | accepted_same_gt_product_previous_Q = 0
	print 'Predict using Decision Tree classifier accept classification of | accepted_same_gt_product_previous_Q = 0 | predict accept = ', clf.predict([[0]])
	print 'try live [0] = ', clf.predict([[0]])
	print '\n'

#decision tree visualization
	from sklearn.externals.six import StringIO
	import pydot
	dot_data = StringIO()
	tree.export_graphviz(clf, out_file=dot_data, feature_names=features)
	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	graph.write_pdf("chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q_decision_tree_2.pdf")

#decision tree predicition accuracy chi_01_edu_q117_q217_only_q117 
#replaced sklearn.model_selection instead of sklearn.cross_validation no more deprecation warning
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

	from sklearn import tree
	my_classifier = tree.DecisionTreeClassifier()
	my_classifier.fit(X_train, y_train)
	predictions = my_classifier.predict(X_test)
	print 'decision tree classification predictions chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'decision tree prediction accuracy score chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print accuracy_score(y_test, predictions)
	print '\n'

#logistic regression predicition accuracy chi_01_edu_q117_q217_only_q117
	from sklearn.model_selection import train_test_split
	from sklearn.linear_model import LogisticRegression
	my_classifier = LogisticRegression()
	my_classifier.fit(X_train, y_train)
	print 'logistic regression model chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print(my_classifier)
	print 'logistic regression coefficients chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print my_classifier.coef_
	print 'logistic regression intercept chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print my_classifier.intercept_
	predictions = my_classifier.predict(X_test)
	print 'logisitic regression classification predictions chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'logisitic regression prediction accuracy score chi_01_edu_q117_q217_only_q117_only_accepted_same_gt_product_previous_Q'
	print accuracy_score(y_test, predictions)
	print '\n'

#OLS regression chi_01_edu_q117_q217_only_q217 accepted vs accepted_same_gt_product_previous_Q
	X = chi_01_edu_q117_q217_only_q217[['accepted_same_gt_product_previous_Q']]
	y = chi_01_edu_q117_q217_only_q217[['is_accepted2']]
#not adding a constant setting intercept = 0
	est = sm.OLS(y, X).fit()
	print "OLS regression chi_01_edu_q117_q217_only_q217 accepted vs accepted_same_gt_product_previous_Q"
	print est.summary()
	print 'r squared: ', est.rsquared
	print 'p value: ', est.pvalues
	print 'params: ', est.params
	print 'params[0]: ', est.params[0]
	print '\n'

#decision tree chi_01_edu_q117_q217_only_q217 predicting accept vs intent + present_impact_surfaced + accepted_same_gt_product_previous_Q
	features = list(chi_01_edu_q117_q217_only_q217[['accepted_same_gt_product_previous_Q']])
	print 'decision tree chi_01_edu_q117_q217_only_q217 predicting accept vs accepted_same_gt_product_previous_Q'
	print 'features for predicting accept'
	print features
	print '\n'

	y = chi_01_edu_q117_q217_only_q217['is_accepted2']
	X = chi_01_edu_q117_q217_only_q217[features]
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X,y)

#Predict accept classification of | accepted_same_gt_product_previous_Q = 1
	print 'Predict using Decision Tree classifier accept classification of | accepted_same_gt_product_previous_Q = 1 | predict accept = ', clf.predict([[1]])
#...and | intent = 0 adopt | present_impact_surfaced = 1 | accepted_same_gt_product_previous_Q = 0
	print 'Predict using Decision Tree classifier accept classification of | accepted_same_gt_product_previous_Q = 0 | predict accept = ', clf.predict([[0]])
	print 'try live [0] = ', clf.predict([[0]])
	print '\n'

#decision tree visualization
	from sklearn.externals.six import StringIO
	import pydot
	dot_data = StringIO()
	tree.export_graphviz(clf, out_file=dot_data, feature_names=features)
	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	graph.write_pdf("chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q_decision_tree_2.pdf")

#decision tree predicition accuracy chi_01_edu_q117_q217_only_q217
#replaced sklearn.model_selection instead of sklearn.cross_validation no more deprecation warning
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

	from sklearn import tree
	my_classifier = tree.DecisionTreeClassifier()
	my_classifier.fit(X_train, y_train)
	predictions = my_classifier.predict(X_test)
	print 'decision tree classification predictions chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'decision tree prediction accuracy score chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print accuracy_score(y_test, predictions)
	print '\n'

#logistic regression predicition accuracy chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q
	from sklearn.model_selection import train_test_split
	from sklearn.linear_model import LogisticRegression
	my_classifier = LogisticRegression()
	my_classifier.fit(X_train, y_train)
	print 'logistic regression model chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print(my_classifier)
	print 'logistic regression coefficients chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print my_classifier.coef_
	print 'logistic regression intercept chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print my_classifier.intercept_
	predictions = my_classifier.predict(X_test)
	print 'logisitic regression classification predictions chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'logisitic regression prediction accuracy score chi_01_edu_q117_q217_only_q217_only_accepted_same_gt_product_previous_Q'
	print accuracy_score(y_test, predictions)
	print '\n'

#decision tree predicition accuracy train_q117 test_q217
#replaced sklearn.model_selection instead of sklearn.cross_validation no more deprecation warning
	from sklearn.model_selection import train_test_split

	features = list(chi_01_edu_q117_q217[['accepted_same_gt_product_previous_Q']])
	X_train = chi_01_edu_q117_q217_only_q117[features]
	X_test =  chi_01_edu_q117_q217_only_q217[features]
	y_train = chi_01_edu_q117_q217_only_q117['is_accepted2']
	y_test = chi_01_edu_q117_q217_only_q217['is_accepted2']

	from sklearn import tree
	my_classifier = tree.DecisionTreeClassifier()
	my_classifier.fit(X_train, y_train)
	predictions = my_classifier.predict(X_test)
	print 'decision tree classification predictions only_accepted_same_gt_product_previous_Q train_q117 test_q217'
	print predictions

#write predictions output
	print ('Hire prediction looping over output:')
	for result in predictions:
	    print result

#next step write result output to a csv file

#create new predictions column in chi_01_edu_q117_q217_only_q217 dataframe
	chi_01_edu_q117_q217_only_q217['predictions_q217_train_q117'] = predictions
	print 'chi_01_edu_q117_q217_only_q217 with predictions column'
	print chi_01_edu_q117_q217_only_q217.head()
	print '\n'

#write dataframe predictions output to a csv file
#after dropping first column which has row index numbers not needed in final output
	chi_01_edu_q117_q217_only_q217.to_csv('predictions_q217_train_q117_op_chi_01_edu_no_index_column_only_accepted_same_gt_previous_Q.csv', mode = 'w', index = False)
	print 'predictions_q217_train_q117_op_chi_01_edu_no_index_column_only_accepted_same_gt_previous_Q.csv output file with predictions column and no index column'
	print '\n'

#write chi_01_edu_q117_q217_only_q217 dataframe output to a csv file
#in this version index column is retained in output
	chi_01_edu_q117_q217_only_q217.to_csv('predictions_q217_train_q117_op_chi_01_edu_only_accepted_same_gt_previous_Q.csv')

	from sklearn.metrics import accuracy_score
	print 'decision tree prediction accuracy score only_accepted_same_gt_product_previous_Q train_q117 test_q217'
	print accuracy_score(y_test, predictions)
	print '\n'

#logistic regression predicition accuracy
	from sklearn.model_selection import train_test_split

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
	print 'logisitic regression classification predictions only_accepted_same_gt_product_previous_Q train_q117 test_q217'
	print predictions

	from sklearn.metrics import accuracy_score
	print 'logisitic regression prediction accuracy score only_accepted_same_gt_product_previous_Q train_q117 test_q217'
	print accuracy_score(y_test, predictions)
