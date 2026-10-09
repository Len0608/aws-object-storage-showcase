"""
Exceptions module for the AWS Object Storage UAC Universal Extension.

This module provides:
- Base ExecutionError class
- Standard exception types (DataValidationError, UnexpectedSystemError)
- AWS S3 specific exceptions (AuthenticationError, BucketNotFoundError,
  AccessDeniedError, S3ServiceError)
- Filesystem exception (LocalFileNotFoundError)
- Input validation exception (ValidationError)

Exit code conventions:
- 0: Successful execution
- 1: Operational failure (authentication, S3 API error, bucket not found,
     access denied, local file not found) — non-transient
- 20: Input validation error (missing or invalid required field values)
"""
from typing import Optional


class ExecutionError(Exception):
    """
    The default error raised by an extension.

    All extension errors must inherit from it.

    Attrs:
        exit_code: The exit code of the extension (for UAC)
        message: The error message for status description
    """

    exit_code: int = 1
    message: str = "Execution Failed"

    def __init__(self, message: Optional[str] = None):
        """
        Initialize exception.

        Args:
            message: Optional message that will be appended to the default message.

        Note:
            To return result data with errors, use error_manager.set_result()
            before raising the exception.
        """
        if message:
            self.message = f"{self.message}: {message}"

        super().__init__(self.message)


class DataValidationError(ExecutionError):
    """Raised when an input field is invalid."""
    exit_code = 20
    message = "Data Validation Error"


class UnexpectedSystemError(ExecutionError):
    """Raised for unexpected system errors."""
    exit_code = 1
    message = "System Error"


class ValidationError(ExecutionError):
    """
    Raised when a required input field is missing or fails validation.

    Use this exception when a field value does not meet the constraints
    defined for the action (e.g., empty required field, invalid format).

    Exit code 20 signals a user configuration error to UAC so the task
    is not eligible for automatic retry.
    """
    exit_code = 20
    message = "Validation Error"


class AuthenticationError(ExecutionError):
    """
    Raised when AWS IAM credentials are rejected by the S3 service.

    Maps to boto3 ClientError codes: AuthFailure,
    InvalidClientTokenId, UnrecognizedClientException,
    ExpiredTokenException.

    Exit code 1 signals a non-transient operational failure.
    Status description format: "Authentication failed: {error_message}"
    """
    exit_code = 1
    message = "Authentication failed"


class BucketNotFoundError(ExecutionError):
    """
    Raised when the specified S3 bucket does not exist.

    Maps to boto3 ClientError code: NoSuchBucket.

    Exit code 1 signals a non-transient operational failure.
    Status description format: "Bucket not found: {bucket_name}"
    """
    exit_code = 1
    message = "Bucket not found"


class AccessDeniedError(ExecutionError):
    """
    Raised when AWS IAM permissions are insufficient for the requested operation.

    Maps to boto3 ClientError codes: AccessDenied, AllAccessDisabled.

    Exit code 1 signals a non-transient operational failure.
    Status description format: "Access denied: {error_message}"
    """
    exit_code = 1
    message = "Access denied"


class S3ServiceError(ExecutionError):
    """
    Raised when the S3 service returns an unexpected or unclassified error.

    Maps to all boto3 ClientError codes not handled by the more specific
    exception classes (AuthenticationError, BucketNotFoundError,
    AccessDeniedError).

    Exit code 1 signals a potentially transient operational failure.
    Status description format: "S3 error: {error_message}"
    """
    exit_code = 1
    message = "S3 error"


class LocalFileNotFoundError(ExecutionError):
    """
    Raised when the local file path supplied for an Upload File action does
    not exist on the Universal Agent host filesystem.

    This exception is raised before the S3 client is created, so no AWS
    call is made when the local file is missing.

    Exit code 1 signals a non-transient user input error.
    Status description format: "Local file not found: {local_file_path}"
    """
    exit_code = 1
    message = "Local file not found"
