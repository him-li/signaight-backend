import json
import requests

from core.config import settings


def notify_slack(resource, action, payload, credits):
    if not settings.SLACK_WEBHOOK_URL:
        return

    text = (
        "*Grayfox API Call Notification*\n"
        f"*Resource:* `{resource}`\n"
        f"*Action:* `{action}`\n"
        "*Payload:*\n```json\n" + json.dumps(payload, indent=2) + "\n```\n"
    )
    if credits:
        text = f"{text}\n*Credits:* `{credits}`\n*Cached:* `False`"
    else:
        text = f"{text}\n*Cached:* `True`"

    resp = requests.post(settings.SLACK_WEBHOOK_URL, json={"text": text})
    resp.raise_for_status()
