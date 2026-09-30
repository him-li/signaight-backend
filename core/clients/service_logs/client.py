from core.rest_client import API

from .resources import ServiceLogsResource, AsyncServiceLogsResource

from core.config import settings

# create api instance
api = API(
    api_root_url=settings.SERVICE_LOGS_BASE_URL,  # base api url
    params={},  # default params
    headers={
        'x-api-key': f"{settings.SERVICE_LOGS_API_KEY}"
    },  # default headers
    timeout=500,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

api.add_resource(resource_name='service_logs_request',
                 resource_class=ServiceLogsResource)
api.add_resource(resource_name='async_service_logs_request',
                 resource_class=AsyncServiceLogsResource)
