import pytest
from pydantic import AnyHttpUrl
from urllib.parse import quote_plus, unquote_plus

from core.utils.url_normalize import url_normalize

@pytest.mark.anyio
async def test_url_query_drop():
    url = url_normalize(
        'https://www.linkedin.com/in/thuba-ncube-234b19180?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app',
        keep_query_params=False
    )
    assert url == 'https://www.linkedin.com/in/thuba-ncube-234b19180'

@pytest.mark.anyio
async def test_url_shorten_url_2_chunks():
    url = url_normalize(
        'https://www.linkedin.com/in/notelodare/details/experience/',
        path_chunks_limit=2
    )
    assert url == 'https://www.linkedin.com/in/notelodare'


@pytest.mark.anyio
async def test_url_without_scheme():
    _url = 'www.linkedin.com/in/büşra-kula-çakmak-71a313a8'

    url = url_normalize(_url)
    assert url == 'https://www.linkedin.com/in/b%C3%BC%C5%9Fra-kula-%C3%A7akmak-71a313a8'

    url = url_normalize(_url, default_scheme='http')
    assert url == 'http://www.linkedin.com/in/b%C3%BC%C5%9Fra-kula-%C3%A7akmak-71a313a8'


@pytest.mark.anyio
async def test_url_dicaritic_symbols_with_field():
    _url = 'https://es.linkedin.com/in/beatriz-francés'
    _url = AnyHttpUrl(_url)
    assert str(_url) == 'https://es.linkedin.com/in/beatriz-franc%C3%A9s'

    url = url_normalize(str(_url))
    assert url == 'https://es.linkedin.com/in/beatriz-franc%C3%A9s'
