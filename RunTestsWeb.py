import pytest
import sys


def main() -> int:
    retcode = pytest.main(["Web/Gorenje/", "-s"])
    return retcode

if __name__ == "__main__":
    main()
