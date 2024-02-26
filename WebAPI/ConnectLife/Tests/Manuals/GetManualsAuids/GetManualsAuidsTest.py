import os

from WebAPI.ConnectLife.Tests.Manuals.HandleContent import HandleTest
import pytest

@pytest.mark.prod
def test_get_manuals_auids(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/manuals/" + ";".join(params["auids"])
    filePath = os.path.realpath(__file__)
    HandleTest(url, params, token, filePath)