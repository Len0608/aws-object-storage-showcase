<!-- generated: 2026-10-09 00:00 -->
# Features Analysis — Universal Extension v1.0.0

## Purpose
Provides Stonebranch Universal Controller tasks for interacting with AWS S3 object storage, supporting listing bucket objects and uploading local files from the Universal Agent host.

## Execution Modes / Actions

| Mode | Trigger | Description |
|---|---|---|
| List Objects | `input_data.action.value == "List Objects"` | Lists all objects in the specified S3 bucket; respects `UE_MAX_OUTPUT_RECORDS` env var to cap output rows |
| Upload File | `input_data.action.value == "Upload File"` | Uploads a local file from the agent host to an S3 bucket at a specified object key |

Dispatch mechanism: `ACTION_MAPPER.get(input_data.action.value)` in `extension.py:execute()`, where `ACTION_MAPPER` maps string choice values to action functions.

## Function List

- `create_s3_client` (utility.py) — creates a boto3 S3 client from access key credentials and region
- `list_all_objects` (utility.py) — paginates through all S3 objects in a bucket and returns a structured list
- `upload_file` (utility.py) — verifies local file existence then delegates to boto3 upload_file
- `_raise_from_client_error` (utility.py) — maps boto3 ClientError error codes to typed custom exceptions and raises
- `list_objects` (actions/list_objects.py) — validates required fields, invokes utility functions, builds ActionOutput
- `upload_file` (actions/upload_file.py) — validates required fields, checks local file exists, invokes utility functions, builds ActionOutput

## Error Handling

| Scope | Error | Handling |
|---|---|---|
| `extension.py:execute()` | `ExecutionError` (base for all typed errors) | Caught; logged; added to ExtensionManager errors; returns `build_result` with `exit_code=e.exit_code` and `status_description=e.message` |
| `extension.py:execute()` | Any unhandled `Exception` | Wrapped in `UnexpectedSystemError`; added to ExtensionManager; returns `build_result` with that error's exit code and message |
| `actions/upload_file.py` | Missing `aws_region`, `bucket_name`, `local_file`, `s3_object_key` | Raises `ValidationError` with field name; caught upstream as `ExecutionError` |
| `actions/upload_file.py` | Local file path not found on agent host | Raises `LocalFileNotFoundError(local_file)` |
| `actions/list_objects.py` | Missing `aws_region` or `bucket_name` | Raises `ValidationError` with field name |
| `actions/list_objects.py` | `UE_MAX_OUTPUT_RECORDS` not parseable as int | `ValueError` caught locally; logs warning and falls back to default value |
| `utility.py:list_all_objects()` | `botocore.exceptions.ClientError` | Caught; delegated to `_raise_from_client_error` |
| `utility.py:upload_file()` | `botocore.exceptions.ClientError` | Caught; delegated to `_raise_from_client_error` |
| `utility.py:_raise_from_client_error()` | Auth error codes (`InvalidClientTokenId`, etc.) | Raises `AuthenticationError` |
| `utility.py:_raise_from_client_error()` | `NoSuchBucket` | Raises `BucketNotFoundError(bucket_name)` |
| `utility.py:_raise_from_client_error()` | Access denied codes | Raises `AccessDeniedError` |
| `utility.py:_raise_from_client_error()` | Any other ClientError | Raises `S3ServiceError` |
