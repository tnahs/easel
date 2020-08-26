from src.easel import Easel

# easel = Easel("examples/template", loglevel="DEBUG")
easel = Easel("examples/snapshots", loglevel="DEBUG")


if __name__ == "__main__":

    # WIP: Placeholder-images/site-caching
    from src.easel.site import contents

    for page in easel.site.pages:
        for content in page.contents:
            if isinstance(content, contents.Image) and page.generate_placeholders:
                content.placeholder.cache_image()

    easel.run(debug=False)
