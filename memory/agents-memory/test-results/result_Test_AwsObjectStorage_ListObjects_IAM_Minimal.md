## Test: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:21:58,926 - utility.py[208] ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.

Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ServiceError"}]}
```

### Notes:
- Extension dispatched correctly to List Objects action
- S3 client created successfully — boto3 integration is working
- Failed at AWS API call due to placeholder credential (InvalidAccessKeyId) — expected known failure
- extensionStatus field set to "Listing objects" confirming correct action execution path
