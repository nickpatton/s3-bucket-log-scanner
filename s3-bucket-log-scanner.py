import boto3
import os
from zipfile import ZipFile
import re

s3_resource = boto3.resource('s3', 
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

s3_client = boto3.client('s3', 
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

bucket_name = '<the name of the s3 bucket>'

# Zip files appeared to follow a date/time name convention like 2020-01-07_00-14-26.zip
def get_latest_zip_file(bucket):
    zip_files = []
    for object in bucket.objects.all():
        zip_files.append(object.key)
    zip_files.sort()
    return zip_files[-1]

def unzip_the_zip_file(zip_file_name):
    directory = zip_file_name.strip('.zip')
    with ZipFile(zip_file_name, 'r') as zip:
        zip.extractall(f'{os.getcwd()}/{directory}')

def search_for_log_files(directory):
    log_files = []
    # Unziped directory named something like 2020-01-07_00-14-26...
    for root, dirs, files in os.walk(f'{os.getcwd()}/{directory}'):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    return log_files

def search_log_files_for_errors(log_files):

    # Matching on timestamp
    # Example log line: [2020-01-07 00:15:58,627] crawl.py:L352 DEBUG: Performing XPath Action "exists" on XPath "continue_to_view_verifications"
    regex = re.compile("^(\[[^\]]+?\])")

    for file in log_files:
        print(f"Scanning {file}...\n")
        with open(file) as f:
            for line in f:
                result = regex.search(line)
                # If the log line doesn't match the regex, we assume it's part of a stacktrace and print it
                if result == None:
                    print(line.rstrip())
        print("")

bucket = s3_resource.Bucket(bucket_name)
latest_zip_file = get_latest_zip_file(bucket)

s3_client.download_file(bucket_name, latest_zip_file, f'{os.getcwd()}/{latest_zip_file}')
unzip_the_zip_file(latest_zip_file)

log_files = search_for_log_files(latest_zip_file.strip('.zip'))
search_log_files_for_errors(log_files)