import boto3
import os

s3_client = boto3.client('s3')

# Make sure to use raw string for the local directory!
local_directory = r'fullPath\To\local\directory'
bucket_name = 'S3_bucket_name'


def download_Bucket(bucket_name, local_directory):

    list_myBucket = s3_client.list_objects_v2(
        Bucket=bucket_name
    )

    bucket_content_list = list_myBucket.get('Contents')

    for item in bucket_content_list:

        # split dirname et basename
        x = os.path.split(item.get('Key'))

        # if item is only  i.e. file, copy to root dest dination
        if x[0] == '':
            destpath = os.path.join(local_directory, x[1])
            s3_client.download_file(bucket_name, x[1], destpath)

        # if item is dirname and basename
        #   1- check if dirname exist. If not, create.
        #   2- copy basename to dirname location using the boto s3_client

        if x[0] != '':

            # destpath = local_directory + dirname
            destpath = os.path.join(local_directory, x[0])

            # Create destpath is not existent
            if os.path.exists(destpath) == False:
                os.makedirs(destpath)

            if x[1]:
                # Create fullPath for basename to use with boto3 download_file
                fullPath = os.path.join(local_directory, x[0], x[1])
                s3_client.download_file(bucket_name, item['Key'], fullPath)


# Execute the function to pull entire S3 bucket mimicing the folder structure
download_Bucket(bucket_name, local_directory)
