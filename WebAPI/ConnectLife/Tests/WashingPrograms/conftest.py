import pytest
from WebAPI.ConnectLife.Tests.WashingPrograms.JsonSchemas import CreateJsonSchemas

def pytest_configure():
    pytest.jsonSchemasWashingPrograms = CreateJsonSchemas()
