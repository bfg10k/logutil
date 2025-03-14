import time
import traceback
from collections import namedtuple

from .console_handler import ConsoleHandler
from .datadog_handler import DatadogConfig, DatadogHandler
from .file_handler import FileHandler
from .levels import LEVEL_ERROR, LEVEL_INFO, LEVEL_WARN
from .message_queue import MessageQueue

Message = namedtuple("Message", ["timestamp", "level", "message", "params"])


class Logger:
    def __init__(self):
        self.outputs = []

    def info(self, message, **kwargs):
        self.add(Message(time.time(), LEVEL_INFO, message, kwargs))

    def error(self, message, **kwargs):
        self.add(Message(time.time(), LEVEL_ERROR, message, kwargs))

    def warn(self, message, **kwargs):
        self.add(Message(time.time(), LEVEL_WARN, message, kwargs))

    def traceback(self):
        self.add(Message(time.time(), LEVEL_ERROR, traceback.format_exc(), None))

    def add(self, message):
        for output in self.outputs:
            output.add(message)


def init_logger(
    console: bool = True,
    file: str | None = "/tmp/app.log",
    datadog: DatadogConfig | None = None,
):
    assert isinstance(console, bool)
    assert isinstance(file, str) or file is None
    assert isinstance(datadog, dict) or datadog is None

    new_outputs = []
    if console:
        new_outputs.append(ConsoleHandler())
    if file is not None:
        new_outputs.append(MessageQueue(FileHandler(file), 0.1))
    if datadog is not None:
        new_outputs.append(MessageQueue(DatadogHandler(datadog), 1))

    log.outputs = new_outputs


log = Logger()
init_logger()
