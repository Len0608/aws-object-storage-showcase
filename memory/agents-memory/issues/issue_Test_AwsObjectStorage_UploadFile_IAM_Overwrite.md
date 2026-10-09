## Issue: Test_AwsObjectStorage_UploadFile_IAM_Overwrite

**Status**: ✗ Failed

### Expected:
Upload and overwrite S3 key `test/nested/subdir/upload_nested.txt` with the local file.

### STDOUT:
[empty]

### STDERR:
upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "errors": [{"type": "LocalFileNotFoundError"}]}

**Note**: The local file does not exist on the remote agent host. Extension correctly dispatched to Upload File action and validated input.
