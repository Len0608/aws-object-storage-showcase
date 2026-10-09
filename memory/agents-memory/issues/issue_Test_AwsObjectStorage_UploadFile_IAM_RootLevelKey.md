## Issue: Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Status**: ✗ Failed

### Expected:
File uploaded to S3 bucket "ue-test-aws-object-storage-2026" at root-level key "upload_root.txt".

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:21:23,895 - upload_file.py[80] ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:21:23,895 - extension.py[90] ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "exit_code": 1}]
}
