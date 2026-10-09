## Test: Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Status**: ✗ Failed

### Output:
```
STDERR: upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
Extension Output: {"exit_code": 1, "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt"}
```

### Notes:
- Extension dispatched to Upload File action; failed because test file does not exist on remote agent host
- Root-level S3 key: upload_root.txt
