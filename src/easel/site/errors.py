import logging


logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(message)


class SiteConfigError(Error):
    pass


class MenuConfigError(Error):
    pass


class PageConfigError(Error):
    pass


class ContentConfigError(Error):
    pass


class TemplateConfigError(Error):
    pass


class MissingContent(Error):
    pass


class UnsupportedContentType(Error):
    pass
