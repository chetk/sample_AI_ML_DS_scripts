#Author: Chetan Kumar ckumaronline@gmail.com
#Automating Jobs Taxonomy query generation for All Jobs categories
#Utilizing job_title, job_brief_description, job_parsed_criteria_skills columns for Amazon ML training dataset 
#Executing generated query in Redshift and storing query output
#Parameterizing files for storing query and Redshift output
#Importing Redshift connection string and updated queries data file from taxonomy_properites
#$ python taxonomy_classification_ml_training.py [store-redshift-query-output-file.csv] 

import xml.etree.ElementTree as ET
import httplib2
import psycopg2
import csv
import sys
import taxonomy_properties

#Execute a SQL query in Redshift 
def execute_query(conn,sql):
	try:
		cur = conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		return rows
	except Exception, e:
		print "Unable to connect to database:" + str(e)

#Write line to a csv txt file
def write_line_to_txtfile(line,file):
 	file.write(line)
	file.write("\n")

#Write query Redshift output to a csv txt file
def write_query_output_to_txtfile(title,file):
    query_result = execute_query(conn,title)
    for result in query_result:
        line = str(result[0]) + ", " + str(result[1]) + ", " + str(result[2]).replace(',',' ').replace('None','') + ", " + str(result[3]).replace(',',' ').replace('None','') + ", " + str(result[4]) + ", " + str(result[5]).replace(',',' ').replace('None','')
        write_line_to_txtfile(line,file)

if __name__ == "__main__":
#Redshift connection
	redshift_connect = "dbname=%s user=%s host=%s port=%s password=%s" % (taxonomy_properties.dbname, taxonomy_properties.user, taxonomy_properties.host, taxonomy_properties.port, taxonomy_properties.password)
	conn=psycopg2.connect(redshift_connect)
#For write Redshift query output to a csv file
	f_redshift_output = open(sys.argv[1],'ab')
#Write Redshift query ouput file header line
	header_line = "job_id" + ", " + "company_id" + ", " + "job_title" + ", " + "job_brief_description" + ", " + "standard_job_taxonomy" + ", " + "job_parsed_criteria_skills"
	write_line_to_txtfile(header_line,f_redshift_output)
#Execute updated queries stored in a data file and write query output to the csv file
	with open(taxonomy_properties.data_file_30more_jobtitle_briefdescription_parsedskills_query) as f:
		for line in f:
			print line
			title = line
			write_query_output_to_txtfile(title,f_redshift_output)
	f_redshift_output.close()
