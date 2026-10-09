## Issue: Test_AwsObjectStorage_ListObjects_IAM_Full

**Status**: ✗ Failed

### Expected:
List all objects in S3 bucket `ue-test-aws-object-storage-2026` using List Objects action with full IAM credentials.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:11:02,618 - extension.py INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:11:02,619 - extension.py INFO: Action requested: List Objects
2026-10-09 12:11:02,619 - extension.py INFO: Executing action: List Objects
2026-10-09 12:11:02,619 - list_objects.py INFO: Starting list_objects action
2026-10-09 12:11:02,619 - list_objects.py INFO: Validating input fields
2026-10-09 12:11:02,619 - list_objects.py INFO: Creating S3 client
2026-10-09 12:11:02,619 - utility.py INFO: Creating S3 client for region: us-east-1
2026-10-09 12:11:02,694 - utility.py INFO: S3 client created successfully
2026-10-09 12:11:02,694 - list_objects.py INFO: Listing objects in bucket: ue-test-aws-object-storage-2026
2026-10-09 12:11:02,694 - utility.py INFO: Listing all objects in bucket: ue-test-aws-object-storage-2026
2026-10-09 12:11:03,019 - utility.py ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:11:03,019 - extension.py ERROR: Execution error: S3 error: The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:11:03,038 - extension_start_result.py ERROR: Error in extension: S3 error: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{
  "exit_code": 1,
  "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.",
  "errors": [{"type": "S3ServiceError", "message": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]
}

**Note**: Failure is due to placeholder AWS credentials. The extension executed correctly and reached the S3 API call.
