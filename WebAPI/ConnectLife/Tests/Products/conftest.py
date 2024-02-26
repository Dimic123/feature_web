import pytest
from WebAPI.ConnectLife.Tests.Products.JsonSchemas import CreateJsonSchemas

def pytest_configure():
    pytest.jsonSchemasProducts = CreateJsonSchemas()
