# Test Issues Summary

**Run Date**: 2026-10-09
**Extension**: aws-object-storage-showcase v1.0.0
**Agent**: sb-agent-ubu - AGNT0012
**Template**: Aws Object Storage Showcase

---

## Upload File Tests (4 tasks) — All ✗ Failed

**Root Cause**: Source file `/home/uac-agent/ue-test-inputs/upload_test.txt` does not exist on the remote agent host.

| Task | Error Type | Error Message |
|------|-----------|---------------|
| Test_AwsObjectStorage_UploadFile_IAM_Minimal | LocalFileNotFoundError | Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt |
| Test_AwsObjectStorage_UploadFile_IAM_NestedKey | LocalFileNotFoundError | Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt |
| Test_AwsObjectStorage_UploadFile_IAM_Overwrite | LocalFileNotFoundError | Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt |
| Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey | LocalFileNotFoundError | Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt |

**Note**: Extension successfully started, dispatched to Upload File action, validated inputs, and checked for the local file before failing. Extension flow and error handling are correct.

---

## List Objects Tests (6 tasks) — All ✗ Failed

**Root Cause**: AWS credential `aws-s3-test-creds` uses placeholder value `test-placeholder-key` which is not a valid AWS Access Key ID. All list operations reach the AWS API before failing with `InvalidAccessKeyId`.

| Task | Error Type | Error Message |
|------|-----------|---------------|
| Test_AwsObjectStorage_ListObjects_IAM_Minimal | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |
| Test_AwsObjectStorage_ListObjects_IAM_Full | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |
| Test_AwsObjectStorage_ListObjects_IAM_MaxRecords50 | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |
| Test_AwsObjectStorage_ListObjects_IAM_MaxRecordsSmall | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |
| Test_AwsObjectStorage_ListObjects_IAM_AfterUpload | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |
| Test_AwsObjectStorage_ListObjects_IAM_AfterNestedUpload | S3ServiceError | S3 error: The AWS Access Key Id you provided does not exist in our records. |

**Note**: Extension successfully started, dispatched to List Objects action, validated inputs, and created a boto3 S3 client before failing at the AWS API call. The boto3 S3 client creation (`utility.py`) worked correctly. The `extensionStatus` field was correctly set to "Listing objects" in all instances.

---

## Summary

All 10 tests failed as expected due to missing test environment prerequisites:
1. **Upload tests**: Test input file not present on agent host
2. **List tests**: Placeholder AWS credentials (not real IAM keys)

These are known infrastructure/credential failures, not extension code defects.
