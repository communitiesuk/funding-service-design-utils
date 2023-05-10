import pytest
from fsd_utils.simple_utils.data_utils import get_remote_data_as_json
from requests.exceptions import HTTPError


class TestDataUtils:
    def test_get_remote_data_json(self, flask_test_client):
        postcode = "SW1P 4DF"
        result = get_remote_data_as_json(f"https://postcodes.io/postcodes/{postcode}")
        assert postcode == result["result"]["postcode"]

    def test_get_remote_data_json_404(self, flask_test_client):
        with pytest.raises(HTTPError):
            get_remote_data_as_json("https://postcodes.io/postcodes/QQ11QQ")
