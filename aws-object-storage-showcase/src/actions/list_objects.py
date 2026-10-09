"""List Objects action — retrieves all objects in an S3 bucket."""

import logging
import os
import sys
from typing import Optional

from tabulate import tabulate

from actions.output import ActionOutput
from exceptions import ValidationError
from fields.input import InputFields
from fields.output import OutputFields
from manager import ExtensionManager
from utility import create_s3_client, list_all_objects

logger = logging.getLogger("UNV")
extension_manager = ExtensionManager()

_DEFAULT_MAX_RECORDS = 100


def list_objects(input_data: InputFields) -> ActionOutput:
    """List all objects in the specified S3 bucket.

    Retrieves all objects using list_objects_v2 with full pagination support.
    Displays results as a rounded_outline formatted table in STDOUT, capped
    at UE_MAX_OUTPUT_RECORDS. Populates the status and object_count output
    fields and returns a structured Extension Output JSON.

    Args:
        input_data: Validated input fields.

    Returns:
        ActionOutput with the listing result, status description, and exit code.

    Raises:
        ValidationError: When aws_region or bucket_name is empty.
        AuthenticationError: When AWS credentials are rejected.
        BucketNotFoundError: When the specified bucket does not exist.
        AccessDeniedError: When IAM permissions are insufficient.
        S3ServiceError: For all other S3 API failures.
    """
    logger.info("Starting list_objects action")
    logger.debug(
        "Input: action=%s, aws_region=%s, bucket_name=%s",
        input_data.action.value if input_data.action else None,
        input_data.aws_region.value if input_data.aws_region else None,
        input_data.bucket_name.value if input_data.bucket_name else None,
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

    aws_region: str = input_data.aws_region.value.strip()
    bucket_name: str = input_data.bucket_name.value.strip()

    # Step 2: Read environment configuration
    max_records: int = _DEFAULT_MAX_RECORDS
    raw_max = os.environ.get("UE_MAX_OUTPUT_RECORDS", "")
    if raw_max:
        try:
            parsed = int(raw_max)
            if parsed > 0:
                max_records = parsed
            else:
                logger.warning(
                    "UE_MAX_OUTPUT_RECORDS=%s is not a positive integer; using default %d",
                    raw_max,
                    _DEFAULT_MAX_RECORDS,
                )
        except ValueError:
            logger.warning(
                "UE_MAX_OUTPUT_RECORDS=%s cannot be parsed as integer; using default %d",
                raw_max,
                _DEFAULT_MAX_RECORDS,
            )
    logger.debug("max_records=%d", max_records)

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

    # Step 4: List all objects with pagination
    output_fields.update(status="Listing objects")
    logger.info("Listing objects in bucket: %s", bucket_name)
    all_objects = list_all_objects(s3_client=s3_client, bucket_name=bucket_name)
    total_count: int = len(all_objects)
    logger.info("Retrieved %d object(s) from bucket: %s", total_count, bucket_name)

    # Step 5: Apply output cap
    truncated: bool = total_count > max_records
    display_objects = all_objects[:max_records]
    logger.debug(
        "truncated=%s, display_count=%d, total_count=%d",
        truncated,
        len(display_objects),
        total_count,
    )

    # Step 6: Write STDOUT table
    rows = [
        [obj["key"], obj["size"], obj["last_modified"]]
        for obj in display_objects
    ]
    table = tabulate(
        rows,
        headers=["Key", "Size (bytes)", "Last Modified"],
        tablefmt="rounded_outline",
    )
    print(table)
    if truncated:
        print(
            f"[Note: Output truncated to {max_records} records "
            f"(total: {total_count} objects). "
            f"Set UE_MAX_OUTPUT_RECORDS to adjust the limit.]"
        )
        logger.debug("STDOUT truncation note printed")

    # Step 7: Write STDERR warning if truncated
    if truncated:
        print(
            f"WARNING: Output truncated. Bucket contains {total_count} objects; "
            f"display limited to {max_records} by UE_MAX_OUTPUT_RECORDS.",
            file=sys.stderr,
        )
        logger.warning(
            "Output truncated: %d total objects, displaying %d",
            total_count,
            max_records,
        )

    # Step 8: Populate output fields
    status_text = f"Found {total_count} objects"
    output_fields.update(
        status=status_text,
        object_count=str(total_count),
    )
    logger.debug("Output fields updated: status=%s, object_count=%s", status_text, str(total_count))

    # Step 9: Return result
    logger.info("list_objects action completed successfully")
    logger.debug(
        "Returning: bucket=%s, count=%d, truncated=%s",
        bucket_name,
        total_count,
        truncated,
    )

    return ActionOutput(
        result={
            "bucket": bucket_name,
            "count": total_count,
            "truncated": truncated,
            "objects": display_objects,
        },
        status_description=status_text,
        exit_code=0,
    )
