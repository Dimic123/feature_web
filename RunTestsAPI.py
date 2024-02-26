import pytest
import sys


def main() -> int:
    retcode = pytest.main(["WebAPI/ConnectLife/Tests/", "-s", "--auth", "swagger"])
    # retcode = pytest.main(["WebAPI/ConnectLife/Tests/", "-s", "--auth", "swagger", "-m", "prod"])
    
    # retcode = pytest.main(["WebAPI/HiJuConn/Tests/", "-s", "--auth", "juconnect"])
    return retcode


if __name__ == "__main__":
    main()
