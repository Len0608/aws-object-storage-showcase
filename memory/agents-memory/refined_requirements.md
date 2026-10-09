# Universal Extension Requirements (Refined)

**Extension Name:** AWS Object Storage  
**Original Generated:** 2026-10-09  
**Refined:** 2026-10-09 12:00:00  
**Agent_id:** N/A  
**Requirements Completeness:** High Detail  
**Target Platform:** Linux  

---

# Table of Contents

1. [Overview](#overview)
2. [Actions](#actions)
   - 2.1 [List Objects](#21-list-objects)
   - 2.2 [Upload File](#22-upload-file)
3. [Input Requirements](#input-requirements)
   - 3.1 [Connection Parameters](#31-connection-parameters)
   - 3.2 [Action Selection](#32-action-selection)
   - 3.3 [Upload File Parameters](#33-upload-file-parameters)
4. [Output Requirements](#output-requirements)
   - 4.1 [List Objects — On Success](#41-list-objects--on-success)
   - 4.2 [Upload File — On Success](#42-upload-file--on-success)
   - 4.3 [On Error](#43-on-error)
5. [Authentication Requirements](#authentication-requirements)
6. [Environment Variables](#environment-variables)
7. [Operational Behavior](#operational-behavior)
8. [Implementation Notes](#implementation-notes)
   - 8.1 [Python Compatibility](#81-python-compatibility)
   - 8.2 [Target Platform](#82-target-platform)
   - 8.3 [Third-Party Services and Tools](#83-third-party-services-and-tools)
   - 8.4 [Error Handling](#84-error-handling)
   - 8.5 [Resource Cleanup](#85-resource-cleanup)
9. [Requirements Summary](#requirements-summary)
10. [Document Change History](#document-change-history)
11. [References](#references)

---

# Overview

This document defines the requirements for the **AWS Object Storage** Universal Extension for Stonebranch Universal Automation Center (UAC).

**Integration Purpose:** The extension provides an MVP/demo AWS S3 integration that enables UAC tasks to list objects in an S3 bucket and upload a local file from the Universal Agent host to a specified S3 bucket. The purpose is to demonstrate that AWS S3 integration can be implemented with Stonebranch. The implementation must remain as simple as possible and avoid unnecessary advanced features.

---

# Actions

## 2.1 List Objects

**Functional Requirements:**

1. The extension must retrieve and list objects stored in a specified AWS S3 bucket using the `list_objects_v2` API.
2. The STDOUT output must present results as a formatted table with the following columns: Key, Size (bytes), and Last Modified.
3. The table must use the `rounded_outline` format.
4. The number of records written to STDOUT must be capped at the value of the `UE_MAX_OUTPUT_RECORDS` environment variable (default: 100 when the variable is not set).
5. When the result is truncated due to the `UE_MAX_OUTPUT_RECORDS` cap, a truncation note must appear in STDOUT and a warning must be written to STDERR, both indicating the total object count and the applied limit.
6. The UAC output-only field **Status** must be populated with a short success summary (e.g., `"Found 42 objects"`).
7. The UAC output-only field **Object Count** must be populated with the total number of objects found in the bucket.
8. The Extension Output JSON must be returned in the structured format defined in [Section 4.1](#41-list-objects--on-success).

## 2.2 Upload File

**Functional Requirements:**

1. The extension must upload a specified local file from the Universal Agent host to a specified AWS S3 bucket and S3 object key.
2. The UAC output-only field **Status** must be populated with a short success summary (e.g., `"Uploaded report.csv → s3://my-bucket/reports/report.csv"`).
3. The Extension Output JSON must be returned in the structured format defined in [Section 4.2](#42-upload-file--on-success).

---

# Input Requirements

## 3.1 Connection Parameters

- **AWS Credentials** (Credential field, required): A UAC Credential entity holding the AWS authentication values used to connect to the S3 service. Required for all actions.
  - Example: A UAC Credential named `aws-prod-credentials`
  - Applicability: All actions
  - Default Value: None

- **AWS Region** (Text field, required): The AWS region identifier specifying which regional S3 endpoint the extension must connect to.
  - Example: `us-east-1`
  - Applicability: All actions
  - Default Value: None

- **Bucket Name** (Text field, required): The name of the target AWS S3 bucket.
  - Example: `my-demo-bucket`
  - Applicability: All actions
  - Default Value: None

## 3.2 Action Selection

- **Action** (Choice field, required): Selects which operation the extension must perform.
  - Available options:
    - `List Objects` — Retrieves and lists objects in the specified S3 bucket
    - `Upload File` — Uploads a local file to the specified S3 bucket
  - Default presented option: `List Objects`
  - Applicability: All actions
  - Behavior: Selecting `Upload File` must show the Upload File Parameters fields ([Section 3.3](#33-upload-file-parameters)); selecting `List Objects` must hide those fields.

## 3.3 Upload File Parameters

These fields are shown only when the Action field is set to `Upload File`.

- **Local File** (Text field, required when Action = Upload File): The absolute path to the local file on the Universal Agent host that must be uploaded to S3.
  - Example: `/tmp/report.csv`
  - Applicability: Upload File action only
  - Default Value: None

- **S3 Object Key** (Text field, required when Action = Upload File): The destination key (path and filename) under which the file must be stored in the S3 bucket.
  - Example: `reports/report.csv`
  - Applicability: Upload File action only
  - Default Value: None

---

# Output Requirements

## 4.1 List Objects — On Success

- **Return code:** 0
- **Status description:** `"Found <N> objects"` where `<N>` is the total number of objects found in the bucket
- **Output-only fields:**
  - `Status` (Text): Short human-readable summary. Example: `"Found 42 objects"`
  - `Object Count` (Text): Total number of objects found. Example: `"42"`
- **Extension Output (JSON):**
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
  - `bucket`: The name of the S3 bucket queried
  - `count`: Total number of objects found (before any STDOUT cap is applied)
  - `truncated`: Boolean indicating whether the `objects` array was truncated due to `UE_MAX_OUTPUT_RECORDS`
  - `objects`: Array of object records; each record contains `key` (string), `size` (integer, bytes), and `last_modified` (ISO 8601 timestamp string). The array must also be capped at `UE_MAX_OUTPUT_RECORDS`.
- **STDOUT output:** `rounded_outline` formatted table with columns Key, Size (bytes), and Last Modified. When truncated, a note must appear below the table indicating the total count and the applied limit.
- **STDERR output:** When truncation occurs, a warning must be written to STDERR indicating the total object count and the applied `UE_MAX_OUTPUT_RECORDS` limit.
- **Success Criteria:**
  1. The S3 API call completes without error
  2. STDOUT contains the formatted table with object data
  3. Extension Output JSON is returned with the correct structure
  4. Output-only fields Status and Object Count are populated

## 4.2 Upload File — On Success

- **Return code:** 0
- **Status description:** `"Uploaded <filename> → s3://<bucket>/<key>"` where `<filename>` is the base name of the local file
- **Output-only fields:**
  - `Status` (Text): Short human-readable upload confirmation. Example: `"Uploaded report.csv → s3://my-bucket/reports/report.csv"`
- **Extension Output (JSON):**
  ```json
  {
    "result": {
      "bucket": "my-bucket",
      "key": "reports/report.csv",
      "local_file": "/tmp/report.csv"
    }
  }
  ```
  - `bucket`: The name of the S3 bucket the file was uploaded to
  - `key`: The S3 object key under which the file was stored
  - `local_file`: The absolute path of the local file that was uploaded
- **STDOUT output:** A confirmation message indicating the upload completed successfully
- **Success Criteria:**
  1. The file transfer to S3 completes without error
  2. Extension Output JSON is returned with the correct structure
  3. Output-only field Status is populated

## 4.3 On Error

- **Failure Scenarios:**

  | Scenario | Description | Root Causes | Return Code | Status Description Pattern |
  |---|---|---|---|---|
  | Authentication Failure | AWS credentials are invalid or expired | Incorrect Access Key ID, Secret Access Key, or Session Token | Non-zero | `"Authentication failed: <error message>"` |
  | Bucket Not Found | The specified S3 bucket does not exist or is inaccessible | Bucket name is wrong or in a different region | Non-zero | `"Bucket not found: <bucket name>"` |
  | Access Denied | The credentials lack required S3 permissions | IAM policy does not allow the requested action | Non-zero | `"Access denied: <error message>"` |
  | Local File Not Found | The specified local file does not exist on the agent host | Invalid path or file deleted before execution | Non-zero | `"Local file not found: <path>"` |
  | S3 Service Error | An unexpected error is returned by the S3 API | AWS service outage, network issue, or misconfiguration | Non-zero | `"S3 error: <error message>"` |

- **Extension Output on Error:**
  ```json
  {
    "error": {
      "message": "<error description>"
    }
  }
  ```

- **Input Validation:** Input fields validation is required.

---

# Authentication Requirements

The extension must authenticate to AWS S3 using explicit IAM credentials supplied through a UAC Credential field. The UAC Credential attributes must be mapped to AWS credential values as follows:

| UAC Credential Attribute | AWS Credential Value | Requirement |
|---|---|---|
| `user` | AWS Access Key ID | Required |
| `password` | AWS Secret Access Key | Required |
| `token` | AWS Session Token | Optional — used with temporary STS credentials; must be passed as `None` when not populated |

The `token` attribute must be supported to enable compatibility with temporary credential workflows (e.g., IAM Role assumption via AWS STS). When the `token` attribute is empty, the extension must pass `None` to the AWS SDK, which accepts this value gracefully.

---

# Environment Variables

- **`UE_MAX_OUTPUT_RECORDS`**: Integer. Caps the number of object records written to STDOUT and included in the Extension Output `objects` array for the List Objects action. Default: `100` when the variable is not set. Used to protect against large bucket listings that could bloat the UAC database or exceed Universal Agent output limits.

---

# Operational Behavior

**Dynamic Choice Fields:**  
Not applicable. The extension does not use dynamic choice fields populated at runtime.

**Cancel Action:**  
Not specified.

**Re-run Capability:**  
Not specified.

**Progress Reporting:**  
Not specified.

**Dynamic Commands:**  
Not applicable.

---

# Implementation Notes

## 8.1 Python Compatibility

Python `>= 3.11` (as specified in the extension environment configuration).

## 8.2 Target Platform

Linux only (x86_64). The Universal Agent is installed on a Linux server, confirmed by the workspace build platform (OS: Linux, Architecture: x86_64). C-extension modules with a confirmed `manylinux_2_17_x86_64` wheel are viable in addition to pure-Python modules.

## 8.3 Third-Party Services and Tools

**AWS S3 (Amazon Simple Storage Service)**
- Short Description: AWS object storage service used for listing and uploading objects
- Version constraints: No specific API version constraint; integration targets the current S3 API via boto3
- Integration approach: Programmatic access via the boto3 Python SDK using IAM credentials

**Python Dependencies to Bundle**

All dependencies must be bundled with the extension ZIP so that nothing needs to be installed separately on the Universal Agent.

| Module | Version | Type | Purpose |
|---|---|---|---|
| `boto3` | 1.43.110 | Pure Python | AWS SDK — provides the S3 client with `list_objects_v2`, `upload_file`, and all related S3 operations |
| `botocore` | 1.43.110 | Pure Python | Required transitive dependency of boto3; must be pinned to the same version |
| `tabulate` | 0.10.0 | Pure Python | Formats list data as clean `rounded_outline` ASCII tables for STDOUT display |

## 8.4 Error Handling

- **Error categories:** Authentication errors, S3 service errors (bucket not found, access denied), local file errors (file not found), and general S3 API errors
- **Error handling strategy:** Errors must be caught and reported with a descriptive message. On failure, the extension must return a non-zero return code, populate the Status output field with an error summary, and return an Extension Output JSON with an `error` object containing the error description.
- **Recovery mechanisms:** None specified. The extension does not implement retry logic.

## 8.5 Resource Cleanup

- **Cleanup scenarios:** Not specified.
- **Strategy:** Not specified.

---

# Requirements Summary

The AWS Object Storage Universal Extension provides a minimal, demo-grade AWS S3 integration for Stonebranch UAC with two actions:

1. **List Objects** — retrieves S3 object listings (Key, Size, Last Modified) from a specified bucket, displayed as a `rounded_outline` table in STDOUT, capped at `UE_MAX_OUTPUT_RECORDS` (default 100), with two UAC output fields (Status, Object Count) and structured Extension Output JSON.
2. **Upload File** — uploads a local file from the Universal Agent host to a specified S3 bucket and object key, with a confirmation Status output field and structured Extension Output JSON.

Authentication uses a UAC Credential with `user`=Access Key ID, `password`=Secret Access Key, and optional `token`=Session Token. Dependencies (boto3==1.43.110, botocore==1.43.110, tabulate==0.10.0) must be fully bundled. The target platform is Linux (x86_64) and the implementation must remain simple and free of unnecessary advanced features.

---

# Document Change History

- **2026-10-09**: Initial requirements — Moderate Detail. Two actions defined (List Objects, Upload File), core fields specified, MVP/demo scope established.
- **2026-10-09 12:00:00**: Comprehensive refinement based on 4 clarification questions and user feedback. Added: Python module selection and versions (boto3, botocore, tabulate), credential attribute mapping (user/password/token), List Objects STDOUT column selection (Key, Size, Last Modified) and large-bucket cap behavior (UE_MAX_OUTPUT_RECORDS), and UAC output field definitions (Status + Object Count) with structured Extension Output JSON for both actions.

---

# References

- Original Requirements Document: `memory/requirements.md`
- Original Requirements Q&A Document: `memory/agents-memory/requirements-QnA.md`
