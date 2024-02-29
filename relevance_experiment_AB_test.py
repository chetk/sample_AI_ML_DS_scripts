#Author: Chet K ckumar12@gmail.com
#Relevance Experiment
#Moods Median Test Median Accept Rate 
#Two Sample Mean t Test Mean Accept Rate
#Aggregate Accept Rate 
#Test, Control, New Control divisions + pods

import pandas as pd
import numpy as np
import scipy as sp
from scipy.stats import median_test
from scipy.stats import ttest_ind

if __name__ == "__main__":
#numerical example of Moods median test
#Moods median test scipy module:https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_test.html
    g1 = [10, 11, 15, 16, 12, 11, 16, 17, 14, 15, 12, 13, 16, 11, 11, 13, 14, 11, 12, 19, 13, 16]
    g2 = [50, 51, 54, 52, 58, 56, 51, 52, 55, 56, 59, 56, 55, 52, 59, 53, 55, 54, 57, 58]

    stat, p, med, tbl = median_test(g1, g2)

    print "median sample g1 = ", np.median(g1)
    print "sample size g1 = ", len(g1)
    print "median sample g2 = ", np.median(g2)
    print "sample size g2 = ", len(g2)
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference g1 g2 = ", p
    print "\n"

#numerical example of two sample t test
#t test scipy module: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
#one tail t test p value: https://stackoverflow.com/questions/15984221/how-to-perform-two-sample-one-tailed-t-test-with-numpy-scipy    
    print "t test g1 g2"
    print sp.stats.ttest_ind(g1, g2, equal_var=False)
    sp_ttest = sp.stats.ttest_ind(g1, g2, equal_var=False) 
    print 't test statistic = ', sp_ttest[0]
    print 'p value t test one tail = ', sp_ttest[1]/2      
    print "\n"
    
#relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017
    relevance_exp_2017q3_breakdown = pd.read_csv('/Users/kumarchetan/Documents/workcode/ropps/data/relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017.csv')
    print "relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017"
    print "\n"

    relevance_exp_2017q3_breakdown_test = relevance_exp_2017q3_breakdown[relevance_exp_2017q3_breakdown['test_control_group_flag'] == 'test']
    print "relevance_exp_2017q3_breakdown_test"
    print "\n"

    relevance_exp_2017q3_breakdown_control = relevance_exp_2017q3_breakdown[relevance_exp_2017q3_breakdown['test_control_group_flag'] == 'control']
    print "relevance_exp_2017q3_breakdown_control"
    print "\n"

    relevance_exp_2017q3_breakdown_new_control = relevance_exp_2017q3_breakdown[relevance_exp_2017q3_breakdown['test_control_group_flag'] == 'new control']
    print "relevance_exp_2017q3_breakdown_new_control"
    print "\n"

#Moods median test relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017
    print "Moods median test relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017"
    print "\n"
    stat, p, med, tbl = median_test(relevance_exp_2017q3_breakdown_test['accept_rate'], relevance_exp_2017q3_breakdown_new_control['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_test['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_test['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_test['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_new_control['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_new_control['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_new_control['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control['accept_rate'])
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference test vs new control  = ", p
    print "\n"

    relevance_exp_2017q3_breakdown_test_AMS = relevance_exp_2017q3_breakdown_test[relevance_exp_2017q3_breakdown_test['region'] == 'Americas']
    relevance_exp_2017q3_breakdown_new_control_AMS = relevance_exp_2017q3_breakdown_new_control[relevance_exp_2017q3_breakdown_new_control['region'] == 'Americas']

    stat, p, med, tbl = median_test(relevance_exp_2017q3_breakdown_test_AMS['accept_rate'], relevance_exp_2017q3_breakdown_new_control_AMS['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_test_AMS['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_test_AMS['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_test_AMS['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test_AMS['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_new_control_AMS['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_new_control_AMS['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_new_control_AMS['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control_AMS['accept_rate'])
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference test vs new control AMS = ", p
    print "\n"

    relevance_exp_2017q3_breakdown_test_EMEA = relevance_exp_2017q3_breakdown_test[relevance_exp_2017q3_breakdown_test['region'] == 'EMEA']
    relevance_exp_2017q3_breakdown_new_control_EMEA = relevance_exp_2017q3_breakdown_new_control[relevance_exp_2017q3_breakdown_new_control['region'] == 'EMEA']

    stat, p, med, tbl = median_test(relevance_exp_2017q3_breakdown_test_EMEA['accept_rate'], relevance_exp_2017q3_breakdown_new_control_EMEA['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_test_EMEA['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_test_EMEA['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_test_EMEA['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test_EMEA['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_new_control_EMEA['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_new_control_EMEA['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_new_control_EMEA['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control_EMEA['accept_rate'])
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference test vs new control EMEA = ", p
    print "\n"

    relevance_exp_2017q3_breakdown_test_APAC = relevance_exp_2017q3_breakdown_test[relevance_exp_2017q3_breakdown_test['region'] == 'APAC']
    relevance_exp_2017q3_breakdown_new_control_APAC = relevance_exp_2017q3_breakdown_new_control[relevance_exp_2017q3_breakdown_new_control['region'] == 'APAC']

    stat, p, med, tbl = median_test(relevance_exp_2017q3_breakdown_test_APAC['accept_rate'], relevance_exp_2017q3_breakdown_new_control_APAC['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_test_APAC['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_test_APAC['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_test_APAC['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test_APAC['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_new_control_APAC['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_new_control_APAC['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_new_control_APAC['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control_APAC['accept_rate'])
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference test vs new control APAC = ", p
    print "\n"

    relevance_exp_2017q3_breakdown_test_AMS_US = relevance_exp_2017q3_breakdown_test_AMS[relevance_exp_2017q3_breakdown_test_AMS['country'] == 'United States']
    relevance_exp_2017q3_breakdown_new_control_AMS_US = relevance_exp_2017q3_breakdown_new_control_AMS[relevance_exp_2017q3_breakdown_new_control_AMS['country'] == 'United States']

    stat, p, med, tbl = median_test(relevance_exp_2017q3_breakdown_test_AMS_US['accept_rate'], relevance_exp_2017q3_breakdown_new_control_AMS_US['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_test_AMS_US['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_test_AMS_US['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_test_AMS_US['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test_AMS_US['accept_rate'])
    print "median sample relevance_exp_2017q3_breakdown_new_control_AMS_US['accept_rate'] = ", np.median(relevance_exp_2017q3_breakdown_new_control_AMS_US['accept_rate'])
    print "sample size relevance_exp_2017q3_breakdown_new_control_AMS_US['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control_AMS_US['accept_rate'])
    print "pooled samples median = ", med
    print "contingency table = ", tbl
    print "p value median difference test vs new control AMS US = ", p
    print "\n"

#two sample t test relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017
    print "two sample t test relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017"
    print "\n"  
    print "mean sample relevance_exp_2017q3_breakdown_test['accept_rate'] = ", np.mean(relevance_exp_2017q3_breakdown_test['accept_rate'])
    print "standard deviation sample relevance_exp_2017q3_breakdown_test['accept_rate'] = ", relevance_exp_2017q3_breakdown_test['accept_rate'].std()
    print "sample size relevance_exp_2017q3_breakdown_test['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_test['accept_rate'])
    print "mean sample relevance_exp_2017q3_breakdown_new_control['accept_rate'] = ", np.mean(relevance_exp_2017q3_breakdown_new_control['accept_rate'])
    print "standard deviation sample relevance_exp_2017q3_breakdown_new_control['accept_rate'] = ", relevance_exp_2017q3_breakdown_new_control['accept_rate'].std()
    print "sample size relevance_exp_2017q3_breakdown_new_control['accept_rate'] = ", len(relevance_exp_2017q3_breakdown_new_control['accept_rate'])   
    print sp.stats.ttest_ind(relevance_exp_2017q3_breakdown_test['accept_rate'], relevance_exp_2017q3_breakdown_new_control['accept_rate'], equal_var=False)
    sp_ttest = sp.stats.ttest_ind(relevance_exp_2017q3_breakdown_test['accept_rate'], relevance_exp_2017q3_breakdown_new_control['accept_rate'], equal_var=False)
    print 't test statistic = ', sp_ttest[0]
    print 'p value t test one tail = ', sp_ttest[1]/2      
    print "\n"
    
#aggregate accept rate relevance_exp_q317_test_control_new_control_07142017_accept_dismiss_breakdown_filter_below9_cn_10032017
    aggregate_accept_rate_test = relevance_exp_2017q3_breakdown_test['accept_count'].sum()*100.00/relevance_exp_2017q3_breakdown_test['review_count'].sum() 
    print "aggregate_accept_rate sample relevance_exp_2017q3_breakdown_test = ", aggregate_accept_rate_test
    aggregate_accept_rate_new_control = relevance_exp_2017q3_breakdown_new_control['accept_count'].sum()*100.00/relevance_exp_2017q3_breakdown_new_control['review_count'].sum() 
    print "aggregate_accept_rate sample relevance_exp_2017q3_breakdown_new_control = ", aggregate_accept_rate_new_control
