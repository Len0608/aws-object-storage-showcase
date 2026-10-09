## Issue: Test_AwsObjectStorage_ListObjects_IAM_MaxRecords50

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket with UE_MAX_OUTPUT_RECORDS=50 environment variable, limiting output to 50 records.

### STDOUT:
[empty]

### STDERR:
S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
Extension reached S3 API call with UE_MAX_OUTPUT_RECORDS=50 set in environment.

### Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ServiceError"}]}

**Note**: Failure is due to placeholder AWS credentials. Environment variable UE_MAX_OUTPUT_RECORDS=50 was passed successfully.
