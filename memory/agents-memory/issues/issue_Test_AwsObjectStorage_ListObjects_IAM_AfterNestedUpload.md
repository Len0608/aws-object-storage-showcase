## Issue: Test_AwsObjectStorage_ListObjects_IAM_AfterNestedUpload

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket after a prior nested upload operation (dependency test).

### STDOUT:
[empty]

### STDERR:
S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ServiceError"}]}

**Note**: Failure is due to placeholder AWS credentials. Extension reached S3 API call correctly.
