from __future__ import annotations

import httpx
import pytest

from clash_royale.exceptions import (
    ClashRoyaleBadRequestError,
    ClashRoyaleException,
    ClashRoyaleHTTPError,
    ClashRoyaleNotFoundError,
    ClashRoyaleRateLimitError,
    ClashRoyaleServerError,
    ClashRoyaleUnauthorizedError,
    InvalidAPIKeyError,
)


def test_clash_royale_exception() -> None:
    """Test base ClashRoyaleException."""
    error = ClashRoyaleException("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_invalid_api_key_error_default() -> None:
    """Test InvalidAPIKeyError with default message."""
    error = InvalidAPIKeyError()
    assert "API key is required" in str(error)
    assert "developer.clashroyale.com" in str(error)
    assert isinstance(error, ClashRoyaleException)


def test_invalid_api_key_error_custom() -> None:
    """Test InvalidAPIKeyError with custom message."""
    error = InvalidAPIKeyError("Custom error message")
    assert str(error) == "Custom error message"


def test_exception_hierarchy() -> None:
    """Test exception hierarchy is correct."""
    # Base exception
    assert issubclass(ClashRoyaleException, Exception)

    # HTTP errors inherit from base
    assert issubclass(ClashRoyaleHTTPError, ClashRoyaleException)
    assert issubclass(InvalidAPIKeyError, ClashRoyaleException)

    # Specific HTTP errors inherit from ClashRoyaleHTTPError
    assert issubclass(ClashRoyaleNotFoundError, ClashRoyaleHTTPError)
    assert issubclass(ClashRoyaleUnauthorizedError, ClashRoyaleHTTPError)
    assert issubclass(ClashRoyaleRateLimitError, ClashRoyaleHTTPError)
    assert issubclass(ClashRoyaleBadRequestError, ClashRoyaleHTTPError)
    assert issubclass(ClashRoyaleServerError, ClashRoyaleHTTPError)


def test_exception_catching() -> None:
    """Test that exceptions can be caught properly."""
    # Create a mock HTTPStatusError
    request = httpx.Request("GET", "https://api.clashroyale.com/v1/players/%23TEST")
    response = httpx.Response(404, request=request, text="Not found")
    http_error = httpx.HTTPStatusError("Not found", request=request, response=response)

    error = ClashRoyaleNotFoundError(http_error)

    # Catching specific exception
    with pytest.raises(ClashRoyaleNotFoundError):
        raise error

    # Catching base ClashRoyaleHTTPError
    with pytest.raises(ClashRoyaleHTTPError):
        raise error

    # Catching base ClashRoyaleException
    with pytest.raises(ClashRoyaleException):
        raise error

    # Catching as generic Exception
    with pytest.raises(Exception):
        raise error


def create_http_error(status_code: int, text: str = "Error") -> httpx.HTTPStatusError:
    """Helper to create HTTPStatusError for testing."""
    request = httpx.Request("GET", "https://api.clashroyale.com/v1/test")
    response = httpx.Response(status_code, request=request, text=text)
    return httpx.HTTPStatusError(text, request=request, response=response)


def test_from_http_error_404() -> None:
    """Test from_http_error returns ClashRoyaleNotFoundError for 404."""
    http_error = create_http_error(404, "Not found")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleNotFoundError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_403() -> None:
    """Test from_http_error returns ClashRoyaleUnauthorizedError for 403."""
    http_error = create_http_error(403, "Forbidden")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleUnauthorizedError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_429() -> None:
    """Test from_http_error returns ClashRoyaleRateLimitError for 429."""
    http_error = create_http_error(429, "Too many requests")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleRateLimitError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_400() -> None:
    """Test from_http_error returns ClashRoyaleBadRequestError for 400."""
    http_error = create_http_error(400, "Bad request")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleBadRequestError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_500() -> None:
    """Test from_http_error returns ClashRoyaleServerError for 500."""
    http_error = create_http_error(500, "Internal server error")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleServerError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_503() -> None:
    """Test from_http_error returns ClashRoyaleServerError for 503."""
    http_error = create_http_error(503, "Service unavailable")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert isinstance(error, ClashRoyaleServerError)
    assert isinstance(error, ClashRoyaleHTTPError)


def test_from_http_error_other() -> None:
    """Test from_http_error returns base ClashRoyaleHTTPError for other status codes."""
    http_error = create_http_error(418, "I'm a teapot")
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    assert type(error) is ClashRoyaleHTTPError
    assert not isinstance(error, ClashRoyaleNotFoundError)
    assert not isinstance(error, ClashRoyaleUnauthorizedError)


def test_http_error_initialization_with_response() -> None:
    """Test ClashRoyaleHTTPError initialization with response."""
    http_error = create_http_error(404, "Not found")
    error = ClashRoyaleHTTPError(http_error)

    # The error should store status code, url, and text
    assert error.args[0] == 404
    assert "api.clashroyale.com" in str(error.args[1])
    assert error.args[2] == "Not found"


def test_http_error_initialization_without_response() -> None:
    """Test ClashRoyaleHTTPError initialization without response."""
    request = httpx.Request("GET", "https://api.clashroyale.com/v1/test")
    http_error = httpx.HTTPStatusError("Error", request=request, response=None)  # ty:ignore[invalid-argument-type]
    error = ClashRoyaleHTTPError(http_error)

    # Should fall back to storing the exception itself
    assert error.args[0] == http_error


def test_from_http_error_without_response() -> None:
    """Test from_http_error when response is None."""
    request = httpx.Request("GET", "https://api.clashroyale.com/v1/test")
    http_error = httpx.HTTPStatusError("Error", request=request, response=None)  # ty:ignore[invalid-argument-type]
    error = ClashRoyaleHTTPError.from_http_error(http_error)

    # Should return base ClashRoyaleHTTPError
    assert type(error) is ClashRoyaleHTTPError
