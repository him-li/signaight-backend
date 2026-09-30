import os
import botocore
import mimetypes
from boto3.session import Session
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from cloudpathlib import S3Client as OriginalS3Client
from cloudpathlib.enums import FileCacheMode
from cloudpathlib.client import register_client_class
from typing import Callable, Optional, Union

from core.logging import logger

from .config import settings


@register_client_class("s3")
class S3Client(OriginalS3Client):
    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        no_sign_request: Optional[bool] = False,
        botocore_session: Optional["botocore.session.Session"] = None,
        profile_name: Optional[str] = None,
        boto3_session: Optional["Session"] = None,
        file_cache_mode: Optional[Union[str, FileCacheMode]] = None,
        local_cache_dir: Optional[Union[str, os.PathLike]] = None,
        endpoint_url: Optional[str] = None,
        boto3_transfer_config: Optional["TransferConfig"] = None,
        content_type_method: Optional[Callable] = mimetypes.guess_type,
        extra_args: Optional[dict] = None,
    ):
        """
        Constructs S3 Client with checking of bucket presence.
        Create bucket if not exists
        """
        super().__init__(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            no_sign_request=no_sign_request,
            botocore_session=botocore_session,
            profile_name=profile_name,
            boto3_session=boto3_session,
            file_cache_mode=file_cache_mode,
            local_cache_dir=local_cache_dir,
            endpoint_url=endpoint_url,
            boto3_transfer_config=boto3_transfer_config,
            content_type_method=content_type_method,
            extra_args=extra_args,
        )

        # override sign method for Amazon buckets when endpoint_url is empty
        if not endpoint_url and settings.AWS_ENDPOINT_URL:
            endpoint_url = str(settings.AWS_ENDPOINT_URL)
        if not endpoint_url:
            self.s3 = self.sess.resource(
                "s3",
                region_name=settings.AWS_S3_REGION_NAME,
                config=Config(signature_version='s3v4'),
            )
            self.client = self.sess.client(
                "s3",
                region_name=settings.AWS_S3_REGION_NAME,
                config=Config(signature_version='s3v4'),
            )

        self.bucket = (extra_args.get('bucket', settings.AWS_S3_BUCKET)
                       if extra_args and isinstance(extra_args, dict)
                       else settings.AWS_S3_BUCKET)
        try:
            self.client.create_bucket(Bucket=self.bucket)
        except Exception as e:
            logger.info(e)
            # TODO: maybe try to detect exception when unable to create bucket
            pass


def init_storage(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    default=True
) -> S3Client:
    '''Initialize default storage. If there is no provided credentials
        try to get one from environment

    Parameters
    ----------
    endpoint_url : str
        S3 object storgae endpoint url
    aws_access_key_id : str
        Access key ID for storage
    aws_secret_access_key : str
        Access key Secret for storage

    Returns
    -------
    None
    '''
    params = {
        'aws_access_key_id': (aws_access_key_id if aws_access_key_id
                                else settings.AWS_ACCESS_KEY_ID),
        'aws_secret_access_key': (aws_secret_access_key if aws_secret_access_key
                                else settings.AWS_SECRET_ACCESS_KEY),
        'extra_args': {
            'bucket': settings.AWS_S3_BUCKET,
        },
        'boto3_transfer_config': TransferConfig(
            max_concurrency=30,
            use_threads=True
        )
    }
    if endpoint_url:
        params['endpoint_url'] = endpoint_url

    client = S3Client(**params)
    if default:
        client.set_as_default_client()

    return client
