# Test Plan

**Extension:** aws-object-storage-showcase
**Template:** Aws Object Storage Showcase
**Generated:** 2026-10-09

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT contains a rounded_outline table with columns Key, Size (bytes), Last Modified
- Output field status is populated (e.g. "Found N objects")
- Output field object_count is populated with the number of objects
- Extension Output JSON contains result.bucket, result.count, result.truncated, result.objects

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_Full

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT contains a rounded_outline table with all listed objects
- Output field status set to "Found N objects"
- Output field object_count populated
- Extension Output JSON structure is valid with result.objects array

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_MaxRecords50

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Environment Variables:**
- UE_MAX_OUTPUT_RECORDS: 50
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT table contains at most 50 rows
- If bucket has more than 50 objects, truncation note appears in STDOUT and warning in STDERR
- result.objects array in Extension Output contains at most 50 entries
- result.count reflects total object count (not capped)

---

## Test: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
- local_file: /home/uac-agent/ue-test-inputs/upload_test.txt
- s3_object_key: test/upload_minimal.txt
**Expected Results:**
- Task completes with exit code 0
- STDOUT contains "Upload complete: /home/uac-agent/ue-test-inputs/upload_test.txt → s3://ue-test-aws-object-storage-2026/test/upload_minimal.txt"
- Output field status set to "Uploaded upload_test.txt → s3://ue-test-aws-object-storage-2026/test/upload_minimal.txt"
- Extension Output JSON contains result.bucket, result.key, result.local_file

---

## Test: Test_AwsObjectStorage_UploadFile_IAM_NestedKey

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
- local_file: /home/uac-agent/ue-test-inputs/upload_test.txt
- s3_object_key: test/nested/subdir/upload_nested.txt
**Expected Results:**
- Task completes with exit code 0
- STDOUT contains "Upload complete: /home/uac-agent/ue-test-inputs/upload_test.txt → s3://ue-test-aws-object-storage-2026/test/nested/subdir/upload_nested.txt"
- Output field status set correctly with deeply nested S3 key
- Extension Output JSON result.key matches the nested path

---

## Test: Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
- local_file: /home/uac-agent/ue-test-inputs/upload_test.txt
- s3_object_key: upload_root.txt
**Expected Results:**
- Task completes with exit code 0
- STDOUT contains upload confirmation with root-level key (no path prefix)
- Output field status set to "Uploaded upload_test.txt → s3://ue-test-aws-object-storage-2026/upload_root.txt"
- Extension Output JSON result.key equals "upload_root.txt"

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_AfterUpload

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT table includes the object uploaded by Test_AwsObjectStorage_UploadFile_IAM_Minimal (test/upload_minimal.txt)
- result.count is at least 1 (reflecting the uploaded object plus any seed objects)
- result.objects array contains entries with key, size, last_modified fields

---

## Test: Test_AwsObjectStorage_UploadFile_IAM_Overwrite

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: Upload File
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
- local_file: /home/uac-agent/ue-test-inputs/upload_test.txt
- s3_object_key: test/nested/subdir/upload_nested.txt
**Expected Results:**
- Task completes with exit code 0 (S3 allows overwriting an existing object key)
- STDOUT contains upload confirmation for the same nested key used in Test_AwsObjectStorage_UploadFile_IAM_NestedKey
- Extension Output JSON result.key matches test/nested/subdir/upload_nested.txt

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_AfterNestedUpload

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT table includes the nested key object (test/nested/subdir/upload_nested.txt)
- result.count reflects all objects including the overwritten entry
- Table rows display correct key, size, and last_modified values

---

## Test: Test_AwsObjectStorage_ListObjects_IAM_MaxRecordsSmall

**Template:** Aws Object Storage Showcase
**Agent:** sb-agent-ubu - AGNT0012
**Environment Variables:**
- UE_MAX_OUTPUT_RECORDS: 1
**Input Fields:**
- action: List Objects
- aws_credentials: aws-s3-test-creds
- aws_region: us-east-1
- bucket_name: ue-test-aws-object-storage-2026
**Expected Results:**
- Task completes with exit code 0
- STDOUT table contains exactly 1 row (capped by UE_MAX_OUTPUT_RECORDS=1)
- Truncation note appears in STDOUT: "[Note: Output truncated to 1 records (total: N objects). Set UE_MAX_OUTPUT_RECORDS to adjust the limit.]"
- STDERR contains truncation warning
- result.objects array has exactly 1 entry; result.count equals total object count; result.truncated is true

---
