> **Version:** aws-object-storage-showcase v1.0.0 | **Date:** 2026-10-09

# AWS Object Storage — Universal Extension User Guide

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Task Actions](#task-actions)
   - [List Objects](#list-objects)
   - [Upload File](#upload-file)
4. [Task Configuration](#task-configuration)
   - [Authentication](#authentication)
   - [Connection](#connection)
   - [Action-Specific Fields](#action-specific-fields)
5. [Example Walkthrough](#example-walkthrough)
   - [Scenario 1 — Audit bucket contents before a data pipeline run](#scenario-1--audit-bucket-contents-before-a-data-pipeline-run)
   - [Scenario 2 — Upload a nightly report to S3](#scenario-2--upload-a-nightly-report-to-s3)
6. [Troubleshooting](#troubleshooting)
7. [Field Reference](#field-reference)

---

## Overview

The **AWS Object Storage** Universal Extension enables Stonebranch Universal Controller tasks to interact with Amazon S3 buckets directly from the Universal Agent host. It supports two operations:

- **List Objects** — retrieve a paginated inventory of all objects in an S3 bucket.
- **Upload File** — push a local file from the agent host into a target S3 bucket at a specified object key.

Both operations authenticate using standard AWS IAM credentials and are suitable for use in automated workflows where S3 access is required.

---

## Prerequisites

- A running Universal Agent (v7.0.0.0 or later) with network access to the target AWS region endpoints.
- An AWS IAM user or role with appropriate S3 permissions:
  - `s3:ListBucket` — required for List Objects.
  - `s3:PutObject` — required for Upload File.
- An AWS credential record configured in Universal Controller (Access Key ID, Secret Access Key, and optionally a Session Token for temporary credentials).
- The target S3 bucket must already exist. This extension does not create buckets.
- For Upload File: the file to be uploaded must already exist on the Universal Agent host at the specified absolute path.

---

## Task Actions

### List Objects

**When to use:** Use this action to inventory the contents of an S3 bucket — for example, before a data pipeline to confirm expected inputs are present, or as part of an audit workflow.

**Execution flow:**

1. The extension validates that `AWS Region` and `Bucket Name` are provided.
2. An S3 client is created using the supplied credentials.
3. All objects are retrieved from the bucket using paginated `list_objects_v2` API calls.
4. Results are printed to the task output as a formatted table (Key, Size, Last Modified).
5. Output is capped at `UE_MAX_OUTPUT_RECORDS` rows (default: 100). If the bucket contains more objects, a truncation notice is appended to the output and a warning is written to STDERR.
6. The `Status` output field is set to `Found <N> objects`.
7. The `Object Count` output field is populated with the total number of objects.

**Completion behavior:** The task completes successfully (exit code 0) when the listing is retrieved. If the bucket is empty, the table will have no data rows and `Object Count` will be `0`.

**Optional environment variable:**

| Variable | Default | Description |
|---|---|---|
| `UE_MAX_OUTPUT_RECORDS` | `100` | Maximum number of objects to include in the task output table. Set to a larger value if the bucket contains many objects. |

---

### Upload File

**When to use:** Use this action to push files generated on the agent host (reports, exports, backups) into an S3 bucket as part of an automated workflow.

**Execution flow:**

1. The extension validates that `AWS Region`, `Bucket Name`, `Local File Path`, and `S3 Object Key` are all provided.
2. The extension verifies that the local file exists on disk at the specified path.
3. An S3 client is created using the supplied credentials.
4. The file is uploaded to `s3://<bucket>/<key>` using the boto3 `upload_file` method.
5. A confirmation line is printed to the task output: `Upload complete: <local_file> → s3://<bucket>/<key>`.
6. The `Status` output field is populated with `Uploaded <filename> → s3://<bucket>/<key>`.

**Completion behavior:** The task completes successfully (exit code 0) when the file upload is confirmed. If the file does not exist locally, the task fails before making any AWS call.

---

## Task Configuration

### Authentication

| Field | Description | Required |
|---|---|---|
| AWS Credentials | A UAC Credential record containing the AWS IAM Access Key ID (username), Secret Access Key (password), and an optional Session Token (token field) for temporary credentials. | Always |

### Connection

| Field | Description | Required |
|---|---|---|
| Action | Selects the S3 operation to perform: `List Objects` or `Upload File`. | Always |
| AWS Region | The AWS region identifier for the target bucket, e.g. `us-east-1`, `eu-west-1`. | Always |
| Bucket Name | The name of the target S3 bucket, e.g. `my-data-bucket`. | Always |

### Action-Specific Fields

These fields are only shown and required when **Action** is set to `Upload File`.

| Field | Description | Required |
|---|---|---|
| Local File Path | Absolute path on the Universal Agent host to the file to upload, e.g. `/tmp/report.csv`. | When Action = Upload File |
| S3 Object Key | The destination key (path) in the S3 bucket, e.g. `reports/2026/report.csv`. | When Action = Upload File |

---

## Example Walkthrough

### Scenario 1 — Audit bucket contents before a data pipeline run

**Goal:** Verify that an S3 bucket contains the expected number of objects before launching a downstream ETL job.

**Prerequisites:**

- A UAC Credential named `aws-prod-iam` with `s3:ListBucket` permission on `etl-inputs-prod`.
- A Universal Agent installed in the same network zone as the S3 endpoint.

**Configuration:**

| Field | Value | Notes |
|---|---|---|
| Action | List Objects | |
| AWS Credentials | `aws-prod-iam` | Select the credential from the UAC credential store |
| AWS Region | `us-east-1` | Match the region where the bucket resides |
| Bucket Name | `etl-inputs-prod` | |

**What happens:**

- The extension authenticates to S3 using the supplied IAM credentials.
- All objects in `etl-inputs-prod` are retrieved with full pagination.
- A table showing each object key, size, and last-modified timestamp is printed to the task output.
- The `Object Count` output field is set to the total number of objects found.
- If the bucket contains more than 100 objects, a truncation notice appears; set `UE_MAX_OUTPUT_RECORDS` on the agent to raise the display limit.
- The task exits with code `0` on success; downstream tasks can branch on the `Object Count` value.

---

### Scenario 2 — Upload a nightly report to S3

**Goal:** After a report generation job completes, push the output CSV to an S3 bucket for downstream consumption.

**Prerequisites:**

- A UAC Credential named `aws-reporting-iam` with `s3:PutObject` permission on `nightly-reports`.
- The report file is written to `/var/reports/nightly_summary.csv` on the Universal Agent host before this task runs.
- The target bucket `nightly-reports` already exists in `eu-west-1`.

**Configuration:**

| Field | Value | Notes |
|---|---|---|
| Action | Upload File | |
| AWS Credentials | `aws-reporting-iam` | |
| AWS Region | `eu-west-1` | |
| Bucket Name | `nightly-reports` | |
| Local File Path | `/var/reports/nightly_summary.csv` | Must exist on the agent host at task launch time |
| S3 Object Key | `reports/2026/10/09/nightly_summary.csv` | Adjust date path dynamically using UAC variables if needed |

**What happens:**

- The extension first confirms that `/var/reports/nightly_summary.csv` exists on the agent host; the task fails immediately if the file is absent.
- An S3 client is created and the file is uploaded to `s3://nightly-reports/reports/2026/10/09/nightly_summary.csv`.
- A confirmation message is printed to the task output.
- The `Status` output field is set to `Uploaded nightly_summary.csv → s3://nightly-reports/reports/2026/10/09/nightly_summary.csv`.
- The task exits with code `0` on success.

---

## Troubleshooting

### Authentication failure

**Symptom:** Task fails with status `Authentication failed` (exit code 1).

**Possible causes:**
- The Access Key ID or Secret Access Key stored in the UAC Credential is incorrect or has been rotated.
- A Session Token was provided but has expired (temporary credentials only).
- The IAM user has been deactivated or deleted.

**Resolution:**
- Verify the credentials in the UAC Credential record match the active IAM user keys in the AWS Console.
- If using temporary credentials (STS), regenerate and update the Session Token.
- Confirm the IAM user is active in AWS IAM.

---

### Access denied

**Symptom:** Task fails with status `Access denied` (exit code 1).

**Possible causes:**
- The IAM user lacks `s3:ListBucket` permission (List Objects) or `s3:PutObject` permission (Upload File) on the target bucket.
- An S3 bucket policy is blocking access from the IAM user.

**Resolution:**
- Review and update the IAM policy attached to the user to include the required S3 permissions.
- Check the bucket policy in the AWS S3 Console for any `Deny` statements that might override IAM allow rules.

---

### Bucket not found

**Symptom:** Task fails with status `Bucket not found` (exit code 1).

**Possible causes:**
- The bucket name in the `Bucket Name` field is misspelled.
- The bucket exists in a different AWS region than the one specified in `AWS Region`.
- The bucket has been deleted.

**Resolution:**
- Confirm the exact bucket name and region in the AWS S3 Console.
- Ensure the `AWS Region` field matches the bucket's actual region.

---

### Local file not found (Upload File only)

**Symptom:** Task fails with status `Local file not found` (exit code 1).

**Possible causes:**
- The path in `Local File Path` is incorrect or contains a typo.
- The file has not yet been generated when this task runs (dependency ordering issue).
- The file was placed on a different agent host than the one executing this task.

**Resolution:**
- Verify the absolute path and that the file exists on the agent host before this task runs.
- Add a dependency in the workflow to ensure the file-generating task completes before this task starts.
- Confirm the correct Universal Agent is assigned to this task.

---

### Validation error — missing required field

**Symptom:** Task fails with status `Validation Error` (exit code 20).

**Possible causes:**
- One of the required fields (`AWS Credentials`, `AWS Region`, `Bucket Name`) is empty.
- For Upload File: `Local File Path` or `S3 Object Key` is blank.

**Resolution:**
- Open the task definition and fill in all required fields.
- Note: exit code 20 indicates a user configuration error — UAC will not automatically retry the task.

---

### Output truncated (List Objects)

**Symptom:** The task output table shows fewer objects than expected, with a note: `Output truncated to N records`.

**Possible causes:**
- The bucket contains more objects than the `UE_MAX_OUTPUT_RECORDS` limit (default: 100).

**Resolution:**
- Set the `UE_MAX_OUTPUT_RECORDS` environment variable on the Universal Agent to a higher value (e.g. `1000`) to increase the display limit.
- The `Object Count` output field always reflects the true total, regardless of truncation.

---

### S3 service error

**Symptom:** Task fails with status `S3 error` (exit code 1).

**Possible causes:**
- A transient AWS service issue or network interruption.
- The AWS endpoint for the specified region is unreachable from the agent host.

**Resolution:**
- Review the full error message in the task output for additional details from the S3 API.
- Check AWS Service Health Dashboard for any active incidents in the target region.
- Verify the agent host has outbound HTTPS access to `s3.<region>.amazonaws.com`.

---

## Field Reference

| Field Name | Label | Type | Required | Description | Allowed Values |
|---|---|---|---|---|---|
| `action` | Action | Choice | No (defaults available) | Selects the S3 operation to perform. | `List Objects`, `Upload File` |
| `aws_credentials` | AWS Credentials | Credential | **Always** | AWS IAM credential record. Username = Access Key ID, Password = Secret Access Key, Token = Session Token (optional). | Any UAC Credential |
| `aws_region` | AWS Region | Text | **Always** | AWS region identifier for the target bucket. | e.g. `us-east-1`, `eu-west-1`, `ap-southeast-2` |
| `bucket_name` | Bucket Name | Text | **Always** | Name of the target S3 bucket. | Any valid S3 bucket name |
| `local_file` | Local File Path | Text | When Action = `Upload File` | Absolute path on the Universal Agent host to the file to upload. | e.g. `/tmp/report.csv` |
| `s3_object_key` | S3 Object Key | Text | When Action = `Upload File` | Destination object key (path) within the S3 bucket. | e.g. `reports/report.csv` |
| `status` | Status | Text (Output) | — | Human-readable summary of the action result, written after execution. | Read-only |
| `object_count` | Object Count | Text (Output) | — | Total number of objects found in the bucket. Populated by List Objects only. | Read-only |
