#Author: Chet K ckumar12@gmail.com
#!/bin/sh
#Automating Taxonomy daily batch prediction
#Utilizing Amazon ML CLI
#$ chmod u+x aws_ml_cli_script_batch.sh
#$ ./aws_ml_cli_script_batch.sh
#$ bash aws_ml_cli_script_batch.sh

export taxonomy_properties
export VAR1="date +\"%m-%d-%Y-%H-%M\""
export DATE=`eval $VAR1`
export dataPath=~/Documents/pa/pycode/
export s3bucketPath=s3://********/chet_jobs_taxonomy

source $dataPath/batch_taxonomy.properties

#Python script for taxonomy batch prediction query generation
BATCH_PREDICTION_INPUT_SCRIPT=$taxonomy_batch_computer_math_engg
echo "The taxonomy batch prediction input generation script is $BATCH_PREDICTION_INPUT_SCRIPT"

#Write taxonomy batch prediction Redshift query results output to a csv file
BATCH_PREDICTION_QUERY_RESULT="batch-taxonomy-jobs-$DATE.csv"
echo "The taxonomy batch prediction query results file is $BATCH_PREDICTION_QUERY_RESULT"

#Execute Python script for generating query results output Amazon ML batch prediction data file
python $BATCH_PREDICTION_INPUT_SCRIPT $BATCH_PREDICTION_QUERY_RESULT
sleep 30

#Upload the Amazon ML batch prediction data file to S3
aws s3 cp $BATCH_PREDICTION_QUERY_RESULT $s3bucketPath/
sleep 30

#Create data source from the file in S3
aws machinelearning create-data-source-from-s3 --region us-east-1 --data-source-id ds-taxonomy-$DATE --data-source-name ***********_taxonomy_pred_ds_$DATE --data-spec DataLocationS3=$s3bucketPath/$BATCH_PREDICTION_QUERY_RESULT,DataSchemaLocationS3=$s3bucketPath/batch_taxonomy_schema.csv.schema --no-compute-statistics
sleep 30

#Make batch prediction and wait until it is done
aws machinelearning create-batch-prediction --region us-east-1 --batch-prediction-id bp-taxonomy-$DATE --batch-prediction-name jobvite_taxonomy_pred_batch_$DATE --ml-model-id ************** --batch-prediction-data-source-id ds-taxonomy-$DATE --output-uri $s3bucketPath/

VAR2=`aws machinelearning get-batch-prediction --batch-prediction-id bp-taxonomy-$DATE | grep Status`
i=0
while [[ ( "${VAR2}" !=  *"COMPLETED"* ) && ( $i -lt 10 ) ]]; do
    i=$((i+1))
    sleep 60
    VAR2=`aws machinelearning get-batch-prediction --batch-prediction-id bp-taxonomy-$DATE | grep Status`
done

#Download the batch prediction output; parse the best cateogry; merge the best-cat with JobID
aws s3 cp $s3bucketPath/*******************/bp-taxonomy-$DATE-$BATCH_PREDICTION_QUERY_RESULT.gz $dataPath/bp-taxonomy-$DATE-$BATCH_PREDICTION_QUERY_RESULT.gz
gunzip $dataPath/bp-taxonomy-$DATE-$BATCH_PREDICTION_QUERY_RESULT.gz

python find_best_taxonomy.py -i $dataPath/bp-taxonomy-$DATE-$BATCH_PREDICTION_QUERY_RESULT -o $dataPath/best_taxonomy.txt
python merge_jobid_and_pred_taxonomy.py $BATCH_PREDICTION_QUERY_RESULT

aws s3 cp $dataPath/id_to_taxonomy.txt $s3bucketPath/taxonomy_full_prediction.txt

psql $redshiftConnection -c "drop table if exists stage_job_ml_pred_taxonomy"
psql $redshiftConnection -c "create table stage_job_ml_pred_taxonomy (like job_id_to_job_taxonomy)"
psql $redshiftConnection -c "delete from stage_job_ml_pred_taxonomy"
psql $redshiftConnection -c "copy stage_job_ml_pred_taxonomy from '$s3bucketPath/taxonomy_full_prediction.txt' credentials 'aws_access_key_id=$awsAccessKey;aws_secret_access_key=$awsSecretKey' CSV  delimiter ','"

psql $redshiftConnection -c "update stage_job_ml_pred_taxonomy set job_taxonomy_modified_time=getdate()"

#Insert the new predictions into the main table
psql $redshiftConnection -c "delete from job_id_to_job_taxonomy using stage_job_ml_pred_taxonomy where job_id_to_job_taxonomy.job_id=stage_job_ml_pred_taxonomy.job_id"
psql $redshiftConnection -c "insert into job_id_to_job_taxonomy select job_id,company_id,standard_job_taxonomy,job_taxonomy_modified_time from stage_job_ml_pred_taxonomy"
