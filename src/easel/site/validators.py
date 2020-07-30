# site.yaml
# ["pages"]["width"]
# ["pages"]["align"]
# ["color"]["accent-base"]
# ["color"]["accent-light"]
# ["menu"]["items"]
# ["menu"]["width"]
# ["menu"]["align"]
# ["menu"]["header"]["image"]["width"]
# ["menu"]["header"]["image"]["height"]

# def _validate_pages(self):

#     """
#     pages:
#         - layout:
#             path: layout
#             landing: true
#         - markdown:
#             path: markdown
#         - lazy:
#             path: lazy
#     """

#     try:
#         pages = self._config["pages"]
#     except IndexError as error:
#         raise errors.ConfigError(
#             f"Missing 'pages' in {config.file_site_yaml}."
#         ) from error

#     if not pages:
#         raise errors.ConfigError(
#             f"No pages 'pages' specified in {config.file_site_yaml}."
#         )

#     for page in pages:
#         for page_type, page_data in page.items():

#             if page_type not in config.VALID_PAGE_TYPES:
#                 raise errors.SiteConfigError(f"Unsupported page type '{page_type}'.")

#             try:
#                 path = page_data["path"]
#             except IndexError as error:
#                 raise errors.ConfigError(f"Missing 'path' in {page_data}.") from error

#             if not path:
#                 raise errors.ConfigError(
#                     f"No 'path' specified in {config.file_site_yaml}."
#                 )


# def _validate_menu(self):

#     try:
#         self._config["menu"]["header"]
#         self._config["menu"]["header"]["label"]
#         self._config["menu"]["header"]["image"]
#         self._config["menu"]["header"]["image"]["is-enabled"]
#         self._config["menu"]["header"]["image"]["path"]
#         self._config["menu"]["header"]["image"]["width"]
#         self._config["menu"]["header"]["image"]["height"]
#         self._config["menu"]["items"]
#     except IndexError as error:
#         raise errors.ConfigError(
#             f"Missing required item in {config.file_site_yaml}."
#         ) from error


# def _validate_info(self):

#     try:
#         self._config["info"]
#         self._config["info"]["title"]
#         self._config["info"]["year"]
#         self._config["info"]["user"]
#         self._config["info"]["user"]["name"]
#         self._config["info"]["user"]["email"]
#     except IndexError as error:
#         raise errors.ConfigError(
#             f"Missing required item in {config.file_site_yaml}."
#         ) from error
