## Test: Test_AwsObjectStorage_ListObjects_IAM_MaxRecordsSmall

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:23:44,953 - utility.py[208] ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.

Extension Output:
{"exit_code": 1, "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "errors": [{"type": "S3ServiceError"}]}
```

### Notes:
- Environment variable UE_MAX_OUTPUT_RECORDS=1 was passed correctly (confirmed in task instance)
- Extension dispatched to List Objects action correctly
- Failed at AWS API call due to placeholder credential — expected known failure
