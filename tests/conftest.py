"""
Pytest configuration and shared fixtures for backend tests.

AAA Pattern (Arrange-Act-Assert):
- Arrange: Fixtures set up test data and TestClient
- Act: Test functions execute API calls
- Assert: Assertions verify expected outcomes
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
import copy

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


# Store initial state of activities for test isolation
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Arrange: Reset activities to initial state before each test.
    
    This ensures test isolation by resetting any modifications made
    to the in-memory activities dictionary during test execution.
    """
    # Reset before test
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """
    Arrange: Provide a TestClient instance for all tests.
    
    Returns:
        TestClient: FastAPI test client for making HTTP requests
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Arrange: Provide a test email for signup scenarios."""
    return "test.student@mergington.edu"


@pytest.fixture
def sample_activity():
    """Arrange: Provide a test activity name that exists in the app."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Arrange: Provide an activity name that doesn't exist."""
    return "Nonexistent Activity XYZ"
