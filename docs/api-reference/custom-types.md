# Custom types

``` python
# Import Easel's Page, Menu and Content factories.
from easel.site.pages import page_factory
from easel.site.menus import menu_factory
from easel.site.contents import content_factory

# Import your custom types.
from .custom import CustomPage, CustomMenu, CustomContent

# Register your custom types.
page_factory.register_page_type("custom-page", CustomPage)
menu_factory.register_menu_type("custom-menu", CustomMenu)
content_factory.register_content_type("custom-content", CustomContent)
```
