## Issue: Test_AwsObjectStorage_UploadFile_IAM_NestedKey

**Status**: ✗ Failed

### Expected:
Upload local file to S3 at a deeply nested key path (test/nested/subdir/upload_nested.txt).

### STDOUT:
[empty]

### STDERR:
upload_file.py ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
exit_code: 1
status_description: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
errors: [LocalFileNotFoundError]

**Known failure**: Test input file /home/uac-agent/ue-test-inputs/upload_test.txt does not exist on the remote agent host.
