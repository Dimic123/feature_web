import pytest
import sys


def main() -> int:
    retcode = pytest.main(["Mobile/ConnectLife/", "-s", "--driver", "appium"])
    return retcode


if __name__ == "__main__":
    main()
