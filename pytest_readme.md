
#examples of how to run pytests:

#collection only (no execution)
pytest --collect-only test_application.py

#executing only the tests marked with samsung label in verbose mode
pytest -m samsung -v test_application.py

#executing default mode (will run everything with test_ prefix in front)
pytest test_applicaiton.py

#pytest generic will collect and execute all files and folders with test_ prefix
pytest


Exit codes
Running pytest can result in six different exit codes:

Exit code 0
All tests were collected and passed successfully

Exit code 1
Tests were collected and run but some of the tests failed

Exit code 2
Test execution was interrupted by the user

Exit code 3
Internal error happened while executing tests

Exit code 4
pytest command line usage error

Exit code 5
No tests were collected


