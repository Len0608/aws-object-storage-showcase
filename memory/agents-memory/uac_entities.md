# UAC Entities

**Extension:** aws-object-storage-showcase

---

## Agent Selection

### Available Agents

| Agent Name | Host | IP | Type | Status | Queue | Version |
|------------|------|----|------|--------|-------|---------|
| sb-agent-ubu - AGNT0012 | sb-agent-ubu | 127.0.1.1 | Linux/Unix | Active | AGNT0012 | 7.9.0.0 |
| integration-showcase-ua-56b6947d59-jbkdp - AGNT0151 | integration-showcase-ua-56b6947d59-jbkdp | 10.244.1.8 | Linux/Unix | Active | AGNT0151 | 8.0.1.0 |
| UDMG-SB | ip-172-31-2-26.us-east-2.compute.internal | 172.31.2.26 | Linux/Unix | Active | AGNT0118 | 7.9.2.0 |
| AGT_LINUX_PS1 | packaged-solutions-1 | 30.0.1.111 | Linux/Unix | Active | AGNT0009 | 8.0.0.0 |

### Selected Agent

| Field      | Value |
|------------|-------|
| Agent Name | sb-agent-ubu - AGNT0012 |
| Host Name  | sb-agent-ubu |
| IP Address | 127.0.1.1 |
| Type       | Linux/Unix |
| Status     | Active |
| Queue Name | AGNT0012 |
| Version    | 7.9.0.0 |
| SysID      | 360fb3ad9d0e41cb8530848d37831fe9 |

**Required OS Type:** Linux
**Selection rationale:** First active Linux/Unix agent returned by the controller agent list API. The extension targets Linux and does not require Windows.

---

## Required Entities

[Populated by test-graph-builder based on planned test scenarios]

### Credentials

| Credential Name | Type | Field Name | Auth Method | Used In Scenarios |
|----------------|------|------------|-------------|-------------------|
| aws-s3-test-creds | UAC (user/password) | aws_credentials | AWS IAM (Access Key ID + Secret Access Key) | All 10 scenarios |

### Scripts

| Script Name | Field Name | Used In Scenarios | Content |
|------------|------------|-------------------|---------|
| *(none)* | N/A | N/A | N/A |

---

## Update Guide

### aws-s3-test-creds
- **Login (user):** Set to the AWS IAM Access Key ID (e.g., `AKIAIOSFODNN7EXAMPLE`). Currently set to placeholder `test-placeholder-key`.
- **Password:** Set to the AWS IAM Secret Access Key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`). Currently set to placeholder `test-placeholder-secret`.
- **Token:** Leave empty unless using STS temporary credentials (session token).

---

## Created Entities

[Populated by main thread after creation on UAC]

### Credentials

| Credential Name | SysID | Status |
|----------------|-------|--------|
| | | |

### Scripts

| Script Name | SysID | Status |
|------------|-------|--------|
| | | |
