## Issue: Test_AwsObjectStorage_ListObjects_IAM_MaxRecords50

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket limited to 50 records (UE_MAX_OUTPUT_RECORDS=50).

### STDOUT:
[empty]

### STDERR:
S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
exit_code: 1
status_description: S3 error: The AWS Access Key Id you provided does not exist in our records.
errors: [S3ServiceError] InvalidAccessKeyId

**Known failure**: Placeholder AWS credentials (test-placeholder-key) are not valid AWS access keys.
