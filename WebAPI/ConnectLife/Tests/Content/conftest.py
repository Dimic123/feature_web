import pytest
from WebAPI.ConnectLife.Tests.Content.JsonSchemas import CreateJsonSchemas

def pytest_configure():
    pytest.jsonSchemasContent = CreateJsonSchemas()
