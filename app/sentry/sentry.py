import logging
import os
from typing import Any, Dict

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def init_sentry(sentry_config: Dict[str, Any]) -> None:
    if not sentry_config["DSN"]:
        return

    event_level = logging.WARNING if sentry_config.get("CAPTURE_WARNING") else logging.ERROR
    integrations = [
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
        LoggingIntegration(event_level=event_level),
    ]
    sentry_sdk.set_tag("service_name", "testing")
    sentry_sdk.init(
        dsn=sentry_config["DSN"],
        environment=sentry_config["ENVIRONMENT"],
        release=os.getenv("RELEASE_TAG"),
        debug=False,
        integrations=integrations,
        send_default_pii=True,
    )
