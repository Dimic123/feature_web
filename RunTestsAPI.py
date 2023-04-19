import pytest
import sys


def main() -> int:
    retcode = pytest.main(["WebAPI/Juconnect/Tests/", "-s"])
    return retcode

if __name__ == "__main__":
    main()
