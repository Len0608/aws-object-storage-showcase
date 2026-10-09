# AWS Object Storage - Implementation Analysis

**Extension Name:** *AWS Object Storage (aws-object-storage-showcase)*
**Universal Template Name:** *Aws Object Storage Showcase*
**Target Platform:** Linux

---

## Extension Overview

The AWS Object Storage extension provides a minimal, demo-grade integration between Stonebranch UAC and Amazon S3. It enables UAC tasks to list objects stored in an S3 bucket and upload a local file from the Universal Agent host to a specified bucket. Authentication uses explicit IAM credentials supplied through a UAC Credential field. The implementation is intentionally simple, with no retry logic, no dynamic choice fields, no progress reporting, and no custom cancellation handling.

---

# Template Fields

## 1. Input Fields

**action**
- **Type**: Choice Field (Single-select)
- **Visible When**: always
- **Required When**: always
- **Options**:
  - *List Objects* — Retrieves and lists all objects in the specified S3 bucket
  - *Upload File* — Uploads a local file from the Universal Agent host to the specified S3 bucket
- **Default Value**: List Objects
- **Validation**:
  - Must be one of the defined options
- **Purpose**: Selects which S3 operation the extension will perform; drives conditional visibility of Upload File Parameters fields

---

**aws_credentials**
- **Type**: Credential Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must reference a valid UAC Credential entity
  - The `user` attribute must contain the AWS Access Key ID
  - The `password` attribute must contain the AWS Secret Access Key
  - The `token` attribute is optional; when populated it is used as the AWS Session Token for temporary STS credentials
- **Purpose**: Supplies AWS IAM credentials used to authenticate all S3 API calls. Mapped as: `user` → Access Key ID, `password` → Secret Access Key, `token` → Session Token (passed as `None` when empty)

---

**aws_region**
- **Type**: Text Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must be a non-empty string
  - Must be a valid AWS region identifier format (e.g., lowercase alphanumeric with hyphens)
- **Purpose**: Specifies the AWS regional S3 endpoint the extension connects to
- **Example**: `us-east-1`

---

**bucket_name**
- **Type**: Text Field
- **Visible When**: always
- **Required When**: always
- **Validation**:
  - Must be a non-empty string
- **Purpose**: Specifies the target AWS S3 bucket for the selected action
- **Example**: `my-demo-bucket`

---

**local_file**
- **Type**: Text Field
- **Visible When**: action value is equal to "Upload File". It is required when it's visible.
- **Required When**: action value is equal to "Upload File"
- **Validation**:
  - Must be a non-empty string
  - Must be an absolute path
- **Purpose**: The absolute path on the Universal Agent host to the local file that will be uploaded to S3
- **Example**: `/tmp/report.csv`

---

**s3_object_key**
- **Type**: Text Field
- **Visible When**: action value is equal to "Upload File". It is required when it's visible.
- **Required When**: action value is equal to "Upload File"
- **Validation**:
  - Must be a non-empty string
- **Purpose**: The destination key (path and filename) under which the uploaded file will be stored in the S3 bucket
- **Example**: `reports/report.csv`

---

## 2. Output Fields

**status**
- **Type**: Text Output
- **Purpose**: Short human-readable summary of the action result, displayed in the UAC task list view
- **Examples**: `"Found 42 objects"`, `"Uploaded report.csv → s3://my-bucket/reports/report.csv"`, `"Authentication failed: Invalid credentials"`, `"Bucket not found: my-demo-bucket"`

---

**object_count**
- **Type**: Text Output
- **Visible When**: action is "List Objects"
- **Purpose**: The total number of objects found in the bucket during a List Objects execution (before any STDOUT truncation is applied)
- **Examples**: `"42"`, `"0"`, `"350"`

---

## 3. Field Ordering

The task form uses a **2-column grid layout**.

**Field Order (Visual Layout):**

```
┌─────────────────────────────────────────┐
│                  action                 │  ← Full-width
├─────────────────────────────────────────┤
│             aws_credentials             │  ← Full-width (credential)
├─────────────────────────────────────────┤
│     aws_region      │   bucket_name     │  ← Half-width pair
├─────────────────────┼───────────────────┤
│               local_file                │  ← Full-width (Upload File only)
├─────────────────────────────────────────┤
│              s3_object_key              │  ← Full-width (Upload File only)
├─────────────────────────────────────────┤
│                  status                 │  ← Full-width (Output Only)
├─────────────────────────────────────────┤
│              object_count               │  ← Full-width (Output Only)
└─────────────────────────────────────────┘
```

---

# Actions

## Action 1: List Objects

**Description**: Retrieves all objects stored in the specified S3 bucket using the `list_objects_v2` API with full pagination support. Displays results as a `rounded_outline` formatted table in STDOUT, capped at `UE_MAX_OUTPUT_RECORDS`. Populates the Status and Object Count output fields and returns a structured Extension Output JSON.

### Input Requirements

- **action** (value: "List Objects")
- **aws_credentials**
- **aws_region**
- **bucket_name**

### Execution Flow

**Step 1: Input Validation**
- Verify `aws_region` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: aws_region is required"`
- Verify `bucket_name` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: bucket_name is required"`

**Step 2: Read Environment Configuration**
- Read `UE_MAX_OUTPUT_RECORDS` from the process environment
- If the variable is not set or cannot be parsed as a positive integer, use the default value `100`

**Step 3: Create S3 Client**
- Map credentials: `access_key_id = input_data.aws_credentials.user`, `secret_access_key = input_data.aws_credentials.password`, `session_token = input_data.aws_credentials.token` (use `None` if token attribute is empty or None)
- Instantiate a boto3 S3 client with the mapped credentials and `region_name = input_data.aws_region`

**Step 4: List All Objects with Pagination**
- Use a boto3 S3 paginator for `list_objects_v2` with `Bucket = input_data.bucket_name`
- Iterate through all pages and collect all objects from the `Contents` key of each page response
- For each object, extract: `key` (string, from S3 object Key), `size` (integer bytes, from S3 object Size), `last_modified` (ISO 8601 timestamp string, from S3 object LastModified converted to UTC ISO format)
- If a page has no `Contents` key (empty bucket), treat as zero objects
- Record the total object count `N` as the count of all collected objects

**Step 5: Apply Output Cap**
- Determine `truncated = (N > max_records)` where `max_records` is the value from Step 2
- Produce `display_objects = all_objects[:max_records]` (the subset written to STDOUT and Extension Output)

**Step 6: Write STDOUT Table**
- Format `display_objects` as a `rounded_outline` table using tabulate with columns: `Key`, `Size (bytes)`, `Last Modified`
- Print the table to STDOUT
- If `truncated` is True, append the following note on a new line after the table:
  `[Note: Output truncated to {max_records} records (total: {N} objects). Set UE_MAX_OUTPUT_RECORDS to adjust the limit.]`

**Step 7: Write STDERR Warning (if truncated)**
- If `truncated` is True, write to STDERR:
  `WARNING: Output truncated. Bucket contains {N} objects; display limited to {max_records} by UE_MAX_OUTPUT_RECORDS.`

**Step 8: Populate Output Fields**
- Set `output_data.status = f"Found {N} objects"`
- Set `output_data.object_count = str(N)`

**Step 9: Return Result**
- Set status_description to `f"Found {N} objects"`
- Return Extension Output JSON with `result` object (see Output Examples below)
- Return exit code `0`

### Output Examples

**STDOUT** (non-truncated, 2 objects):
```
╭──────────────────────┬───────────────┬──────────────────────────╮
│ Key                  │   Size (bytes) │ Last Modified            │
├──────────────────────┼───────────────┼──────────────────────────┤
│ reports/report.csv   │          1024 │ 2026-10-09T10:00:00Z     │
│ data/file.txt        │           512 │ 2026-10-08T08:30:00Z     │
╰──────────────────────┴───────────────┴──────────────────────────╯
```

**STDOUT** (truncated — 350 objects, cap of 100):
```
╭─ ... table rows up to 100 ... ─╮
[Note: Output truncated to 100 records (total: 350 objects). Set UE_MAX_OUTPUT_RECORDS to adjust the limit.]
```

**Extension Output result object (JSON)**:

```json
{
  "result": {
    "bucket": "my-bucket",
    "count": 42,
    "truncated": false,
    "objects": [
      {"key": "reports/report.csv", "size": 1024, "last_modified": "2026-10-09T10:00:00Z"},
      {"key": "data/file.txt", "size": 512, "last_modified": "2026-10-08T08:30:00Z"}
    ]
  }
}
```

Note: The Extension Output also includes `exit_code`, `status_description`, and `invocation` elements added automatically at implementation time. The `objects` array is capped at `UE_MAX_OUTPUT_RECORDS` entries; `count` always reflects the total number of objects in the bucket regardless of the cap; `truncated` is `true` when the array was capped.

### Success Criteria
1. The `list_objects_v2` S3 API call completes without error (all paginated pages fetched)
2. STDOUT contains the `rounded_outline` formatted table with object data (Key, Size, Last Modified)
3. When output is truncated, a note appears in STDOUT and a warning appears in STDERR
4. Output fields `status` and `object_count` are populated with the correct values
5. Extension Output JSON is returned with the correct structure including `bucket`, `count`, `truncated`, and `objects`
6. Exit code is `0`

---

## Action 2: Upload File

**Description**: Uploads a specified local file from the Universal Agent host filesystem to a specified S3 bucket and object key. Returns a confirmation in STDOUT, populates the Status output field, and returns a structured Extension Output JSON.

### Input Requirements

- **action** (value: "Upload File")
- **aws_credentials**
- **aws_region**
- **bucket_name**
- **local_file**
- **s3_object_key**

### Execution Flow

**Step 1: Input Validation**
- Verify `aws_region` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: aws_region is required"`
- Verify `bucket_name` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: bucket_name is required"`
- Verify `local_file` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: local_file is required"`
- Verify `s3_object_key` is non-empty; if empty, raise a ValidationError with status description `"Validation Error: s3_object_key is required"`

**Step 2: Verify Local File Exists**
- Check that the file at `input_data.local_file` exists on the Agent filesystem
- If the file does not exist, raise a LocalFileNotFoundError immediately (before creating the S3 client) with status description `"Local file not found: {input_data.local_file}"`

**Step 3: Create S3 Client**
- Map credentials: `access_key_id = input_data.aws_credentials.user`, `secret_access_key = input_data.aws_credentials.password`, `session_token = input_data.aws_credentials.token` (use `None` if token is empty or None)
- Instantiate a boto3 S3 client with the mapped credentials and `region_name = input_data.aws_region`

**Step 4: Upload File**
- Call boto3 S3 client `upload_file(Filename=input_data.local_file, Bucket=input_data.bucket_name, Key=input_data.s3_object_key)`
- This call raises a boto3 `ClientError` on failure (authentication, access denied, bucket not found, etc.) which is handled in the exception mapping

**Step 5: Write STDOUT Confirmation**
- Print to STDOUT: `Upload complete: {input_data.local_file} → s3://{input_data.bucket_name}/{input_data.s3_object_key}`

**Step 6: Populate Output Fields**
- Derive `filename = os.path.basename(input_data.local_file)`
- Set `output_data.status = f"Uploaded {filename} → s3://{input_data.bucket_name}/{input_data.s3_object_key}"`

**Step 7: Return Result**
- Set status_description to `f"Uploaded {filename} → s3://{input_data.bucket_name}/{input_data.s3_object_key}"`
- Return Extension Output JSON with `result` object (see Output Examples below)
- Return exit code `0`

### Output Examples

**STDOUT**:
```
Upload complete: /tmp/report.csv → s3://my-bucket/reports/report.csv
```

**Extension Output result object (JSON)**:

```json
{
  "result": {
    "bucket": "my-bucket",
    "key": "reports/report.csv",
    "local_file": "/tmp/report.csv"
  }
}
```

Note: The Extension Output also includes `exit_code`, `status_description`, and `invocation` elements added automatically at implementation time.

### Success Criteria
1. The file transfer to S3 completes without error
2. STDOUT contains the upload confirmation message
3. Output field `status` is populated with the upload confirmation
4. Extension Output JSON is returned with the correct structure (`bucket`, `key`, `local_file`)
5. Exit code is `0`

---

# Progress Reporting

Progress Reporting (percentage of completion report) is not required. Neither the List Objects nor the Upload File action involves a measurable multi-step operation suitable for progress percentage reporting.

---

# Dynamic Choice Field Population

No Dynamic choice fields should be implemented. The extension does not use any fields whose options are populated at runtime from an external service or dynamic computation.

---

# Cancellation Behavior

Default cancellation logic is used (TERM signal). No custom cancellation implementation is required. When UAC sends a Cancel command, the default SIGTERM signal terminates the running Python process. No cleanup of S3 operations or temporary files is required because: the List Objects action performs read-only API calls, and the Upload File action does not use temporary files.

---

# Re-Run Behavior

Re-runs are treated as initial executions. No output-only fields are used to persist identifiers or state that would alter re-run behavior. Each re-run will perform the full action from scratch using the current input field values.

---

# Dynamic Commands

No Dynamic commands should be implemented. The extension has no operations that need to be triggered interactively against a running task instance.

---

# Utility Modules

## Required Utility Modules

### 1. S3 Client Manager

**Purpose:** Creates an authenticated boto3 S3 client from InputFields credential values and provides thin wrapper methods for the two required S3 operations (list all objects with pagination, upload a local file).

**Required Capabilities:**

**Client Initialization:**
- Accept AWS Access Key ID, Secret Access Key, Session Token (optional, `None` when absent), and Region as inputs
- Instantiate and return a configured boto3 S3 client

**List All Objects (with pagination):**
- Accept bucket name as input
- Use the S3 paginator for `list_objects_v2` to iterate through all pages
- Collect all object records from the `Contents` key of each page; treat missing `Contents` (empty bucket) as zero objects
- For each object record, extract and return: `key` (str), `size` (int, bytes), `last_modified` (ISO 8601 UTC string formatted as `YYYY-MM-DDTHH:MM:SSZ`)
- Return the complete list of object records and the total count

**Upload File:**
- Accept local file path, bucket name, and S3 object key as inputs
- Delegate directly to the boto3 S3 client `upload_file` method
- Propagate any `ClientError` raised by boto3 without wrapping (handled by the exception mapping layer)

**Used By:** List Objects action, Upload File action

---

## Exception Mapping Strategy

All exception handling maps boto3 and filesystem errors to custom extension exceptions with the status description patterns required by the requirements.

**AWS ClientError (boto3.exceptions.ClientError) — by error code:**
- `AuthFailure`, `InvalidClientTokenId`, `UnrecognizedClientException`, `ExpiredTokenException` → `AuthenticationError` (exit code 1, non-transient user config error); status description: `"Authentication failed: {error_message}"`
- `NoSuchBucket` → `BucketNotFoundError` (exit code 1, non-transient user config error); status description: `"Bucket not found: {input_data.bucket_name}"`
- `AccessDenied`, `AllAccessDisabled` → `AccessDeniedError` (exit code 1, non-transient user config error); status description: `"Access denied: {error_message}"`
- All other `ClientError` codes → `S3ServiceError` (exit code 1, potentially transient); status description: `"S3 error: {error_message}"`

**Local Filesystem Errors:**
- `FileNotFoundError` when checking or accessing the local file path → `LocalFileNotFoundError` (exit code 1, non-transient user input error); status description: `"Local file not found: {input_data.local_file}"`

**Input Validation Errors:**
- Any required field that fails the validation checks in Step 1 of each action → `ValidationError` (exit code 20); status description as defined in each action's validation step

**Extension Output on Error (all error scenarios):**
```json
{
  "error": {
    "message": "<status description text>"
  }
}
```

**Exit Code Guide:**
- Exit code `0`: Successful execution
- Exit code `1`: Operational failure (authentication, S3 API error, bucket not found, access denied, local file not found) — non-transient
- Exit code `20`: Input validation error (missing or invalid required field values)

---

# Dependencies

## 1. External API Dependencies

**1. Amazon S3 (Simple Storage Service)**
- **Endpoint**: `https://s3.{region}.amazonaws.com` (resolved automatically by boto3 from the configured region)
- **Purpose**: Object listing (`list_objects_v2`) and file upload (`put_object` via `upload_file`) operations
- **Protocol**: HTTPS
- **Method**: S3 API calls via boto3 (internally HTTP GET for listing, HTTP PUT for upload)
- **Authentication**: AWS IAM — Access Key ID + Secret Access Key + optional Session Token supplied via boto3 client constructor
- **Response Format**: Parsed by boto3; returned to extension as Python dictionaries
- **Data Retrieved/Sent**: Object metadata (Key, Size, LastModified) for list; raw file bytes for upload

**General API Requirements:**
- AWS account with IAM credentials that have at minimum `s3:ListBucket` permission for List Objects and `s3:PutObject` permission for Upload File
- No additional subscription or activation steps beyond standard AWS account access

---

## 2. Python version dependency

Python `>= 3.11` as configured in the extension environment.

---

## 3. Target Platform

Linux (x86_64). The Universal Agent runs on a Linux server. C extension modules with a confirmed `manylinux_2_17_x86_64` wheel are viable in addition to pure-Python modules.

---

## 4. Python Library Dependencies

**1. boto3**
- **Purpose**: AWS SDK for Python — provides the S3 client with `list_objects_v2` (via paginator) and `upload_file` operations
- **Version**: `1.43.110`
- **Installation**: `pip install boto3==1.43.110`
- **Usage**: Used in the S3 Client Manager utility to create the S3 client and execute all S3 API calls
- **Features Used**: `boto3.client('s3', ...)`, S3 paginator for `list_objects_v2`, `s3_client.upload_file(...)`

**2. botocore**
- **Purpose**: Required transitive dependency of boto3; provides the low-level AWS request/response handling and `ClientError` exception class
- **Version**: `1.43.110`
- **Installation**: `pip install botocore==1.43.110`
- **Usage**: `botocore.exceptions.ClientError` is caught in exception handling for all S3 API error responses
- **Features Used**: `ClientError` exception, error code extraction via `e.response['Error']['Code']`

**3. tabulate**
- **Purpose**: Formats the list of S3 objects as a clean `rounded_outline` ASCII table for STDOUT display in the List Objects action
- **Version**: `0.10.0`
- **Installation**: `pip install tabulate==0.10.0`
- **Usage**: Used in the List Objects action to format `display_objects` as a table
- **Features Used**: `tabulate(rows, headers=["Key", "Size (bytes)", "Last Modified"], tablefmt="rounded_outline")`

---

## 5. Python Standard Library Dependencies

**1. os**
- **Purpose**: Filesystem path operations
- **Version**: Standard library (Python 3.11+)
- **Installation**: Built-in — no installation required
- **Usage**: `os.path.basename(local_file)` in Upload File action to derive the filename for the status description; `os.path.exists(local_file)` for local file existence check in Upload File action

**2. os.environ**
- **Purpose**: Reads the `UE_MAX_OUTPUT_RECORDS` environment variable in the List Objects action
- **Version**: Standard library (Python 3.11+)
- **Installation**: Built-in — no installation required
- **Usage**: `os.environ.get("UE_MAX_OUTPUT_RECORDS", "100")` with integer parsing and fallback to default 100

---

## 6. CLI Tool Dependencies

No Dependencies. The extension uses boto3 SDK calls exclusively and does not invoke any CLI tools.

---

## 7. Environment Variables

**`UE_MAX_OUTPUT_RECORDS`** (*integer*, *optional*):
- **Purpose**: Caps the number of S3 object records written to STDOUT and included in the Extension Output `objects` array for the List Objects action. Protects against large bucket listings that could bloat the UAC database or exceed Universal Agent output limits.
- **Default**: `100` when not set or not parseable as a positive integer
- **Usage**: Read at the start of the List Objects action execution (Step 2). Applied to both the STDOUT table row count and the `objects` array length in Extension Output.
- **Examples**: `UE_MAX_OUTPUT_RECORDS=50`, `UE_MAX_OUTPUT_RECORDS=200`
