from enum import Enum


class E_Directory(str, Enum):
    BUILD = "build"
    CONTENTS = "contents"
    PAGES = "pages"
    SITE_CACHE = "site-cache"
    STATIC = "static"
    TEMPLATES = "templates"
    THEMES = "themes"


class E_Filename(str, Enum):
    SITE_YAML = "site.yaml"
    PAGE_YAML = "page.yaml"
    THEME_YAML = "theme.yaml"
    TEMPLATE_MAIN_HTML = "main.html"
    TEMPLATE_404_HTML = "404.html"


class E_Mimetype(str, Enum):
    MP4 = "video/mp4"
    WEBM = "video/webm"
    MOV = "video/quicktime"
    MP3 = "audio/mpeg"
    WAV = "audio/wav"


class E_Page(str, Enum):
    AUTO = "auto"
    LAYOUT = "layout"
    AUTO_GALLERY = "auto-gallery"
    LAYOUT_GALLERY = "layout-gallery"


class E_Menu(str, Enum):
    LINK_PAGE = "link-page"
    LINK_URL = "link-url"
    SPACER = "spacer"


class E_Content(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    MARKDOWN = "markdown"
    EMBEDDED = "embedded"
    HEADER = "header"
    BREAK = "break"


class E_Size(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class E_Alignment(str, Enum):
    START = "start"
    CENTER = "center"
    END = "end"
