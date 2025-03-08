import os
from logutil import init_logger, logger

api_key = os.environ["DATADOG_API_KEY"]

init_logger(
    datadog={
        "api_key": api_key,
        "site": "US3",
        "service": "logutil",
        "tags": {"env": "dev"},
    },
)

logger.info("Hello", a=1, b=[10, 20, 30], c="foo")

try:
    raise Exception("this is a test error")
except Exception:
    logger.traceback()
