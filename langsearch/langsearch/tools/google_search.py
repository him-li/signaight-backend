import asyncio
import hashlib
import httpx
import requests
import os
import random
import sys
import string
import re
from faker import Faker
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

import logging

from langsearch.config import settings
from langsearch.models.google_search_results import GoogleSearchResults


__all__ = ["append_new_info","search_person","tools","SearchInput","extract_body_content"]

fake = Faker(locale="en_US")

# THIS CLIENT IS USED TO GET GOOGLE LINKS

httpx_headers = headers = {
    "x-oxylabs-geo-location": "United States",
    "X-Oxylabs-Render": "html"
}

'''
# custom headers setup
httpx_headers = headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;"
        "q=0.8,application/signed-exchange;v=b3;q=0.9"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "x-oxylabs-geo-location": "United States",
    "x-oxylabs-force-headers": "1",
    "x-oxylabs-force-cookies": "1",
}
'''

async def get_content_async(url: str, semaphore):
    # acquire the semaphore
    async with semaphore:
        response = None
        # use random user-agent if it set in headers var
        if httpx_headers.get('User-Agent'):
            httpx_headers["User-Agent"] = fake.user_agent()
        # use random US state for geolocation
        httpx_headers["x-oxylabs-geo-location"] = ','.join(
            [fake.state(), "United States"])
        # add cookies to randomize requests
        cookies = httpx.Cookies()
        if httpx_headers.get('x-oxylabs-force-cookies'):
            hash_message = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(32))
            cookies.set('csrf_token',
                hashlib.sha256(hash_message.encode()).hexdigest(),
                domain=urlparse(url).hostname)
        # finally lets call url
        print(f"{settings.OXYLABS_PROXY_UNBLOCKER_URL}: {headers}")
        '''
        async with httpx.AsyncClient(
            proxy=str(settings.OXYLABS_PROXY_UNBLOCKER_URL),
            headers=httpx_headers,
            cookies=cookies,
            timeout=httpx.Timeout(120, read=60),
            http2=True, # useful to bypass cloudflare
            follow_redirects=True, # follow redirects
            verify=False, # disable ssl verification
            trust_env=False, # disable automatic env vars consuming
        ) as client:
            try:
                print(f"BEFORE url: {url}\n")
                response = await client.get(url)
            except Exception  as e:
                sys.stderr.write(f"Error occurred: {repr(e)} on {url}\n")
                return {"url":url, "content": None, "exception": repr(e), "status_code": None}
        return {"url": url, "content": response.text, "exception": None, "status_code": response.status_code }
        '''
        async with httpx.AsyncClient(
            proxy=str(settings.OXYLABS_PROXY_UNBLOCKER_URL),
            headers=httpx_headers,
            cookies=cookies,
            timeout=httpx.Timeout(120, read=60),
            http2=True, # useful to bypass cloudflare
            follow_redirects=True, # follow redirects
            verify=False, # disable ssl verification
            trust_env=False, # disable automatic env vars consuming
        ) as client:
            try:
                if url.lower().endswith(".pdf"):
                    return {"url":url, "content": None,
                        "exception": "PDF file - skipping",
                        "status_code": None, "images": []}
                print(f"BEFORE url: {url}\n")
                response = await client.get(url)
                import time
                for i in range(5):
                    response = await client.get(url)
                    if response.status_code != 429:
                        break
                    time.sleep(5 * i)
            except Exception  as e:
                sys.stderr.write(f"Error occurred: {repr(e)} on {url}\n")
                return {"url":url, "content": None, "exception": repr(e),
                    "status_code": None, "images": []}
        image_urls = []
        # max_count = 20
        max_count = 3
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # TODO: images processing should be rworked in async way
            for img in soup.find_all("img"):
                if len(image_urls) >= max_count:
                    break
                src= img.get("src")
                if not src:
                    continue
                if src.startswith("data:image"):
                    continue
                ext = src.split("?")[0].split(".")[-1].lower()
                if ext in ["svg", "ico"]:
                    continue
                if not src.startswith(("http://", "https://")):
                    src = urljoin(url, src)
                try:
                    r = requests.get(src, timeout=5)
                    r.raise_for_status()
                except Exception:
                    continue
                # Open using PIL
                try:
                    img_bytes = BytesIO(r.content)
                    pil_img = Image.open(img_bytes)
                    width, height = pil_img.size
                except Exception:
                    continue
                # Skip too small images
                print('img', src, width, height)
                if width <= 50 or height <= 50:
                    continue

                image_urls.append(src)
        except Exception as e:
            # Capture the parsing error but still return a usable payload
            logger.warning(f"ERROR parsing images for {url}: {e}")
            

        return {
            "url": url,
            "content": extract_body_content(response.text) if response.text else "",
            "exception": None,
            "status_code": response.status_code,
            "images": image_urls,
        }

async def get_urls_html_content_for_graph_tool(urls: list[str])-> dict[str, dict]:
    # prepare semaphore for limiting concurrency
    semaphore = asyncio.Semaphore(10)
    stats_dict= {}
    res_dict={}
    #runs all over all urls asyncronously
    responses = await asyncio.gather(*[
        get_content_async(url, semaphore) for url in urls])
    for i,response in enumerate(responses):
        try:
            res_dict[f"message{i+1}"] = response
            # if response["status_code"]==200:
            #     res_dict[f"message{i+1}"]["parsed_content"] = response# extract_body_content(response)
            # else:
            #     res_dict[f"message{i+1}"]["parsed_content"] = response
        except Exception as e:
            pass
        if status_code := response.get("status_code"):
            if status_code not in stats_dict.keys():
                stats_dict[status_code] = 1
            else:
                stats_dict[status_code] += 1
    print(f"Data extracting stats by response code: {stats_dict}")
    return res_dict

# TODO make this async?
def extract_body_content(response_content: str) -> str:
    """Extract content from body tag only"""
    # soup = BeautifulSoup(response_content, 'html.parser')
    # try:
    #     text = soup.getText()
    #     return text
    # except Exception as e:
    #     return response_content
    soup = BeautifulSoup(response_content, 'html.parser')
    body = soup.find('body')
    if body:
        # Remove script and style elements
        for script in body(["script", "style"]):
            script.decompose()

        # Get text content
        text = body.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()
    else:
        return ""
