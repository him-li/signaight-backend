from core.clients.service_logs import api as service_logs_api
from core.logging import logger
from core.utils import parse_urn


def post_service_log(search_id,
                     urn,
                     executor,
                     search_step,
                     message,
                     step_point,
                     docs_count=None,
                     step_duration_microseconds=None):
    service_log_body = {
        "meta": {
            "search_id": search_id,
            "person_id": parse_urn(urn),
            "executor": executor,
            "search_step": search_step,
            "message": f"{message} with {docs_count} docs",
            "docs_count": docs_count,
            "step_point": step_point,
            "step_duration_microseconds": step_duration_microseconds
        }
    }
    try:
        service_logs_api.service_logs_request.post(
            body=service_log_body)
    except Exception as e:
        logger.error(f"Unable to send service log: {str(e)}")
