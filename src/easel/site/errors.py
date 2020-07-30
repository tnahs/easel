import logging


logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class ConfigError(Error):
    def __init__(self, message: str):
        super().__init__(message)


class MissingContent(Error):
    def __init__(self, message: str):
        super().__init__(message)


class UnsupportedContentType(Error):
    def __init__(self, message: str):
        super().__init__(message)
