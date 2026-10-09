## Issue: Test_AwsObjectStorage_UploadFile_IAM_NestedKey

**Status**: ✗ Failed

### Expected:
File uploaded to S3 bucket "ue-test-aws-object-storage-2026" at nested key "test/nested/subdir/upload_nested.txt".

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:20:14,437 - extension.py[63] INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:20:14,437 - extension.py[70] INFO: Action requested: Upload File
2026-10-09 12:20:14,438 - upload_file.py[80] ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:20:14,438 - extension.py[90] ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "metadata": {"version": "1.0.0", "extension": "aws-object-storage-showcase"},
  "input_fields": {
    "action": ["Upload File"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-object-storage-2026",
    "local_file": "/home/uac-agent/ue-test-inputs/upload_test.txt",
    "s3_object_key": "test/nested/subdir/upload_nested.txt"
  },
  "result": {},
  "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "exit_code": 1}]
}
