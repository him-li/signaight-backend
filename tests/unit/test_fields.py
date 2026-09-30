import pytest
import json

from fastapi.encoders import ENCODERS_BY_TYPE, jsonable_encoder
from core.fields import S3Path
from tests.unit.common import (
    PhotoDoc,
    HybridStorage,
    PictureParentDoc,
)

#ENCODERS_BY_TYPE.update({S3Path: str})

@pytest.mark.anyio
async def test_document_picture():
    obj = HybridStorage(photo='https://i.pravatar.cc/150?img=19')
    await obj.insert()
    assert 's3://' in str(obj.photo)
    pic_http_url = obj.photo.as_url()
    assert ('http://' in pic_http_url or 'https://' in pic_http_url)
    photo_doc = PhotoDoc(**obj.model_dump())
    data_json = photo_doc.json() # noqa


@pytest.mark.anyio
async def test_document_picture_with_expired_signature():
    obj = HybridStorage(photo=('https://i.pravatar.cc/150?img=19'))
    await obj.insert()
    assert obj.photo

    obj = HybridStorage(photo=('https://scontent.fcwc1-1.fna.fbcdn.net/v/t39.30808-6/'
        '448340099_10232708818443583_294523822125877328_n.jpg'
        '?_nc_cat=103&ccb=1-7&_nc_sid=5f2048&_nc_ohc=mn2_sg6Au1YQ7kNvgF8k3qu'
        '&_nc_ht=scontent.fcwc1-1.fna'
        '&oh=00_AYDgu8hJeAftuIFNxJbc-KUYB_7rYxO18fjbhV0M4FaKVb&oe=66776122'))
    await obj.insert()
    assert not obj.photo


@pytest.mark.anyio
async def test_nested_document_picture():
    data = {
        "name": "Parent Doc",
        "picture_nested_doc": {
            "alt": "test image",
            "photo": 'https://i.pravatar.cc/150?img=19'
        }
    }
    obj = PictureParentDoc(**data)
    await obj.insert()
    assert 's3://' in str(obj.picture_nested_doc.photo)


@pytest.mark.anyio
async def test_s3path_serialization():
    obj = HybridStorage(photo='https://i.pravatar.cc/150?img=19')
    await obj.insert()

    # Standard dumping to python dict from Pydantic V2 as s3 url
    obj_dumped_as_dict = obj.model_dump()
    assert 's3://' in str(obj_dumped_as_dict.get('photo'))
    assert isinstance(obj_dumped_as_dict.get('photo'), S3Path)

    # Dumping through fastapi encoder as http(s) url
    obj_dumped_as_dict = jsonable_encoder(obj)
    assert ('http://' in obj_dumped_as_dict.get('photo')
            or 'https://' in obj_dumped_as_dict.get('photo'))

    # Standard dumping to json from Pydantic V2 as http(s) url
    obj_dumped_as_json = json.loads(obj.model_dump_json())
    assert ('http://' in obj_dumped_as_json.get('photo')
            or 'https://' in obj_dumped_as_json.get('photo'))
