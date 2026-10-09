## Issue: Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Status**: ✗ Failed

### Expected:
Upload local file to root-level S3 key `upload_root.txt` in bucket `ue-test-aws-object-storage-2026`.

### STDOUT:
[empty]

### STDERR:
upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "errors": [{"type": "LocalFileNotFoundError"}]}

**Note**: The local file does not exist on the remote agent host. Extension correctly dispatched to Upload File action.
