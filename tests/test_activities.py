"""
Tests for the activities endpoint (GET /activities)

AAA Pattern:
- Arrange: TestClient fixture provided by conftest.py
- Act: Make GET request to /activities endpoint
- Assert: Verify response structure, status code, and data format
"""

import pytest


class TestActivitiesEndpoint:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns 200 with all activities.
        
        Arrange:
            - TestClient is available via fixture
        
        Act:
            - Send GET request to "/activities"
        
        Assert:
            - Status code is 200
            - Response is a dictionary (not empty)
            - Contains expected activity keys
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Robotics Club",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity has the required structure.
        
        Arrange:
            - TestClient is available via fixture
        
        Act:
            - Send GET request to "/activities"
            - Extract first activity from response
        
        Assert:
            - Activity contains: description, schedule, max_participants, participants
            - participants is a list
            - max_participants is an integer
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = list(activities.values())[0]

        # Assert
        for field in required_fields:
            assert field in first_activity
        assert isinstance(first_activity["participants"], list)
        assert isinstance(first_activity["max_participants"], int)

    def test_activities_have_participants(self, client):
        """
        Test that activities contain participant email addresses.
        
        Arrange:
            - TestClient is available via fixture
        
        Act:
            - Send GET request to "/activities"
        
        Assert:
            - At least one activity has participants
            - Participants are strings (email-like format)
        """
        # Arrange
        # (client fixture already set up)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        found_participants = False
        for activity_name, activity_data in activities.items():
            if activity_data["participants"]:
                found_participants = True
                for participant in activity_data["participants"]:
                    assert isinstance(participant, str)
                    assert "@" in participant  # Email-like format

        assert found_participants, "At least one activity should have participants"
