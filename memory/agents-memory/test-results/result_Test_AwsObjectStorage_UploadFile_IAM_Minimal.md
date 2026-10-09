## Test: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Status**: ✗ Failed

### Output:
```
STDERR: upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
EXTENSION: exit_code=1, status_description=Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
errors: [LocalFileNotFoundError]
```

### Notes:
- Known failure: test input file /home/uac-agent/ue-test-inputs/upload_test.txt does not exist on the remote agent host
- Extension loaded and ran correctly; file existence check executed properly; error propagated correctly
- Upload action path taken correctly (not List Objects)
