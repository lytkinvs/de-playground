import boto3
from botocore.client import Config

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url='http://127.0.0.1:9000/',
        aws_access_key_id='minioadmin',
        aws_secret_access_key='minioadmin',
        config=Config(signature_version="s3v4"),
    )


def list_s3_objects(bucket_name):
    """List objects in the specified S3 bucket."""
    try:
        client = get_s3_client()
        response = client.list_objects(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []

def upload_file_to_s3(file_path, bucket_name, object_name):
    """Upload a file to an S3 bucket."""
    try:
        client = get_s3_client()
        client.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

if __name__ == "__main__":
    bucket = '123'
    # List objects
    print("Objects in bucket:")
    for key in list_s3_objects(bucket):
        print(key)
    # Example upload
    # upload_file_to_s3('localfile.txt', bucket, 'uploadedfile.txt')