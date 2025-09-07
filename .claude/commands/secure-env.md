---
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
description: Secure the .env file and ensure it's not committed to git
---

# Secure Environment File

Ensure your .env file containing LinkedIn credentials is properly secured:

**Security Actions:**
1. **Set File Permissions**: Restrict .env to owner-only access (600)
2. **Git Ignore Setup**: Add .env to .gitignore if not already present  
3. **Verify Security**: Check current permissions and git status
4. **Remove from Git**: If .env was accidentally committed, remove it from git history

**Process:**
1. Check if .env file exists and display current permissions
2. Set secure permissions (600 - owner read/write only)
3. Verify .gitignore contains .env entry
4. Add .env to .gitignore if missing
5. Check if .env is currently tracked by git
6. If tracked, provide instructions to remove from git history

**Security Verification:**
```bash
# Check .env file permissions (should show -rw-------)
ls -la .env

# Verify .env is ignored by git (should show no output)
git check-ignore .env

# Confirm .env is not in git status (should not appear)
git status --ignored
```

**Git History Cleanup (if needed):**
If .env was accidentally committed, provides commands to:
- Remove from current commit
- Clean from git history 
- Force push if necessary (with warnings)

**Error Handling & Diagnostics:**
- **System Errors**: Invoke diagnostic-fix-agent for file permission setting failures, git repository access errors, or .gitignore modification issues
- **Workflow Failures**: Use diagnostic-fix-agent when security verification fails repeatedly, git history cleanup errors occur, or file system operations fail
- **Unexpected Behavior**: Call diagnostic-fix-agent for unexpected git repository states, .env file access errors, or permission verification failures

Secure your LinkedIn credentials and prevent accidental exposure in version control.