import pytest
from core.api_client import APIClient

# ---------------------
# Fixtures:
# SetUp and TerDown
# ---------------------
@pytest.fixture
def setup():
    # This will perform setup before each test
    # You can customize this further based on your needs
    print("Setting up the test...")
    yield
    print("Tearing down the test...")


@pytest.fixture
def teardown():
    print("Setting up...")
    yield
    print("Tearing down...")


@pytest.fixture(scope="session")
def api_client(sample_url):
    return APIClient(base_url=sample_url)


# ---------------------
# Add reporting
# ---------------------
def pytest_configure(config):
    # Register a custom marker for sanity tests
    config.addinivalue_line(
        "addopts", "-v --html=report.html --self-contained-html --title='PYTEST AUTOMATION REPORT'"
    )


def pytest_html_report_title(report):
    report.title = "API Automation Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([f"<p>Project: Sample API Tests</p><br/><p>{summary}</p><br/><p>{postfix}</p><quote>THAT's IT</quote>"])

# ---------------------
# pytest CLI options
# ---------------------
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run the tests against")
    parser.addoption("--browser", action="store", default="firefox", help="Browser to run the tests on")
    parser.addoption("--url", action="store", default="http://localhost", help="Web/API URL to run the tests against")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="session")
def sample_url() -> str:
    return "http://localhost"


@pytest.fixture
def config(request):
    env = request.config.getoption("--env")
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    return {"env": env, "browser": browser, "url": url}


@pytest.fixture
def config_setup(config):
    print(f"Running tests in {config['env']} environment on {config['browser']} browser, for {config['url']}")
    yield
    print("Cleaning up after tests...")


@pytest.fixture
def config_teardown(config):
    print(f"Tearing down {config['env']} environment on {config['browser']} browser, for {config['url']}")
    yield
    print("Cleaning up after tests...")
