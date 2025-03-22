import json
import pg8000.native

import os 
from dotenv import load_dotenv

# Redshift connection setup
def connect_redshift():
    conn = pg8000.native.Connection(
        user = os.getenv("redshift_user"),
        password = os.getenv("redshift_password"),
        host = os.getenv("redshift_host"),
        database = os.getenv("redshift_db"),
        port=5439
    )
    return conn

def s3_to_redshift(conn, iam_role, s3_bucket, s3_key):

    copy_command = f"""
    COPY user_data
    FROM 's3://{s3_bucket}/{s3_key}'
    IAM_ROLE '{iam_role}'
    FORMAT AS PARQUET;
    """

    try:
        print("Executing COPY command...")
        conn.run(copy_command)
        print(f"Data from {s3_key} loaded successfully into Redshift.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
    finally:
        conn.close()

# Lambda handler
def lambda_handler(event, context):
    iam_role = os.getenv("iam_role")
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    print(f"File uploaded: s3://{s3_bucket}/{s3_key}")

    if s3_key.endswith('.parquet'):
        conn = connect_redshift()
        s3_to_redshift(conn, iam_role, s3_bucket, s3_key)
    