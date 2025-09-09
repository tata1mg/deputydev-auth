from typing import Any, Dict

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def init_sentry(sentry_config: Dict[str, Any]) -> None:
    if not sentry_config["DSN"]:
        return

    sentry_sdk.init(
        dsn=sentry_config["DSN"],
        traces_sample_rate=sentry_config["TRACES_SAMPLE_RATE"],
        environment=sentry_config["ENVIRONMENT"],
        release=sentry_config["RELEASE_TAG"],
        enable_logs=sentry_config["ENABLE_LOGS"],
        debug=sentry_config["DEBUG"],
        integrations=[FastApiIntegration(), RedisIntegration(), StarletteIntegration()],
    )
