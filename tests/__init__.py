
import os


def start_testing():
    if "tests" in os.listdir():
        os.system("pytest tests")
