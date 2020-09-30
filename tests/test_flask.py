from easel import Easel
from tests.test_configs import TestSites


def test__pages():

    easel = Easel(TestSites.valid)

    with easel.test_client() as client:

        for page in easel.site.pages:

            response_page = client.get(page.url)

            assert response_page.status_code == 200

        response_index = client.get("/")
        response_missing = client.get("/page-missing")

        assert response_index.status_code == 200
        assert response_missing.status_code == 200
