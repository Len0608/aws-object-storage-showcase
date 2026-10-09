## Test: Test_AwsObjectStorage_UploadFile_IAM_RootLevelKey

**Status**: ✗ Failed

### Output:
```
STDERR:
2026-10-09 12:21:23,895 - upload_file.py[80] ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

Extension Output:
{"exit_code": 1, "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt"}
```

### Notes:
- Extension dispatched correctly to Upload File action
- Same root cause as all Upload File tests — source file absent on remote agent
