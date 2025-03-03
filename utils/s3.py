import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

class S3Client:
    def __init__(self):
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.region = os.getenv('AWS_REGION')
        
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region
        )
    
    def upload_file(self, file, filename):
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                f'avatars/{filename}',
            )
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/avatars/{filename}"
            return url
        except ClientError as e:
            print(f"S3 上傳錯誤：{str(e)}")
            return None