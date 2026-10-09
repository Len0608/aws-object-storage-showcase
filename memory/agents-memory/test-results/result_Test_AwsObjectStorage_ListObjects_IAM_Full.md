## Test: Test_AwsObjectStorage_ListObjects_IAM_Full

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:11:03,019 - utility.py ERROR: S3 ClientError: code=InvalidAccessKeyId
Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records."}
```

### Notes:
- Extension executed and reached S3 API; failure due to placeholder credentials (InvalidAccessKeyId)
- Known failure: no valid AWS credentials provided
