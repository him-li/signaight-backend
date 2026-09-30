import mimetypes
import requests
import uuid
import time
from typing import Union
from pydantic import AnyHttpUrl

from core.logging import logger

from .fields import S3Path
from .storage import S3Client

'''
def profile_photos_to_storage(path: str) -> Union[S3Path, AnyHttpUrl]:
    client = S3Client.get_default_client()
    creds = client.sess.get_credentials()
    # TODO: rework this check for argument type
    if (isinstance(path, str) and ('http' in path or 'https' in path)
            and (creds.access_key and creds.secret_key)):
        try:
            tryouts = 0
            while True:
                if tryouts == 4:
                    return None
                resp = requests.get(path, stream=True)
                file_ext = mimetypes.guess_extension(
                    resp.headers.get('Content-Type'), strict=True)
                if file_ext == ".txt":
                    logger.error(f"Remote cdn bad response with txt. Retry... {resp.reason}")
                    time.sleep(1)
                    tryouts += 1
                    continue
                else:
                    file_key = str(uuid.uuid4())
                    file_path = "profile_photos/{}/{}/{}/{}{}".format(
                        file_key[0:1],
                        file_key[1:3],
                        file_key[3:8],
                        file_key,
                        file_ext)
                    s3p = S3Path(f"s3://{client.bucket}/{file_path}")
                    s3p.write_bytes(resp.raw.read())
                    path = s3p
                    break
        except Exception as e:
            logger.error(f"S3 image save error: {str(e)}")
            print(f"S3 image save error: {str(e)}")
    return path
'''

def profile_photos_to_storage(path: str) -> Union[S3Path, AnyHttpUrl]:
    client = S3Client.get_default_client()
    creds = client.sess.get_credentials()
    # TODO: rework this check for argument type
    if (isinstance(path, str) and ('http' in path or 'https' in path)
            and (creds.access_key and creds.secret_key)):
        try:
            resp = requests.get(path, stream=True)
            file_ext = mimetypes.guess_extension(
                resp.headers.get('Content-Type'), strict=True)
            file_key = str(uuid.uuid4())
            file_path = "profile_photos/{}/{}/{}/{}{}".format(
                file_key[0:1],
                file_key[1:3],
                file_key[3:8],
                file_key,
                file_ext)
            s3p = S3Path(f"s3://{client.bucket}/{file_path}")
            s3p.write_bytes(resp.raw.read())
            path = s3p
        except Exception as e:
            logger.info(e)
            print(str(e))
    return path
