import os
import aiohttp
from aiobotocore.session import get_session
from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException, status

load_dotenv()


class FileManager:
    def __init__(self):
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.endpoint_url = os.getenv('ENDPOINT_URL')
        self.region_name = os.getenv('REGION_NAME')

    async def save_file(self, file: UploadFile, filename: str) -> None:
        session = get_session()
        async with session.create_client(
                's3',
                region_name=self.region_name,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
        ) as client:
            try:
                data = await file.read()
                await client.put_object(Bucket=self.bucket_name, Key=filename, Body=data)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not save file')

    async def get_file(self, file_path: str):
        session = get_session()
        async with session.create_client(
                's3',
                region_name=self.region_name,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
        ) as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=file_path)
                async with response['Body'] as stream:
                    data = await stream.read()
                    return data
            except client.exceptions.NoSuchKey as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not get file')

    async def delete_file(self, file_path: str):
        session = get_session()
        async with session.create_client(
                's3',
                region_name=self.region_name,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
        ) as client:
            try:
                await client.delete_object(Bucket=self.bucket_name, Key=file_path)

            except client.exceptions.NoSuchKey as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not get file')


FILE_MANAGER = FileManager()
