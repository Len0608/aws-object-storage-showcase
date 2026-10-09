# Test Issues Summary

All 10 tests failed due to missing infrastructure:

## List Objects Tests (6 tasks) — Root Cause: Invalid AWS Credentials
Tasks: ListObjects_IAM_Minimal, ListObjects_IAM_Full, ListObjects_IAM_MaxRecords50, ListObjects_IAM_MaxRecordsSmall, ListObjects_IAM_AfterUpload, ListObjects_IAM_AfterNestedUpload
- **Error**: `S3 ClientError: code=InvalidAccessKeyId — The AWS Access Key Id you provided does not exist in our records.`
- The extension started and dispatched correctly; the S3 API was called with the credential values from `aws-s3-test-creds` (user=`test-placeholder-key`), which are placeholder values that do not exist in AWS.

## Upload File Tests (4 tasks) — Root Cause: Missing local test file on agent host
Tasks: UploadFile_IAM_Minimal, UploadFile_IAM_NestedKey, UploadFile_IAM_Overwrite, UploadFile_IAM_RootLevelKey
- **Error**: `Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt`
- The extension started and dispatched correctly; file existence check ran before any S3 call; the test input file was not present on the remote agent host.

## Positive Findings
- Extension loaded and started correctly in all 10 runs (v1.0.0)
- Action dispatch worked correctly (List Objects → list_objects.py, Upload File → upload_file.py)
- Credential object was accessed correctly (user/password attributes, not subscript)
- Error handling and exit codes were propagated properly in all cases
- Extension status fields were set correctly where applicable
