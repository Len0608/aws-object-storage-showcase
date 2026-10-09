🌐 EXTERNAL SERVICE SETUP: Amazon S3

BEFORE RUNNING TESTS, CREATE THE FOLLOWING ON THE EXTERNAL SERVICE:

1. AWS IAM User with Programmatic Access
   - What: An AWS IAM user (or role) whose access key credentials will be used by the extension
   - Why: The extension authenticates all S3 API calls using an Access Key ID and Secret Access Key supplied via a UAC Credential field. Without valid IAM credentials, every test will fail with an authentication error.
   - How:
     1. Log in to the AWS Management Console → IAM → Users → Create user
     2. Select "Provide user access to the AWS Management Console" → No (programmatic only)
     3. On the Permissions step, attach the following inline or managed policy:
        ```json
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "s3:ListBucket",
                "s3:PutObject"
              ],
              "Resource": [
                "arn:aws:s3:::YOUR_TEST_BUCKET_NAME",
                "arn:aws:s3:::YOUR_TEST_BUCKET_NAME/*"
              ]
            }
          ]
        }
        ```
     4. Complete user creation, then go to the user → Security credentials → Create access key
     5. Select "Application running outside AWS" → create key
     6. Record the Access Key ID and Secret Access Key — the secret is shown only once
   - Example: Access Key ID `AKIAIOSFODNN7EXAMPLE`, Secret Access Key `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

2. S3 Test Bucket
   - What: An Amazon S3 bucket that the extension will list objects from and upload files to during tests
   - Why: Both the List Objects and Upload File actions require a pre-existing bucket. The extension does not create buckets; it will raise a BucketNotFoundError if the bucket does not exist.
   - How:
     1. In the AWS Management Console → S3 → Create bucket
     2. Choose a globally unique name (e.g., `ue-test-aws-object-storage-2026`)
     3. Select the AWS region you will use in test task fields (e.g., `us-east-1`)
     4. Leave Block Public Access settings at their defaults (all blocked)
     5. Complete bucket creation
   - Example: bucket name `ue-test-aws-object-storage-2026` in region `us-east-1`

3. At Least One Object in the Test Bucket
   - What: One or more objects pre-uploaded into the test bucket so that List Objects tests return non-empty results
   - Why: The List Objects action fetches `Contents` from each page. An empty bucket is a valid edge case, but functional tests should also verify non-empty listings. Pre-seeding objects ensures meaningful table output is validated.
   - How:
     1. In the AWS Management Console → S3 → select your test bucket → Upload
     2. Upload any small file (e.g., a text file)
     3. Alternatively, use the AWS CLI:
        ```bash
        echo "test seed file" > seed.txt
        aws s3 cp seed.txt s3://ue-test-aws-object-storage-2026/seed/seed.txt
        ```
   - Example: object key `seed/seed.txt`, size ~15 bytes

4. UAC Credential Entity — AWS Credentials
   - What: A UAC Credential record that stores the IAM Access Key ID in the `user` field and the Secret Access Key in the `password` field
   - Why: The extension's `aws_credentials` field is a UAC Credential type. The extension reads `input_data.aws_credentials.user` as the Access Key ID and `input_data.aws_credentials.password` as the Secret Access Key. A missing or misconfigured credential causes a runtime crash or authentication failure.
   - How:
     1. In UAC → Credentials → Create Credential
     2. Set Credential Type to "UAC" (generic username/password)
     3. Set Login (user) to: the AWS Access Key ID from step 1
     4. Set Password to: the AWS Secret Access Key from step 1
     5. Leave Token (runtime token) empty unless using STS temporary credentials
     6. Save with a recognisable name such as `aws-s3-test-creds`
   - Example:
     - Name: `aws-s3-test-creds`
     - Login: `AKIAIOSFODNN7EXAMPLE`
     - Password: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

---

🖥️ AGENT HOST SETUP

BEFORE RUNNING TESTS, PREPARE THE FOLLOWING ON THE UAC AGENT MACHINE:

1. Local Test File for Upload File Action
   - What: A small file placed at a known absolute path on the UAC Agent host, referenced by the `local_file` field in Upload File test tasks
   - Why: The Upload File action checks that the file exists at `input_data.local_file` before creating the S3 client. If the path does not exist, the task fails immediately with a LocalFileNotFoundError. A pre-created file is required for Upload File positive tests to pass.
   - How: Log in to the UAC Agent host (or run the following via a UAC Script task targeting that agent) and execute:
     ```bash
     mkdir -p ~/ue-test-inputs
     echo "UAC upload test file" > ~/ue-test-inputs/upload_test.txt
     ```
   - Example:
     - Path: `~/ue-test-inputs/upload_test.txt`
     - Content: `UAC upload test file`
   - Use this absolute path as the value of the `local_file` field in Upload File test tasks. Resolve `~` to the agent user's home directory (e.g., `/home/uac-agent/ue-test-inputs/upload_test.txt`).

---

📋 CHECKLIST:

  ☐ AWS IAM user created with Access Key ID and Secret Access Key recorded
  ☐ IAM policy grants s3:ListBucket and s3:PutObject on the test bucket
  ☐ S3 test bucket created in target region (e.g., us-east-1)
  ☐ At least one seed object uploaded into the test bucket
  ☐ UAC Credential entity created with IAM Access Key ID (login) and Secret Access Key (password)
  ☐ Local test file created on the UAC Agent host at a known absolute path
  ☐ Verified: UAC Agent can reach `https://s3.<region>.amazonaws.com` over HTTPS (port 443)
