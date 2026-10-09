"""Upload File action — uploads a local file to an S3 bucket."""

import logging
import os
from typing import Optional

from actions.output import ActionOutput
from exceptions import LocalFileNotFoundError, ValidationError
from fields.input import InputFields
from fields.output import OutputFields
from manager import ExtensionManager
from utility import create_s3_client, upload_file as utility_upload_file

logger = logging.getLogger("UNV")
extension_manager = ExtensionManager()


def upload_file(input_data: InputFields) -> ActionOutput:
    """Upload a local file from the Universal Agent host to an S3 bucket.

    Validates all required fields, verifies the local file exists, then
    uploads via the boto3 S3 client. Returns a confirmation in STDOUT,
    populates the status output field, and returns a structured Extension
    Output JSON.

    Args:
        input_data: Validated input fields.

    Returns:
        ActionOutput with the upload result, status description, and exit code.

    Raises:
        ValidationError: When aws_region, bucket_name, local_file, or
            s3_object_key is empty.
        LocalFileNotFoundError: When the local_file path does not exist on disk.
        AuthenticationError: When AWS credentials are rejected.
        BucketNotFoundError: When the specified bucket does not exist.
        AccessDeniedError: When IAM permissions are insufficient.
        S3ServiceError: For all other S3 API failures.
    """
    logger.info("Starting upload_file action")
    logger.debug(
        "Input: action=%s, aws_region=%s, bucket_name=%s, local_file=%s, s3_object_key=%s",
        input_data.action.value if input_data.action else None,
        input_data.aws_region.value if input_data.aws_region else None,
        input_data.bucket_name.value if input_data.bucket_name else None,
        input_data.local_file.value if input_data.local_file else None,
        input_data.s3_object_key.value if input_data.s3_object_key else None,
    )

    # Initialize output fields for real-time UI updates
    output_fields = OutputFields()

    # Step 1: Input Validation
    logger.info("Validating input fields")
    if not input_data.aws_region or not input_data.aws_region.value.strip():
        logger.error("aws_region is required but was not provided")
        raise ValidationError("aws_region is required")

    if not input_data.bucket_name or not input_data.bucket_name.value.strip():
        logger.error("bucket_name is required but was not provided")
        raise ValidationError("bucket_name is required")

    if not input_data.local_file or not input_data.local_file.value.strip():
        logger.error("local_file is required but was not provided")
        raise ValidationError("local_file is required")

    if not input_data.s3_object_key or not input_data.s3_object_key.value.strip():
        logger.error("s3_object_key is required but was not provided")
        raise ValidationError("s3_object_key is required")

    aws_region: str = input_data.aws_region.value.strip()
    bucket_name: str = input_data.bucket_name.value.strip()
    local_file: str = input_data.local_file.value.strip()
    s3_object_key: str = input_data.s3_object_key.value.strip()

    # Step 2: Verify local file exists
    logger.info("Verifying local file exists: %s", local_file)
    if not os.path.exists(local_file):
        logger.error("Local file not found: %s", local_file)
        raise LocalFileNotFoundError(local_file)

    # Step 3: Create S3 client
    access_key_id: str = input_data.aws_credentials.user
    secret_access_key: str = input_data.aws_credentials.password
    session_token: Optional[str] = input_data.aws_credentials.token or None

    logger.info("Creating S3 client")
    s3_client = create_s3_client(
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        region_name=aws_region,
        session_token=session_token,
    )

    # Step 4: Upload file
    output_fields.update(status="Uploading")
    logger.info(
        "Uploading file: %s → s3://%s/%s", local_file, bucket_name, s3_object_key
    )
    utility_upload_file(
        s3_client=s3_client,
        local_file=local_file,
        bucket_name=bucket_name,
        s3_object_key=s3_object_key,
    )

    # Step 5: Write STDOUT confirmation
    print(f"Upload complete: {local_file} → s3://{bucket_name}/{s3_object_key}")

    # Step 6: Populate output fields
    filename: str = os.path.basename(local_file)
    status_text = f"Uploaded {filename} → s3://{bucket_name}/{s3_object_key}"
    output_fields.update(status=status_text)
    logger.debug("Output field status updated: %s", status_text)

    # Step 7: Return result
    logger.info("upload_file action completed successfully")
    logger.debug(
        "Returning: bucket=%s, key=%s, local_file=%s",
        bucket_name,
        s3_object_key,
        local_file,
    )

    return ActionOutput(
        result={
            "bucket": bucket_name,
            "key": s3_object_key,
            "local_file": local_file,
        },
        status_description=status_text,
        exit_code=0,
    )
