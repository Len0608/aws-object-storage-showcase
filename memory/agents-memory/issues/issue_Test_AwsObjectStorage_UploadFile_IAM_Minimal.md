## Issue: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Status**: ✗ Failed

### Expected:
Upload local file `/home/uac-agent/ue-test-inputs/upload_test.txt` to S3 key `test/upload_minimal.txt` in bucket `ue-test-aws-object-storage-2026`.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:12:24,459 - extension.py INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:12:24,459 - extension.py INFO: Action requested: Upload File
2026-10-09 12:12:24,460 - extension.py INFO: Executing action: Upload File
2026-10-09 12:12:24,460 - upload_file.py INFO: Starting upload_file action
2026-10-09 12:12:24,460 - upload_file.py INFO: Validating input fields
2026-10-09 12:12:24,460 - upload_file.py INFO: Verifying local file exists: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:12:24,460 - upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:12:24,460 - extension.py ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:12:24,477 - extension_start_result.py ERROR: Error in extension: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "exit_code": 1}]
}

**Note**: The local file `/home/uac-agent/ue-test-inputs/upload_test.txt` does not exist on the remote agent host. The extension correctly validated input, dispatched to Upload File action, and returned a clear error.
