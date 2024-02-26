import os
from WebAPI.ConnectLife.Tests.WashingPrograms.HandleContent import HandleTest
import pytest

@pytest.mark.prod
def test_get_washing_programs_langs(token: str, params: dict):
    url = "https://api.connectlife.io/api/v1/washing-programs/" + params["lang"]
    filePath = os.path.realpath(__file__)
    HandleTest(url, params, token, filePath)