from WebAPI.ConnectLife.Tests.Content.HandleContent import HandleTest
import pytest

@pytest.mark.prod
def test_get_guides(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/guides" + ("?id=" + params["id"] if params["id"] != "" else "")
    HandleTest(url, params, token)