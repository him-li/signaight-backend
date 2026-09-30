# import requests
import json
import httpx


def compute_face_compare(meta_data, url, known_tokens, headers={}):
    """
    main function for face compare

    meta_data = {
        "source": "s3://testing/source/1.jpg",
        "destination": ["s3://testing/dist/1.jpg", "s3://testing/dist/2.jpg"]
    }

    url = "http://127.0.0.1:8000/face/compare_batch"
    """
    try:
        payload = {}

        files = [
            ('file', (
                'test_s3_.json',
                json.dumps(meta_data),
                'application/json'))
        ]

        headers["Authorization"] = f'Bearer {known_tokens}'
        print("Computing face compare.............")

        # response = requests.request("POST", url, headers=headers, data=payload, files=files) # noqa
        timeout = httpx.Timeout(500.0, read=450.0)
        client = httpx.Client(timeout=timeout)
        response = client.post(
            url,
            headers=headers,
            data=payload,
            files=files
        )

        print("Computing face compare finished.............")

        return response.json()
    except Exception as e:
        print(f"Error computing face compare....... {str(e)}")

# TODO: for some reason executor does not work with async version of function
async def async_compute_face_compare(meta_data, url, known_tokens, headers={}):
    try:
        payload = {}

        files = [
            ('file', (
                'test_s3_.json',
                json.dumps(meta_data),
                'application/json'))
        ]

        headers["Authorization"] = f'Bearer {known_tokens}'
        print("Computing face compare.............")

        timeout = httpx.Timeout(180.0, read=120.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                headers=headers,
                data=payload,
                files=files
            )
        print("Computing face compare finished.............")

        return response.json()
    except Exception as e:
        print(f"Error computing face compare....... {str(e)}")
