import pytest, sys, os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

def main() -> int:
    retcode = pytest.main([os.path.join(ROOT_DIR, "Web", "Gorenje"), "-s"])
    return retcode


if __name__ == "__main__":
    main()
