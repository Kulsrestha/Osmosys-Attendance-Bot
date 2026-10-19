
import random
from pathlib import Path

import requests

from config import (
    API_BASE_URL,
    API_TOKEN,
    ORGANISATION_ID,
    SITE_ID,
    USER_ID,
    CHECKIN_LATITUDE,
    CHECKIN_LONGITUDE,
    CHECKOUT_LATITUDE,
    CHECKOUT_LONGITUDE,
    TEST_PHOTO_PATH,
    DRY_RUN,
)

# API field names from the supplied Angular code.
PHOTO_FIELDS = {
    "CheckIn": "checkInPhoto",
    "CheckOut": "checkOutPhoto",
}

COMMENT_FIELDS = {
    "CheckIn": "checkInComment",
    "CheckOut": "checkOutComment",
}

COMMENT_TEXT = {
    "CheckIn": "Checking in",
    "CheckOut": "Checking out",
}

# Exact hostname confirmed by the user.
ALLOWED_API_HOST = "osmosys-api.oqsha.com"


ALLOWED_API_HOST = "osmosys-api.oqsha.com"


def _validate_api_host(base_url: str) -> str:
    parsed_url = requests.utils.urlparse(base_url)
    host = (parsed_url.hostname or "").lower()

    if not host:
        raise ValueError("API_BASE_URL must be a valid HTTPS URL.")

    if parsed_url.scheme.lower() != "https":
        raise ValueError("Only HTTPS API_BASE_URL values are allowed.")

    if host != ALLOWED_API_HOST:
        raise RuntimeError(
            f"Blocked API request to '{host}'. "
            f"Only '{ALLOWED_API_HOST}' is allowed."
        )

    return host


def submit_attendance(status: str) -> str:
    if status not in ("CheckIn", "CheckOut"):
        raise ValueError("Unsupported attendance status.")

    # Select coordinates according to the requested action.
    if status == "CheckIn":
        latitude = CHECKIN_LATITUDE
        longitude = CHECKIN_LONGITUDE
    else:
        latitude = CHECKOUT_LATITUDE
        longitude = CHECKOUT_LONGITUDE

    endpoint = (
        f"{API_BASE_URL.rstrip('/')}/Organisations/"
        f"{ORGANISATION_ID}/Attendance"
    )

    # Dry-run mode displays details without sending a request.
    if DRY_RUN:
        return (
            "DRY RUN only — no API request sent.\n"
            f"Action: {status}\n"
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"
            f"Endpoint: {endpoint}\n"
            "Payload fields: attendanceStatus, latitude, longitude, "
            f"siteId, userId, {PHOTO_FIELDS[status]}, "
            f"{COMMENT_FIELDS[status]}\n"
            "Set DRY_RUN=false to attempt API submission."
        )

    # Validate the host before sending any request.
    _validate_api_host(API_BASE_URL)

    if not API_TOKEN:
        raise RuntimeError("API_TOKEN is missing.")

    if not all([ORGANISATION_ID, SITE_ID, USER_ID]):
        raise RuntimeError(
            "ORGANISATION_ID, SITE_ID, and USER_ID must be configured."
        )

    if TEST_PHOTO_PATH:
        photo_path = Path(TEST_PHOTO_PATH)
        if not photo_path.is_file():
            raise FileNotFoundError(f"Test photo not found: {photo_path}")
    else:
        photo_folder = Path(__file__).resolve().parent / "photos"
        photo_options = sorted(
            path for path in photo_folder.iterdir()
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
        )
        if not photo_options:
            raise FileNotFoundError(f"No supported photos found in {photo_folder}")
        photo_path = random.choice(photo_options)

    data = {
        "attendanceStatus": status,
        "latitude": str(latitude),
        "longitude": str(longitude),
        "siteId": str(SITE_ID),
        "userId": str(USER_ID),
        COMMENT_FIELDS[status]: COMMENT_TEXT[status],
    }

    # Accept API_TOKEN with or without the "Bearer " prefix.
    token = API_TOKEN.strip()

    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        with photo_path.open("rb") as photo:
            files = {
                PHOTO_FIELDS[status]: (
                    photo_path.name,
                    photo,
                    "image/jpeg",
                )
            }

            response = requests.post(
                endpoint,
                headers=headers,
                data=data,
                files=files,
                timeout=20,
            )

        try:
            body = response.json()
        except ValueError:
            body = {"Message": response.text[:500]}

        if response.ok:
            return (
                f"Attendance API request completed.\n"
                f"HTTP status: {response.status_code}\n"
                f"Response: {body}"
            )

        return (
            f"Attendance API request failed.\n"
            f"HTTP status: {response.status_code}\n"
            f"Response: {body}"
        )

    except requests.RequestException as exc:
        return f"Attendance API request error: {exc}"
