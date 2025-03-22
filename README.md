# UserInsight-Streaming-Data-Pipeline
## Overview
&emsp;The UserInsight-Streaming-Data-Pipeline is a real-time data processing pipeline that ingests data from an API into Kafka, processes it using Apache Spark, and stores it in AWS S3. An AWS Lambda function is triggered upon new data arrival in S3, pulling data into AWS Redshift for further analytics and visualization in Looker.key components such as Kafka and Spark can be easily installed and managed using Docker. <br>
!! You can view the dashboard [here. ](https://lookerstudio.google.com/reporting/581cb65a-beb0-45b6-a14c-8f86a316fd18)!! <br>
## Architecture
<img src="readme_pic/UserInsight_Architecture.png" alt="Architecture" width="800">
1. Fetch data from the API and send a message to Kafka. <br>
2. Spark will read data from Kafka and process it. <br>
3. The processed data will be stored in S3 as a data lake. <br>
4. When a new file is saved in S3, it will trigger a Lambda function. <br>
5. The Lambda function will load data from S3 into Redshift. <br>
6. Use data from Redshift to create dashboards in Looker Studio for insights and reporting. <br>

## Dashboard
<img src="readme_pic/UserInsight_Dashboard.png" alt="Dashboard" width="750">
I use Looker Studio to create dashboards using data from the data warehouse.

!! You can view the dashboard [here. ](https://lookerstudio.google.com/reporting/581cb65a-beb0-45b6-a14c-8f86a316fd18)!! <br>
#### A special note
While developing this project, I connected Looker Studio to AWS Redshift for data. However, due to AWS free tier limits, Redshift cannot run continuously. As a result, the dashboard now uses data from a CSV file exported from Redshift, but it appears the same as when directly connected to Redshift.

## Tools & Technologies
- Cloud: Amazon Web Services (AWS) <br>
- Containerization - Docker, Docker Compose <br>
- Stream Processing: Apache Kafka, Apache Spark <br>
- Data Lake: AWS S3 <br>
- Serverless Computing: AWS Lambda <br>
- Data Warehouse: AWS Redshift <br>
- Data Visualization: Looker Studio <br>
- Programming Language: Python <br>

## Set up
1. Check that your Docker has more than 4 GB of RAM. (to use airflow)
```bash
docker run --rm "debian:bookworm-slim" bash -c "numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))"
```
2. clone this github repository
```bash
git clone https://github.com/mikecerton/The-Retail-ELT-Pipeline-End-To-End-project.git
cd The-Retail-ELT-Pipeline-End-To-End-project
```
3. Run mkdir to create directories: logs, plugins, and config.
```bash
mkdir logs, plugins, config
```
4. put you data into .env file like this
```bash
AIRFLOW_UID=50000

bucket_name = your bucket_name
aws_access_key_id = your aws_access_key_id
aws_secret_access_key = your aws_secret_access_key
region_name = your region_name

redshift_host = your redshift_host
redshift_port = your redshift_port
redshift_db = your redshift_db
redshift_user = your redshift_user
redshift_password = your redshift_password
iam_role = your iam_role
```
5. run (airflow-init)
```bash
docker-compose up airflow-init
```
6. run (start docker-compose)
```bash
docker-compose up
```
7. you can start activate dag at http://localhost:8080

## Disclaimer
- airflow : <br>
&emsp;https://github.com/mikecerton/Apache_Airflow_Tutorial <br>
- AWS : <br>
&emsp;https://docs.aws.amazon.com/s3/ <br>
&emsp;https://docs.aws.amazon.com/redshift/ <br>
&emsp;https://www.youtube.com/watch?v=WAjPQZ8Osmg&list=LL&index=14&t=2947s <br>
&emsp;https://www.youtube.com/watch?v=7r2z3Qn3Qz8&list=LL&index=27&t=1672s
- Other : <br>
&emsp;https://www.geeksforgeeks.org/introduction-to-psycopg2-module-in-python/
