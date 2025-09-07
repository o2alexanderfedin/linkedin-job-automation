---
allowed-tools: Write(*), Read(*), Edit(*), TodoWrite(*), Bash(*)
argument-hint: [email] [password] [phone] [resume-path] [location] [work-auth]
description: Set up or update job application credentials for LinkedIn automation
---

# Setup Job Application Credentials

Configure credentials for LinkedIn job application automation:

**Arguments:**
- **Email**: $1 - Your contact email for job applications and linkedin login
- **Password**: $2 - Your password for linkedin
- **Phone**: $3 - Your phone number  
- **Resume Path**: $4 - Full path to your resume file
- **Location**: $5 - Your current location (City, State ZIP)
- **Work Authorization**: $6 - Your work authorization status

**Process:**
- Use TodoWrite tool to plan complete credential setup workflow
- Mark tasks in_progress before execution, completed after success
- Revise todo list if validation fails or file operations encounter issues
1. Validate provided credentials and paths
2. Check if resume file exists at specified path
3. Save credentials securely to .env file in current directory
4. Create backup of existing .env if it exists
5. Set secure file permissions and verify setup
6. Display summary of configured credentials (without showing password)

**Setup Planning:**
- Create initial todo list covering: validate inputs → backup existing .env → create new .env → set permissions → verify setup
- Adapt plan if file validation fails or security setup encounters errors
- Track progress through credential configuration for transparency and error recovery

**Environment Variables Created:**
- `LINKEDIN_EMAIL` - Login email
- `LINKEDIN_PASSWORD` - Login password (securely stored)
- `JOB_PHONE` - Contact phone number
- `JOB_RESUME_PATH` - Full path to resume file
- `JOB_LOCATION` - Current location
- `JOB_WORK_AUTH` - Work authorization status

**Example Usage:**
```
/setup-job-credentials "john.doe@email.com" "mypassword123" "(555)123-4567" "/Users/john/resume.pdf" "Austin, TX 78701" "US Citizen"
```

**Supported Work Authorization Types:**
- "US Citizen"
- "Green Card holder" 
- "H1B"
- "OPT"
- "L1"
- "TN Visa"
- Custom status (provide your specific status)

**Security Notes:**
- .env file is created with restricted permissions (600 - owner read/write only)
- Credentials are stored locally and never transmitted except to LinkedIn
- Add .env to your .gitignore to prevent accidental commits
- Backup existing .env file before overwriting

**Output:**
- Creates .env file with all job application credentials
- Other LinkedIn job commands automatically read from .env
- Eliminates need to provide credentials each time
- Validates resume file exists at specified path

**Usage by Other Commands:**
Once configured, all other job application commands (`/linkedin-jobs`, `/apply-job`, etc.) will automatically use the credentials from the .env file, falling back to command arguments if .env values are not found.

**Implementation Steps:**

1. **Validate Arguments**: Check all provided credentials and paths
```bash
# Validate email format
# Check if resume file exists at $4 path
# Validate phone number format
# Verify location format
```

2. **Backup Existing .env**: If .env exists, create backup
```bash
# Create .env.backup with timestamp if .env exists
```

3. **Create .env File**: Write credentials to .env with proper security
```bash
# Set file permissions to 600 (owner read/write only)
# Write environment variables in proper format
```

4. **Verify Setup**: Test file creation and credential accessibility
```bash
# Read back .env values to confirm they were written correctly
# Display summary without showing sensitive information
```

## Task Execution Rules

**SEQUENTIAL EXECUTION REQUIRED** - All Task tool calls must run sequentially due to file dependencies:

1. **Input Validation** → **Backup Creation** (validation must complete before backup)
2. **Backup Creation** → **Credential Writing** (backup must exist before overwriting)
3. **Credential Writing** → **Permission Setting** (file must exist before setting permissions)
4. **Permission Setting** → **Verification** (permissions must be set before verification)

**Never run Task tool calls in parallel** - Each file operation depends on the previous step's completion.

Configure your job application credentials for seamless LinkedIn automation with secure local storage.