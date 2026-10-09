<!-- generated: 2026-10-09 00:00 -->
# Fields Analysis — Universal Extension v1.0.0

> Note: `fields.yml` (the canonical Universal Extension fields file) is empty. All field definitions are sourced from `src/templates/template.json` (templateType: "Extension"). The table below follows the Universal Template column schema.

## Complete Field Table

| name | label | fieldType | required | requireIfVisible | choices | showIfField | showIfFieldValue | requireIfField | requireIfFieldValue | hint |
|---|---|---|---|---|---|---|---|---|---|---|
| action | Action | Choice | false | false | List Objects, Upload File | — | — | — | — | Select the S3 operation to perform |
| aws_credentials | AWS Credentials | Credential | true | false | — | — | — | — | — | AWS IAM credentials: user=Access Key ID, password=Secret Access Key, token=Session Token (optional) |
| aws_region | AWS Region | Text | true | false | — | — | — | — | — | AWS region identifier, e.g. us-east-1 |
| bucket_name | Bucket Name | Text | true | false | — | — | — | — | — | Target S3 bucket name, e.g. my-demo-bucket |
| local_file | Local File Path | Text | false | true | — | Choice Field 1 | Upload File | — | — | Absolute path on the agent host to the local file to upload, e.g. /tmp/report.csv |
| s3_object_key | S3 Object Key | Text | false | true | — | Choice Field 1 | Upload File | — | — | Destination key in the S3 bucket, e.g. reports/report.csv |
| status | Status | Text (Output Only) | false | false | — | — | — | — | — | Short human-readable summary of the action result |
| object_count | Object Count | Text (Output Only) | false | false | — | — | — | — | — | Total number of objects found in the bucket (List Objects action only) |

## Cross-references

### Always-required fields
- `aws_credentials` — AWS IAM credential, always required
- `aws_region` — AWS region, always required
- `bucket_name` — S3 bucket name, always required

### Conditionally-required fields (requireIfVisible)
- `local_file` — required when visible (shown only when action = "Upload File")
- `s3_object_key` — required when visible (shown only when action = "Upload File")

### Field visibility dependencies (showIfField)
- `local_file` → shown when `Choice Field 1` (action) = `"Upload File"`
- `s3_object_key` → shown when `Choice Field 1` (action) = `"Upload File"`

### Mutually exclusive options
- `action` drives two mutually exclusive operation modes:
  - `"List Objects"` — `local_file` and `s3_object_key` are hidden; `object_count` output field is populated
  - `"Upload File"` — `local_file` and `s3_object_key` are shown and required; `object_count` is not applicable
