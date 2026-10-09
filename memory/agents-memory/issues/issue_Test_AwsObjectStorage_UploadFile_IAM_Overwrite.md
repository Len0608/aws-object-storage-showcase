## Issue: Test_AwsObjectStorage_UploadFile_IAM_Overwrite

**Status**: ✗ Failed

### Expected:
File uploaded (overwriting existing object) to S3 bucket "ue-test-aws-object-storage-2026" at key "test/nested/subdir/upload_nested.txt".

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:20:49,611 - extension.py[63] INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:20:49,611 - extension.py[70] INFO: Action requested: Upload File
2026-10-09 12:20:49,611 - upload_file.py[80] ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:20:49,611 - extension.py[90] ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "exit_code": 1}]
}
