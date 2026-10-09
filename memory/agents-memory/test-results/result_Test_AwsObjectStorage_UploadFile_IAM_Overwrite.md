## Test: Test_AwsObjectStorage_UploadFile_IAM_Overwrite

**Status**: ✗ Failed

### Output:
```
STDERR: upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
EXTENSION: exit_code=1, errors: [LocalFileNotFoundError]
```

### Notes:
- Known failure: test input file /home/uac-agent/ue-test-inputs/upload_test.txt does not exist on the remote agent host
- Extension loaded correctly; file existence check executed properly; error propagated correctly
