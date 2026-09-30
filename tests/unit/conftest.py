import pytest

from core.storage import S3Client


@pytest.fixture()
def storage(settings):
    client = S3Client(
        endpoint_url=str(settings.AWS_ENDPOINT_URL),
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        extra_args={
            'bucket': settings.AWS_S3_BUCKET
        }
    )
    client.set_as_default_client()
    return client
