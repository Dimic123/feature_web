import pytest
from WebAPI.ConnectLife.Tests.Manuals.JsonSchemas import CreateJsonSchemas

def pytest_configure():
    pytest.jsonSchemasManuals = CreateJsonSchemas()
