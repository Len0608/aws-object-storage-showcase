## Test: Test_AwsObjectStorage_ListObjects_IAM_MaxRecordsSmall

**Status**: ✗ Failed

### Output:
```
STDERR: S3 ClientError: code=InvalidAccessKeyId
Extension Output: {"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records."}
```

### Notes:
- Extension executed with UE_MAX_OUTPUT_RECORDS=1 env var; failure due to placeholder credentials
- Known failure: no valid AWS credentials provided
