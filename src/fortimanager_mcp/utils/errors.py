"""Custom exception classes for FortiManager MCP server."""


class FortiManagerError(Exception):
    """Base exception for all FortiManager-related errors."""

    def __init__(self, message: str, code: int | None = None, details: dict | None = None) -> None:
        """Initialize FortiManager error.

        Args:
            message: Human-readable error message
            code: FortiManager error code (if available)
            details: Additional error context
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of error."""
        if self.code is not None:
            return f"[Error {self.code}] {self.message}"
        return self.message

    def to_dict(self) -> dict:
        """Convert error to dictionary for serialization."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


class AuthenticationError(FortiManagerError):
    """Raised when authentication fails."""

    pass


class ConnectionError(FortiManagerError):
    """Raised when connection to FortiManager fails."""

    pass


class APIError(FortiManagerError):
    """Raised when FortiManager API returns an error."""

    pass


class ValidationError(FortiManagerError):
    """Raised when input validation fails."""

    pass


class ResourceNotFoundError(FortiManagerError):
    """Raised when a requested resource is not found."""

    pass


class PermissionError(FortiManagerError):
    """Raised when operation is not permitted."""

    pass


class TimeoutError(FortiManagerError):
    """Raised when request times out."""

    pass


# Common FortiManager error code mappings
ERROR_CODE_MAP = {
    -1: ("Internal error", APIError),
    -2: ("Object already exists", APIError),
    -3: ("Object does not exist", ResourceNotFoundError),
    -4: ("Permission denied", PermissionError),
    -5: ("Invalid request format", ValidationError),
    -6: ("Invalid argument", ValidationError),
    -10: ("Action not allowed", PermissionError),
    -11: ("No permission for the resource", PermissionError),
    -20: ("Session expired", AuthenticationError),
}


def parse_fmg_error(code: int, message: str, url: str | None = None) -> FortiManagerError:
    """Parse FortiManager error code and create appropriate exception.

    Args:
        code: FortiManager error code
        message: Error message from FortiManager
        url: API URL that caused the error

    Returns:
        Appropriate FortiManagerError subclass
    """
    details = {"url": url} if url else {}

    if code in ERROR_CODE_MAP:
        error_msg, error_class = ERROR_CODE_MAP[code]
        return error_class(f"{error_msg}: {message}", code=code, details=details)

    return APIError(message, code=code, details=details)

