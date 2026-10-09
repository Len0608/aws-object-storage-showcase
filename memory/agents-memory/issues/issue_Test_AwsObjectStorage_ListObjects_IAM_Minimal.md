## Issue: Test_AwsObjectStorage_ListObjects_IAM_Minimal

**Status**: ✗ Failed

### Expected:
List of objects returned from S3 bucket "ue-test-aws-object-storage-2026" with IAM credentials.

### STDOUT:
[empty]

### STDERR:
2026-10-09 12:21:58,514 - extension.py[63] INFO: aws-object-storage-showcase v1.0.0 started
2026-10-09 12:21:58,514 - extension.py[70] INFO: Action requested: List Objects
2026-10-09 12:21:58,515 - list_objects.py[95] INFO: Creating S3 client
2026-10-09 12:21:58,591 - utility.py[79] INFO: S3 client created successfully
2026-10-09 12:21:58,591 - list_objects.py[105] INFO: Listing objects in bucket: ue-test-aws-object-storage-2026
2026-10-09 12:21:58,926 - utility.py[208] ERROR: S3 ClientError: code=InvalidAccessKeyId, message=The AWS Access Key Id you provided does not exist in our records.
2026-10-09 12:21:58,926 - extension.py[90] ERROR: Execution error: S3 error: The AWS Access Key Id you provided does not exist in our records.

### Extension Output:
{
  "exit_code": 1,
  "status_description": "S3 error: The AWS Access Key Id you provided does not exist in our records.",
  "input_fields": {
    "action": ["List Objects"],
    "aws_credentials": {"user": "test-placeholder-key", "password": "****", "token": "", "passphrase": ""},
    "aws_region": "us-east-1",
    "bucket_name": "ue-test-aws-object-storage-2026",
    "local_file": "",
    "s3_object_key": ""
  },
  "errors": [{"type": "S3ServiceError", "message": "S3 error: The AWS Access Key Id you provided does not exist in our records.", "exit_code": 1}]
}
