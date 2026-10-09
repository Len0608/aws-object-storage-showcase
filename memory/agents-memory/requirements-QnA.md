# Requirements Completeness Assessment

**Level: Moderate Detail**

The requirements set a clear and well-focused foundation: AWS S3 integration using boto3, two concrete actions (List Objects and Upload File), a named credential field, and a small set of explicitly listed fields. The MVP/demo intent is well-expressed and scopes the work effectively.

A few key decisions still need to be shaped together:
- Which Python modules to bundle alongside boto3 (specifically, whether to use `tabulate` for readable STDOUT output)
- How AWS Access Key ID and Secret Access Key map to UAC credential attributes (wrong mapping causes a runtime crash)
- Which object metadata to display in the List Objects STDOUT output, and how to protect against large bucket listings
- What output-only fields to expose in UAC's task list view and what structure the Extension Output JSON should take

---

# Platform Compatibility

**Platform Compatibility from Requirements**: Linux — confirmed from `environment.md` (Build Platform: OS: Linux, Architecture: x86_64); requirements also reference "the Linux server where the Universal Agent is installed"

**Platform Compatibility Agreement**: Linux-only

---

# Python Modules and Versions

## Researched Modules

**boto3**
- **Module Purpose**: AWS SDK for Python — provides the S3 client with `list_objects_v2`, `upload_file`, and all related S3 operations; handles credential resolution, request signing, and retry logic
- **Version**: 1.43.110
- **Type**: Pure Python

**botocore**
- **Module Purpose**: Core AWS service client layer; required transitive dependency of boto3 providing low-level API calls, credential chain resolution, serialization, and error handling — must be pinned to the same version as boto3
- **Version**: 1.43.110
- **Type**: Pure Python

**tabulate**
- **Module Purpose**: Formats list/dict data as clean ASCII/Unicode tables for STDOUT display; the architect notes specifically recommend `tablefmt="rounded_outline"` for well-formatted output
- **Version**: 0.10.0
- **Type**: Pure Python

## Agreed Python Modules and Versions

| Module Name | Module Purpose | Version | Type |
|---|---|---|---|
| [Placeholder — to be updated after question answers are finalized] | | | |

---

# Question Rationale

These 4 questions address the critical open decisions in the requirements: Python module selection (boto3 version confirmation and tabulate for STDOUT), AWS credential attribute mapping (wrong mapping causes runtime crashes), List Objects STDOUT design and large-bucket safety, and the UAC output fields plus Extension Output JSON structure. All other elements — the two actions, field names, SDK choice, and MVP scope — are explicitly defined in the requirements and require no clarification.

---

# Clarifying Questions for Requirements Refinement

## Critical Decision Path Questions

**Question 1**: Which Python modules should be bundled with the extension?

`boto3` is specified in the requirements and confirmed as pure-Python with full compatibility on the Linux build platform. The architect notes recommend ASCII table formatting for STDOUT output when data can be presented in rows and columns — `tabulate` is the standard module for this, is pure-Python, is specifically referenced in the architect notes, and produces the clean `rounded_outline` table style in a single function call.

- **Options**:
  - **O1**: `boto3==1.43.110`, `botocore==1.43.110`, `tabulate==0.10.0` — full table-formatted STDOUT for the List Objects action
  - **O2**: `boto3==1.43.110`, `botocore==1.43.110` only — plain-text STDOUT (no table formatting)

- **Question Type**: New Discussion topic
- **Context & Resources**:
  - [boto3 PyPI](https://pypi.org/project/boto3/) — AWS SDK, pure-Python
  - [tabulate PyPI](https://pypi.org/project/tabulate/) — well-maintained, pure-Python, 0 C dependencies
  - Architect notes: *"ASCII Table format is preferable when information can be printed nicely in rows or in columns using well known python libraries"*; *"Use `tablefmt="rounded_outline"` as it provides a really nice output"*
  - All three modules are pure-Python: no manylinux wheel concerns, fully compatible with the Linux build platform
  - `botocore` must always be pinned to the same version number as `boto3` — they share synchronized versioning
- **Question Dependencies**: None
- **Recommended Answer**: O1 — Include `tabulate` for table-formatted STDOUT. A well-formatted table of S3 objects significantly improves the demo impact and adds only ~1 line of code per column definition.
- **Rationale**: tabulate produces a visually clean `rounded_outline` table in a single function call with no complexity cost; important for a demo integration where output impression matters
- **Trade-offs**: O1 adds one more entry in `requirements.txt` but produces a much more readable STDOUT; O2 is marginally simpler but produces plain-text output that is harder to read in a demo context
- **Requirement Impact**: None
- **User's Answer**: O1

---

## Authentication & Security Questions

**Question 2**: How should AWS credentials be mapped to UAC credential attributes?

The AWS SDK requires an Access Key ID and a Secret Access Key for programmatic authentication. UAC Credential entities have four attributes: `user`, `password`, `token`, and `passphrase`. A clear, documented mapping is essential so task operators know exactly which attribute to populate for each AWS credential value — and so extension code reads from the correct attribute (wrong attribute access causes an AttributeError at runtime).

The recommended mapping follows UAC's convention that `user` holds a non-sensitive identifier and `password` holds the corresponding secret:

| UAC Credential Attribute | AWS Credential Value | Notes |
|---|---|---|
| `user` | AWS Access Key ID | Always required; non-sensitive identifier |
| `password` | AWS Secret Access Key | The corresponding secret |
| `token` | AWS Session Token | Optional — used with temporary STS credentials |

- **Options**:
  - **O1**: `user` = AWS Access Key ID, `password` = AWS Secret Access Key, `token` = AWS Session Token (optional — passes `None` to boto3 when not provided, which boto3 handles gracefully)
  - **O2**: `user` = AWS Access Key ID, `password` = AWS Secret Access Key only (Session Token not supported)

- **Question Type**: New Discussion topic
- **Context & Resources**:
  - [boto3 Credentials Guide](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html) — boto3 accepts `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token` when constructing an S3 client
  - AWS Session Tokens are issued when assuming IAM roles or using AWS SSO — common in enterprise AWS environments; passing `None` as the session token when not needed is supported and safe
  - UAC architect notes: *"`user` attribute is always mandatory for the definition of a credential entity, even though it might not be used for the business logic"*; *"DO: Map API keys to `password` attribute"*; *"DON'T: Use `user` attribute for sensitive information"*
- **Question Dependencies**: None
- **Recommended Answer**: O1 — Map `user`=Access Key ID, `password`=Secret Access Key, `token`=Session Token (optional). Supporting session token via the `token` attribute adds zero extra code (boto3 accepts `None` silently) while making the extension compatible with temporary credential workflows common in enterprise AWS.
- **Rationale**: The `token` attribute is natively available on UAC credentials; using it costs nothing and enables the extension to work in IAM Role / STS-based environments without future modification
- **Trade-offs**: O2 is slightly simpler to document (two attributes vs. three) but would require rework later for organizations using role-based AWS authentication; O1 future-proofs the credential design at no implementation cost
- **Requirement Impact**: None — the credential field is already specified in requirements; this only defines which UAC credential attribute holds which AWS value
- **User's Answer**: O1

---

## Essential Input/Output Questions

**Question 3**: What object metadata should the List Objects action display in STDOUT, and how should large bucket listings be handled?

The List Objects action retrieves objects from a specified S3 bucket. S3 objects carry several metadata attributes (Key, Size, Last Modified, ETag, Storage Class). For STDOUT, a table with selected columns is most readable. For safety, the architect notes strongly recommend capping the number of records written to STDOUT using the `UE_MAX_OUTPUT_RECORDS` environment variable (default: 100) — especially important because S3 buckets can contain thousands or millions of objects, and writing all of them to STDOUT would bloat the UAC database and risk hitting Universal Agent output limits.

When truncation occurs, a note should appear in STDOUT and a warning in STDERR indicating the total object count and the applied limit.

- **Options for object attributes to display**:
  - **O1**: Key, Size (bytes), Last Modified — the three most useful attributes for a demo; size and timestamp add meaningful context without clutter
  - **O2**: Key only — minimal output, absolute simplest implementation
  - **O3**: Key, Size, Last Modified, ETag, Storage Class — a comprehensive view of common S3 metadata

- **Options for large output cap**:
  - **A**: Cap STDOUT listing at `UE_MAX_OUTPUT_RECORDS` (environment variable, default: 100); include a truncation note in STDOUT and a warning on STDERR when the limit is applied
  - **B**: No cap — list all objects (acceptable only when the target bucket is guaranteed to remain small)

- **Question Type**: New Discussion topic
- **Context & Resources**:
  - [boto3 list_objects_v2 reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html) — returns up to 1,000 objects per API page; pagination is handled via `NextContinuationToken`
  - Architect notes — *Large Output Safety Net Pattern*: *"Use environment variable `UE_MAX_OUTPUT_RECORDS` to cap the number of records written to STDOUT or Extension Output; Default to `100` records if the environment variable is not set"*; *"When the output is truncated, include a note in STDOUT, a warning on STDERR"*
  - Without a cap, running the extension against a production S3 bucket with 50,000 objects would send all 50,000 rows to the UAC database
- **Question Dependencies**: None
- **Recommended Answer**: O1 + A — Display Key, Size (bytes), and Last Modified in a `rounded_outline` table; cap STDOUT at `UE_MAX_OUTPUT_RECORDS` (default: 100) with truncation notification in STDOUT and STDERR.
- **Rationale**: Key + Size + Last Modified provides a useful and visually appealing snapshot for a demo while keeping the table compact; the cap is essential for safe operation against real-world S3 buckets
- **Trade-offs**: O1+A adds ~10 lines of cap logic but is safe for any bucket; O2+B is the absolute minimum but risks problems when pointed at a real or growing S3 bucket
- **Requirement Impact**: None — within MVP scope; the environment variable approach is operator-configurable without code changes
- **User's Answer**: O1 + A

---

**Question 4**: What output-only fields should appear in the UAC task list view, and what should the Extension Output JSON contain?

After a task instance reaches its terminal state, UAC displays output-only fields in the task list grid — giving operators immediate at-a-glance information without opening the task. The Extension Output (machine-readable JSON) is also returned and can be consumed by downstream workflow tasks.

For the List Objects action, the number of objects found is highly informative at a glance. For Upload File, a brief confirmation is the key result. The Extension Output should carry the key result data for any potential downstream automation — even at MVP level.

- **Options for UAC output-only fields**:
  - **O1**: One field — `Status` (short success/failure summary for both actions; e.g. `"Found 42 objects"` / `"Uploaded report.csv → s3://my-bucket/reports/report.csv"`)
  - **O2**: Two fields — `Status` + `Object Count` (List Objects shows the number of objects found; Upload File shows `"1 file uploaded"`)

- **Options for Extension Output JSON structure**:
  - **A**: Structured per-action result:
    - List Objects: `{"result": {"bucket": "my-bucket", "count": 42, "truncated": false, "objects": [{"key": "...", "size": 1024, "last_modified": "2026-10-09T10:00:00Z"}, ...]}}`
    - Upload File: `{"result": {"bucket": "my-bucket", "key": "reports/report.csv", "local_file": "/tmp/report.csv"}}`
  - **B**: Minimal for both actions: `{"result": {"status": "success", "action": "list_objects"}}`

- **Question Type**: New Discussion topic
- **Context & Resources**:
  - Architect notes: *"2-3 fields are suitable for most cases. Choose the most important information to be displayed for best User Experience"*; *"Do not store large Information on Output Only fields. Use short information directly visible and understood by users"*
  - Architect notes: *"Always provide an Extension Output"*; *"Enclose output information in a `result` object"*; *"In case of failure scenarios it is recommended to use an `error` object to include metadata and description about the error"*
  - For List Objects Extension Output, the same `UE_MAX_OUTPUT_RECORDS` cap from Q3 applies to the `objects` array — preventing the JSON blob from becoming excessively large
  - Fields marked `defaultListView: true` appear in the UAC task instance list grid, providing immediate visibility for operators
- **Question Dependencies**: Answer to Q3 (O1+A) informs the `objects` array structure in the List Objects Extension Output
- **Recommended Answer**: O2 + A — Two output fields (Status + Object Count) with structured per-action Extension Output JSON. The Object Count field provides strong visual impact in the UAC task list for a demo; the structured JSON makes the extension immediately useful for automation workflows.
- **Rationale**: Two fields are minimal but give the demo meaningful at-a-glance information in the UAC grid; structured JSON enables downstream workflow integration and makes the MVP useful beyond pure demonstration
- **Trade-offs**: O1+B is the absolute simplest implementation; O2+A adds modest code for field population but significantly improves both the demo experience and the downstream usability of the extension
- **Requirement Impact**: None
- **User's Answer**: O2 + A
