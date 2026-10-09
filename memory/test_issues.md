# Test Issues Summary

All 10 tasks failed. Two distinct failure categories observed:

---

## Category 1: Invalid AWS Credentials (6 tasks)

**Root cause**: The `aws-s3-test-creds` credential contains placeholder values (`test-placeholder-key`). AWS rejected the access key with `InvalidAccessKeyId`.

**Affected tasks**:
- Test_AwsObjectStorage_ListObjects_IAM_Minimal
- Test_AwsObjectStorage_ListObjects_IAM_Full
- Test_AwsObjectStorage_ListObjects_IAM_MaxRecords50
- Test_AwsObjectStorage_ListObjects_IAM_MaxRecordsSmall
- Test_AwsObjectStorage_ListObjects_IAM_AfterUpload
- Test_AwsObjectStorage_ListObjects_IAM_AfterNestedUpload

**Error**: `S3 error: The AWS Access Key Id you provided does not exist in our records.`

**Extension behavior**: Correct — extension loaded, dispatched to List Objects action, created S3 client, and reached the API call before failing with a clear S3 service error.

---

## Category 2: Missing Local File on Agent Host (4 tasks)

**Root cause**: The local test file `/home/uac-agent/ue-test-inputs/upload_test.txt` does not exist on the remote agent host `sb-agent-ubu - AGNT0012`.

**Affected tasks**:
- Test_AwsObjectStorage_UploadFile_IAM_Minimal
- Test_AwsObjectStorage_UploadFile_IAM_NestedKey
- Test_AwsObjectStorage_UploadFile_IAM_Overwrite
- Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Error**: `Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt`

**Extension behavior**: Correct — extension loaded, dispatched to Upload File action, validated input fields, checked for local file existence, and returned a clear error with `LocalFileNotFoundError` type.

---

## Positive Observations

- The extension loaded and initialized correctly on all 10 runs (v1.0.0)
- Action dispatch worked correctly for both `List Objects` and `Upload File`
- Input field validation executed before S3 API calls (List Objects) and before file checks (Upload File)
- Error types and messages were structured and informative in all extension outputs
- Exit code 1 was returned consistently on failures
