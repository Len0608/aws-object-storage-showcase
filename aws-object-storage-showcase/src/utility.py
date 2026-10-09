"""
Utility module for the AWS Object Storage UAC Universal Extension.

Provides S3 client creation and thin wrapper methods for S3 operations:
- create_s3_client: Instantiates an authenticated boto3 S3 client
- list_all_objects: Paginates through all S3 objects in a bucket
- upload_file: Uploads a local file to S3
"""

import logging
import os
from typing import Optional

import boto3
import botocore.exceptions

from exceptions import (
    AuthenticationError,
    AccessDeniedError,
    BucketNotFoundError,
    LocalFileNotFoundError,
    S3ServiceError,
)

logger = logging.getLogger("UNV")

# boto3 ClientError codes that map to AuthenticationError
_AUTH_ERROR_CODES = frozenset({
    "AuthFailure",
    "InvalidClientTokenId",
    "UnrecognizedClientException",
    "ExpiredTokenException",
})

# boto3 ClientError codes that map to AccessDeniedError
_ACCESS_DENIED_CODES = frozenset({
    "AccessDenied",
    "AllAccessDisabled",
})


def create_s3_client(
    access_key_id: str,
    secret_access_key: str,
    region_name: str,
    session_token: Optional[str] = None,
) -> "boto3.client":
    """
    Instantiate and return an authenticated boto3 S3 client.

    Args:
        access_key_id: AWS Access Key ID (from UAC credential user field).
        secret_access_key: AWS Secret Access Key (from UAC credential password field).
        region_name: AWS region identifier (e.g., "us-east-1").
        session_token: Optional AWS Session Token for temporary STS credentials.
                       Pass None or an empty string when not required.

    Returns:
        A configured boto3 S3 client.
    """
    # Treat empty string as absent token
    token: Optional[str] = session_token if session_token else None

    logger.info("Creating S3 client for region: %s", region_name)
    logger.debug(
        "S3 client parameters: region=%s, access_key_id=***, session_token=%s",
        region_name,
        "provided" if token else "not provided",
    )

    client = boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=token,
        region_name=region_name,
    )

    logger.info("S3 client created successfully")
    return client


def list_all_objects(
    s3_client: "boto3.client",
    bucket_name: str,
) -> list[dict]:
    """
    List all objects in an S3 bucket using full pagination.

    Uses the boto3 S3 paginator for ``list_objects_v2`` to iterate through
    every page and collects all object records. An empty bucket returns an
    empty list.

    Each returned record is a dict with:
    - ``key`` (str): S3 object key
    - ``size`` (int): object size in bytes
    - ``last_modified`` (str): ISO 8601 UTC timestamp (``YYYY-MM-DDTHH:MM:SSZ``)

    Args:
        s3_client: An authenticated boto3 S3 client.
        bucket_name: Name of the S3 bucket to list.

    Returns:
        List of object record dicts. Empty list when the bucket has no objects.

    Raises:
        AuthenticationError: When credentials are rejected by AWS.
        BucketNotFoundError: When the specified bucket does not exist.
        AccessDeniedError: When IAM permissions are insufficient.
        S3ServiceError: For all other S3 API failures.
    """
    logger.info("Listing all objects in bucket: %s", bucket_name)

    paginator = s3_client.get_paginator("list_objects_v2")
    all_objects: list[dict] = []

    try:
        for page in paginator.paginate(Bucket=bucket_name):
            contents = page.get("Contents", [])
            logger.debug(
                "Page received: %d object(s)", len(contents)
            )
            for obj in contents:
                all_objects.append({
                    "key": obj["Key"],
                    "size": obj["Size"],
                    "last_modified": obj["LastModified"]
                    .astimezone(__import__("datetime").timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ"),
                })
    except botocore.exceptions.ClientError as exc:
        _raise_from_client_error(exc, bucket_name)

    logger.info(
        "Listed %d object(s) in bucket: %s", len(all_objects), bucket_name
    )
    return all_objects


def upload_file(
    s3_client: "boto3.client",
    local_file: str,
    bucket_name: str,
    s3_object_key: str,
) -> None:
    """
    Upload a local file to S3.

    Verifies the local file exists before initiating the upload, then
    delegates to the boto3 ``upload_file`` method. Any ``ClientError``
    raised by boto3 is mapped to the appropriate custom exception.

    Args:
        s3_client: An authenticated boto3 S3 client.
        local_file: Absolute path on the agent host to the file to upload.
        bucket_name: Destination S3 bucket name.
        s3_object_key: Destination object key within the bucket.

    Raises:
        LocalFileNotFoundError: When ``local_file`` does not exist on disk.
        AuthenticationError: When credentials are rejected by AWS.
        BucketNotFoundError: When the specified bucket does not exist.
        AccessDeniedError: When IAM permissions are insufficient.
        S3ServiceError: For all other S3 API failures.
    """
    logger.info(
        "Uploading file: %s → s3://%s/%s", local_file, bucket_name, s3_object_key
    )

    if not os.path.exists(local_file):
        logger.error("Local file not found: %s", local_file)
        raise LocalFileNotFoundError(local_file)

    try:
        s3_client.upload_file(
            Filename=local_file,
            Bucket=bucket_name,
            Key=s3_object_key,
        )
    except botocore.exceptions.ClientError as exc:
        _raise_from_client_error(exc, bucket_name)

    logger.info(
        "Upload complete: %s → s3://%s/%s", local_file, bucket_name, s3_object_key
    )


def _raise_from_client_error(
    exc: "botocore.exceptions.ClientError",
    bucket_name: str,
) -> None:
    """
    Map a boto3 ClientError to the appropriate custom exception and raise it.

    Args:
        exc: The ClientError raised by boto3.
        bucket_name: Bucket name used in the failed operation (for error messages).

    Raises:
        AuthenticationError: For auth-related error codes.
        BucketNotFoundError: For NoSuchBucket error code.
        AccessDeniedError: For access-denied error codes.
        S3ServiceError: For all other ClientError codes.
    """
    error_code: str = exc.response["Error"]["Code"]
    error_message: str = exc.response["Error"].get("Message", str(exc))

    logger.error(
        "S3 ClientError: code=%s, message=%s", error_code, error_message
    )

    if error_code in _AUTH_ERROR_CODES:
        raise AuthenticationError(error_message)
    if error_code == "NoSuchBucket":
        raise BucketNotFoundError(bucket_name)
    if error_code in _ACCESS_DENIED_CODES:
        raise AccessDeniedError(error_message)
    raise S3ServiceError(error_message)
