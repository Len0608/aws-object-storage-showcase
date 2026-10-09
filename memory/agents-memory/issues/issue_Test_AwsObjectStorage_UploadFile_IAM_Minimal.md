## Issue: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Status**: ✗ Failed

### Expected:
Upload local file /home/uac-agent/ue-test-inputs/upload_test.txt to S3 bucket at key test/upload_minimal.txt.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:34:25,390 - upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:34:25,390 - extension.py ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "errors": [{"type": "LocalFileNotFoundError", "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "exit_code": 1}]
}

**Known failure**: Test input file /home/uac-agent/ue-test-inputs/upload_test.txt does not exist on the remote agent host.
