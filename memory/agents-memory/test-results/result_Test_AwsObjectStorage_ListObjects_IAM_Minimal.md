## Test: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:31:37,988 - utility.py ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
EXTENSION: exit_code=1, status_description=S3 error: The AWS Access Key Id you provided does not exist in our records.
```

### Notes:
- Known failure: placeholder AWS credentials (test-placeholder-key) are not valid AWS access keys
- Extension loaded and ran correctly; S3 client created; API call attempted and properly errored
