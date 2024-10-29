import boto3
from botocore.exceptions import ClientError
from drf_friend.env import getEnv

# Retrieve environment variables
aws_access_key_id = getEnv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = getEnv('AWS_SECRET_ACCESS_KEY')
aws_region = getEnv('S3_AWS_REGION')
bucket_name = getEnv('S3_BUCKET_NAME')

class S3Storage:
    def __init__(self):
        self.s3_bucket = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

    def put(self, path, contents):
        try:
            self.s3_client.put_object(Body=contents, Bucket=self.s3_bucket, Key=path)
        except ClientError as e:
            print(f"Error putting object to S3: {e}")

    def get(self, path):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            print(f"Error getting object from S3: {e}")

    def delete(self, path):
        try:
            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=path)
        except ClientError as e:
            print(f"Error deleting object from S3: {e}")

    def update(self, path, contents):
        self.delete(path)
        self.put(path, contents)

    def exists(self, path):
        try:
            self.s3_client.head_object(Bucket=self.s3_bucket, Key=path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                print(f"Error checking object existence in S3: {e}")

    def download(self, source_path, destination_path):
        try:
            self.s3_client.download_file(self.s3_bucket, source_path, destination_path)
        except ClientError as e:
            print(f"Error downloading object from S3: {e}")

    def url(self, path):
        try:
            return self.s3_client.generate_presigned_url('get_object', Params={'Bucket': self.s3_bucket, 'Key': path})
        except ClientError as e:
            print(f"Error generating URL for S3 object: {e}")

    def temporary_url(self, path, expiration=3600):
        try:
            return self.s3_client.generate_presigned_url('get_object', Params={'Bucket': self.s3_bucket, 'Key': path}, ExpiresIn=expiration)
        except ClientError as e:
            print(f"Error generating temporary URL for S3 object: {e}")

    def all_files(self, directory):
        try:
            objects = self.s3_client.list_objects(Bucket=self.s3_bucket, Prefix=directory)
            return [obj['Key'] for obj in objects.get('Contents', [])]
        except ClientError as e:
            print(f"Error listing all files in S3 directory: {e}")

    def directories(self, directory):
        try:
            objects = self.s3_client.list_objects(Bucket=self.s3_bucket, Prefix=directory, Delimiter='/')
            return [common_prefix['Prefix'] for common_prefix in objects.get('CommonPrefixes', [])]
        except ClientError as e:
            print(f"Error listing directories in S3 directory: {e}")

    def append(self, path, contents):
        current_contents = self.get(path)
        new_contents = current_contents + contents
        self.update(path, new_contents)

    def prepend(self, path, contents):
        current_contents = self.get(path)
        new_contents = contents + current_contents
        self.update(path, new_contents)

    def copy(self, source, destination):
        self.s3_client.copy_object(Bucket=self.s3_bucket, CopySource=f'/{self.s3_bucket}/{source}', Key=destination)

    def move(self, source, destination):
        self.copy(source, destination)
        self.delete(source)
