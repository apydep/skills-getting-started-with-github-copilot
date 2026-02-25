"""
Tests for the root endpoint (GET /)

AAA Pattern:
- Arrange: TestClient fixture provided by conftest.py
- Act: Make GET request to root endpoint without following redirects
- Assert: Verify redirect response and target URL
"""

import pytest


class TestRootEndpoint:
    """Test suite for GET / endpoint."""

    def test_root_redirects_to_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange:
            - TestClient is available via fixture
        
        Act:
            - Send GET request to "/" with follow_redirects=False
        
        Assert:
            - Status code is 307 (Temporary Redirect)
            - Location header points to /static/index.html
        """
        # Arrange
        # (client fixture already set up)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
