## Test: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:10:15,446 - extension.py INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:10:15,446 - extension.py INFO: Action requested: List Objects
2026-10-09 12:10:15,867 - utility.py ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:10:15,867 - extension.py ERROR: Execution error: S3 error: The AWS Access Key Id you provided does not exist in our records.

Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ServiceError"}]}
```

### Notes:
- Extension reached the S3 API call successfully; failure is due to placeholder AWS credentials (InvalidAccessKeyId)
- Known failure: no valid AWS credentials provided
