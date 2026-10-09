## Issue: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Status**: ✗ Failed

### Expected:
List objects in S3 bucket `ue-test-aws-object-storage-2026` using List Objects action with IAM credentials.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:10:15,446 - extension.py[63] INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:10:15,446 - extension.py[70] INFO: Action requested: List Objects
2026-10-09 12:10:15,446 - extension.py[76] INFO: Executing action: List Objects
2026-10-09 12:10:15,446 - list_objects.py[44] INFO: Starting list_objects action
2026-10-09 12:10:15,446 - list_objects.py[56] INFO: Validating input fields
2026-10-09 12:10:15,446 - list_objects.py[95] INFO: Creating S3 client
2026-10-09 12:10:15,446 - utility.py[64] INFO: Creating S3 client for region: us-east-1
2026-10-09 12:10:15,520 - utility.py[79] INFO: S3 client created successfully
2026-10-09 12:10:15,520 - list_objects.py[105] INFO: Listing objects in bucket: ue-test-aws-object-storage-2026
2026-10-09 12:10:15,520 - utility.py[112] INFO: Listing all objects in bucket: ue-test-aws-object-storage-2026
2026-10-09 12:10:15,867 - utility.py[208] ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:10:15,867 - extension.py[90] ERROR: Execution error: S3 error: The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:10:15,885 - extension_start_result.py[221] ERROR: Error in extension: /var/opt/universal/uag/extensions/.aws-object-storage-showcase/extension.py:187 - S3 error: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{
  "exit_code": 1,
  "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.",
  "metadata": {
    "version": "1.0.0",
    "extension": "aws-object-storage-showcase"
  },
  "input_fields": {
    "action": ["List Objects"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-object-storage-2026",
    "local_file": "",
    "s3_object_key": ""
  },
  "result": {},
  "errors": [{"type": "S3ServiceError", "message": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]
}

**Note**: Failure is due to placeholder AWS credentials. The extension executed correctly and reached the S3 API call.
