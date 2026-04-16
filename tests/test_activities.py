from fastapi import status

from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"].startswith("Learn strategies")


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()
    assert email not in original_participants

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_for_activity_rejects_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "nobody@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "test_student_remove@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()
    if email not in original_participants:
        activities[activity_name]["participants"].append(email)

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing_student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()
    if email in original_participants:
        activities[activity_name]["participants"].remove(email)

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Participant not found"
    finally:
        activities[activity_name]["participants"] = original_participants
