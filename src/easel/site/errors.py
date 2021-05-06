import logging


logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class ConfigLoadError(Error):
    pass


class SiteConfigError(Error):
    pass
