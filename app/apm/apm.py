from __future__ import annotations

import os
from typing import Any, Dict

from elasticapm import Client
from elasticapm.contrib.starlette import make_apm_client
from fastapi import __version__ as fastapi_version

APM_CLIENT: Client | None = None


def get_apm_client(apm_config: Dict[str, Any], service_config: Dict[str, Any]) -> Client:
    global APM_CLIENT  # noqa: PLW0603
    APM_CLIENT = make_apm_client(
        config={
            **apm_config,
            "FRAMEWORK_NAME": "fastapi",
            "FRAMEWORK_VERSION": fastapi_version,
            "DISABLE_LOG_RECORD_FACTORY": True,
            "SERVICE_CONFIG": os.environ.get("RELEASE_TAG"),
            "SERVICE_NAME": service_config["NAME"],
        }
    )

    return APM_CLIENT
