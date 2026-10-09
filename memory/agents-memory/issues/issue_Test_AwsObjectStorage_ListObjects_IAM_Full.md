## Issue: Test_AwsObjectStorage_ListObjects_IAM_Full

**Status**: ✗ Failed

### Expected:
Complete list of all objects returned from S3 bucket "ue-test-aws-object-storage-2026".

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:22:39,649 - utility.py[208] ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:22:39,649 - extension.py[90] ERROR: Execution error: S3 error: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{
  "exit_code": 1,
  "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.",
  "errors": [{"type": "S3ServiceError", "message": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]
}
