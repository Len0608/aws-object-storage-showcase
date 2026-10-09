## Test: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR: upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
Extension Output: {"exit_code": 1, "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt", "errors": [{"type": "LocalFileNotFoundError"}]}
```

### Notes:
- Extension dispatched correctly to Upload File action; failed because test file does not exist on remote agent host
- The file /home/uac-agent/ue-test-inputs/upload_test.txt was not pre-created on the agent
