import pytest
import os
import signal
import time
import logging
import cProfile
from unittest.mock import MagicMock
import coverage
import pdb
    


# -------------------------------
# For INI file configuration
# -------------------------------
def pytest_configure(config):
    # Register a custom marker for sanity tests
    config.addinivalue_line(
        "markers", "sanity: mark a test as a sanity test"
    )

# -------------------------------
# For command line options
# -------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--sanity",
        action="store_true",
        default=False,
        help="run only sanity tests",
    )
    parser.addoption(
        "--skip-sanity",
        action="store_true",
        default=False,
        help="skip sanity tests",
    )
    

# -------------------------------
# For FIXTURES
# -------------------------------
@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    # This fixture will run once per session
    print("\nSetting up the test session...")
    yield
    print("\nTearing down the test session...")

@pytest.fixture
def sample_fixture():
    # This is a sample fixture that can be used in tests
    # You can customize this further based on your needs
    return "sample data"

@pytest.fixture
def another_fixture():
    # This is another sample fixture that can be used in tests
    # You can customize this further based on your needs
    return "another sample data"


# -------------------------------
# For Parameterization
# -------------------------------
@pytest.mark.parametrize("input, expected", [
    (1, 2),
    (2, 3),
    (3, 4),
])
def test_increment(input, expected):
    assert input + 1 == expected
    # This will parameterize the test with different inputs and expected outputs
    # You can customize this further based on your needs


# For test fixtures with parameters
@pytest.fixture(params=[1, 2, 3])
def param_fixture(request):
    return request.param

def test_param_fixture(param_fixture):
    assert param_fixture in [1, 2, 3]
    # This will parameterize the fixture with different values
    # You can customize this further based on your needs


# -------------------------------
# For test Retries
# -------------------------------
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # Retry the test if it fails
        item.session.testsfailed += 1
        item.session.testsfailed -= 1
        item.rerun = True
        print(f"\nRetrying {item.name}...")
    # This will retry failed tests
    # You can customize this further based on your needs


# -------------------------------
# For test timeouts
# -------------------------------
class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Test timed out")


def pytest_runtest_setup(item):
    # Set a timeout for each test
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # Set a timeout of 5 seconds
    # This will set a timeout for each test
    # You can customize this further based on your needs

def pytest_runtest_teardown(item):
    # Cancel the timeout after the test completes
    signal.alarm(0)
    # This will cancel the timeout after each test completes
    # You can customize this further based on your needs


# -------------------------------
# For test skipping
# based on conditions
# -------------------------------
def pytest_runtest_setup(item):
    if "SKIP_TEST" in os.environ:
        pytest.skip("Skipping test due to SKIP_TEST environment variable")
    # This will skip tests based on the presence of an environment variable
    # You can customize this further based on your needs


# -------------------------------
# For test collection 
# based on the defined markers
# -------------------------------
def pytest_collection_modifyitems(config, items):
    if config.getoption("--sanity"):
        # If --sanity is given, skip all tests that are not marked as sanity
        for item in items:
            if "sanity" not in item.keywords:
                item.add_marker(pytest.mark.skip(reason="Skipping non-sanity test"))
    elif config.getoption("--skip-sanity"):
        # If --skip-sanity is given, skip all tests that are marked as sanity
        for item in items:
            if "sanity" in item.keywords:
                item.add_marker(pytest.mark.skip(reason="Skipping sanity test"))


# -------------------------------
# For test reporting
# -------------------------------
def pytest_runtest_makereport(item, call):
    if call.when == "call":
        if call.excinfo is not None:
            print(f"\nTest {item.name} failed")
        else:
            print(f"\nTest {item.name} passed")
    else:
        print(f"\nSetting up {item.name}...")
    # This will print a message before each test setup
    # and after each test teardown
    # You can customize this further based on your needs


# For test output formatting
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.section("Custom Test Summary")
    terminalreporter.write("This is a custom summary of the test run.\n")
    # You can add more details here based on the test results
    # For example, you can iterate through the test results and print them
    # terminalreporter.write(f"Total tests run: {len(terminalreporter.stats)}\n")
    # terminalreporter.write(f"Total tests passed: {len(terminalreporter.stats.get('passed', []))}\n")
    # terminalreporter.write(f"Total tests failed: {len(terminalreporter.stats.get('failed', []))}\n")
    # You can also customize the output format here


# For test dependencies
def pytest_runtest_setup(item):
    # Check if the test has dependencies
    dependencies = item.get_closest_marker("depends")
    if dependencies:
        for dep in dependencies.args:
            if not item.session.items[dep].passed:
                pytest.skip(f"Skipping {item.name} due to dependency on {dep}")
    # This will skip tests based on their dependencies
    # You can customize this further based on your needs

# --------------------------------
# For test ordering
# --------------------------------
def pytest_collection_modifyitems(config, items):
    # Sort tests by their names
    items.sort(key=lambda item: item.name)
    # This will sort tests by their names
    # You can customize this further based on your needs


# --------------------------------
# For test filtering
# --------------------------------
def pytest_collection_modifyitems(config, items):
    # Filter tests based on their names
    filtered_items = []
    for item in items:
        if "filter" in item.name:
            filtered_items.append(item)
    items[:] = filtered_items
    # This will filter tests based on their names
    # You can customize this further based on your needs

# --------------------------------
# For test skipping
# --------------------------------
@pytest.mark.skip(reason="This test is skipped for demonstration purposes")
def test_skipped():
    assert False
    # This will skip the test with a reason
    # You can customize this further based on your needs


# --------------------------------
# For test marking
# --------------------------------
@pytest.mark.sanity
def test_sanity():
    assert True
    # This will mark the test as a sanity test
    # You can customize this further based on your needs

# --------------------------------
# For test assertions
# --------------------------------
def test_assertion():
    assert 1 == 1
    # This will perform a simple assertion
    # You can customize this further based on your needs


# --------------------------------
# For test cleanup
# --------------------------------
@pytest.fixture
def cleanup():
    yield
    # This will perform cleanup after each test
    # You can customize this further based on your needs
    print("Cleaning up after the test...")


# --------------------------------
# For test setup
# --------------------------------
@pytest.fixture
def setup():
    # This will perform setup before each test
    # You can customize this further based on your needs
    print("Setting up the test...")
    yield
    print("Tearing down the test...")


# --------------------------------
# For test teardown
# --------------------------------
@pytest.fixture
def teardown():
    # This will perform teardown after each test
    # You can customize this further based on your needs
    print("Tearing down the test...")
    yield
    print("Cleaning up after the test...")


# --------------------------------
# For test logging
# --------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def test_logging():
    logger.info("This is a test log message")
    # This will log a message during the test
    # You can customize this further based on your needs


# --------------------------------
# For test debugging
# --------------------------------
def test_debugging():
    pdb.set_trace()
    # This will set a breakpoint during the test
    # You can customize this further based on your needs


# --------------------------------
# For test profiling
# --------------------------------
def test_profiling():
    import cProfile
    profiler = cProfile.Profile()
    profiler.enable()
    # Your test code here
    profiler.disable()
    profiler.print_stats()
    # This will profile the test and print the stats
    # You can customize this further based on your needs


# --------------------------------
# For test coverage
# --------------------------------
def test_coverage():
    cov = coverage.Coverage()
    cov.start()
    # Your test code here
    cov.stop()
    cov.save()
    cov.report()
    # This will measure the code coverage of the test
    # You can customize this further based on your needs


# --------------------------------
# For test mocking
# --------------------------------
def test_mocking():
    mock = MagicMock()
    mock.return_value = 42
    assert mock() == 42
    # This will mock a function and assert its return value
    # You can customize this further based on your needs

# --------------------------------
# For test fixtures with setup and teardown
# --------------------------------
@pytest.fixture
def setup_teardown():
    print("Setting up...")
    yield
    print("Tearing down...")

def test_setup_teardown(setup_teardown):
    assert True
    # This will perform setup and teardown for the test
    # You can customize this further based on your needs


# --------------------------------
# For test fixtures with scope
# --------------------------------
@pytest.fixture(scope="module")
def module_fixture():
    print("Setting up module fixture...")
    yield
    print("Tearing down module fixture...")

def test_module_fixture(module_fixture):
    assert True
    # This will perform setup and teardown for the module fixture
    # You can customize this further based on your needs


# --------------------------------
# For test fixtures with autouse
# --------------------------------
@pytest.fixture(autouse=True)
def autouse_fixture():
    print("Setting up autouse fixture...")
    yield
    print("Tearing down autouse fixture...")