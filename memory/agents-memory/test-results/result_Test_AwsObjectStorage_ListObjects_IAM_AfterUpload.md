## Test: Test_AwsObjectStorage_ListObjects_IAM_AfterUpload

**Status**: ✗ Failed

### Output:
```
STDERR: S3 ClientError: code=InvalidAccessKeyId - The AWS Access Key Id you provided does not exist in our records.
EXTENSION: exit_code=1, status_description=S3 error: The AWS Access Key Id you provided does not exist in our records.
```

### Notes:
- Known failure: placeholder AWS credentials (test-placeholder-key) are not valid AWS access keys
- Extension loaded and ran correctly; API call attempted and properly errored
