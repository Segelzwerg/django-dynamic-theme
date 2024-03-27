import os
import sys

from django import setup
from django.conf import settings
from django.test.utils import get_runner


def runtests():
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    return failures


if __name__ == "__main__":
    failures = runtests()
    sys.exit(bool(failures))
