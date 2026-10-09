## Issue: Test_AwsObjectStorage_UploadFile_IAM_Minimal

**Status**: ✗ Failed

### Expected:
File uploaded to S3 bucket "ue-test-aws-object-storage-2026" at key "test/upload_minimal.txt" using IAM credentials.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:19:25,497 - 128885270222528 AsyEvent[EXTENSION_START] - extension.py[63] INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - extension.py[70] INFO: Action requested: Upload File
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - extension.py[76] INFO: Executing action: Upload File
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - upload_file.py[41] INFO: Starting upload_file action
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - upload_file.py[55] INFO: Validating input fields
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - upload_file.py[78] INFO: Verifying local file exists: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - upload_file.py[80] ERROR: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:19:25,498 - 128885270222528 AsyEvent[EXTENSION_START] - extension.py[90] ERROR: Execution error: Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt
2026-10-09 12:19:25,515 - 128885270222528 AsyEvent[EXTENSION_START] - extension_start_result.py[221] ERROR: Error in extension: /var/opt/universal/uag/extensions/.aws-object-storage-showcase/extension.py:187 - Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt

### Extension Output:
{
  "exit_code": 1,
  "status_description": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
  "metadata": {
    "version": "1.0.0",
    "extension": "aws-object-storage-showcase"
  },
  "input_fields": {
    "action": ["Upload File"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-object-storage-2026",
    "local_file": "/home/uac-agent/ue-test-inputs/upload_test.txt",
    "s3_object_key": "test/upload_minimal.txt"
  },
  "result": {},
  "errors": [
    {
      "type": "LocalFileNotFoundError",
      "message": "Local file not found: /home/uac-agent/ue-test-inputs/upload_test.txt",
      "exit_code": 1
    }
  ]
}
