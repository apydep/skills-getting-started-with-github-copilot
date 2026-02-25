"""
Tests for signup endpoints (POST and DELETE /activities/{activity_name}/signup)

AAA Pattern:
- Arrange: Set up test data (activity name, email, TestClient)
- Act: Make POST or DELETE request to signup endpoint with query parameters
- Assert: Verify response status, message, and that participant list is updated
"""

import pytest


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client, sample_activity, sample_email):
        """
        Test successful signup for a new student.
        
        Arrange:
            - Activity name: "Chess Club" (exists in app data)
            - Email: "test.student@mergington.edu" (not yet signed up)
            - TestClient is available via fixture
        
        Act:
            - Send POST request to "/activities/Chess Club/signup?email=test.student..."
        
        Assert:
            - Status code is 200
            - Response contains success message
            - Verify student was added to activity by checking GET /activities
        """
        # Arrange
        activity_name = sample_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_fails(self, client, sample_activity):
        """
        Test that signing up twice with same email fails.
        
        Arrange:
            - Activity name: "Chess Club"
            - Email: "michael@mergington.edu" (already signed up in app data)
            - TestClient is available via fixture
        
        Act:
            - Send POST request to signup with email that's already in participants
        
        Assert:
            - Status code is 400
            - Response contains error detail about already signed up
        """
        # Arrange
        activity_name = sample_activity
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity_fails(self, client, sample_email, nonexistent_activity):
        """
        Test that signing up for non-existent activity fails.
        
        Arrange:
            - Activity name: "Nonexistent Activity XYZ" (doesn't exist)
            - Email: "test.student@mergington.edu"
            - TestClient is available via fixture
        
        Act:
            - Send POST request to signup for non-existent activity
        
        Assert:
            - Status code is 404
            - Response contains "Activity not found" error message
        """
        # Arrange
        activity_name = nonexistent_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUnregisterEndpoint:
    """Test suite for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_existing_student_success(self, client, sample_activity):
        """
        Test successful unregistration of an existing student.
        
        Arrange:
            - Activity name: "Chess Club"
            - Email: "michael@mergington.edu" (already signed up in app data)
            - TestClient is available via fixture
        
        Act:
            - Send DELETE request to "/activities/Chess Club/signup?email=michael..."
        
        Assert:
            - Status code is 200
            - Response contains success message
            - Verify student was removed from activity by checking GET /activities
        """
        # Arrange
        activity_name = sample_activity
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_student_fails(self, client, sample_activity, sample_email):
        """
        Test that unregistering a student not signed up fails.
        
        Arrange:
            - Activity name: "Chess Club"
            - Email: "test.student@mergington.edu" (not signed up)
            - TestClient is available via fixture
        
        Act:
            - Send DELETE request to unregister email that's not in participants
        
        Assert:
            - Status code is 400
            - Response contains error about student not being signed up
        """
        # Arrange
        activity_name = sample_activity
        email = sample_email  # Not in any activity

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_nonexistent_activity_fails(self, client, sample_email, nonexistent_activity):
        """
        Test that unregistering from non-existent activity fails.
        
        Arrange:
            - Activity name: "Nonexistent Activity XYZ" (doesn't exist)
            - Email: "test.student@mergington.edu"
            - TestClient is available via fixture
        
        Act:
            - Send DELETE request for non-existent activity
        
        Assert:
            - Status code is 404
            - Response contains "Activity not found" error message
        """
        # Arrange
        activity_name = nonexistent_activity
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
