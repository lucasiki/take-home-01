from main import MainEvent
from tests.run_tests import run_tests

if __name__ == '__main__':
    mainevent = MainEvent(initial_file='./test_data.json')
    run_tests(mainevent)