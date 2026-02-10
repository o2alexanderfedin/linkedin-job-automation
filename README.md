# LinkedIn Job Application Automation

Comprehensive Claude Code slash commands and agents for automated LinkedIn job searching and application submission.

## Features

🤖 **Intelligent Automation**
- Resume-driven job search parameters
- Human-like interaction patterns
- Comprehensive application tracking

🔒 **Secure Credential Management** 
- Environment variable storage (.env)
- No credential exposure in logs
- Secure local storage with proper permissions

📊 **Flexible Targeting**
- Natural language instructions
- Customizable application targets (default: 100 jobs)
- Adaptive search refinement

🎯 **Smart Matching**
- Skill-based job filtering
- Experience level targeting  
- Location preference handling

## Quick Start

### 1. Setup Credentials
```bash
/setup-job-credentials "your@email.com" "password" "(555)123-4567" "/path/to/resume.pdf" "Your City, ST" "Work Auth Status"
```

### 2. Run Job Automation
```bash
# Use intelligent defaults from resume
/linkedin-jobs

# Custom targeting
/linkedin-jobs Apply to 20 Staff Engineer jobs in California from past 3 days
```

### 3. Check Progress  
```bash
/job-status
```

## Commands

| Command | Purpose |
|---------|---------|
| `/linkedin-jobs` | Full automation: search, analyze, and apply |
| `/apply-job [url]` | Apply to specific LinkedIn job posting |
| `/search-jobs` | Search and analyze without applying |
| `/setup-job-credentials` | Configure secure credential storage |
| `/job-status` | Display application statistics |
| `/job-help` | Show all available commands |

## Architecture

### Slash Commands
- **Natural language interface** for job automation
- **Resume-driven defaults** with custom override options
- **Mermaid flow diagrams** define precise execution paths

### Claude Code Agents
- **Declarative goal-based design** for adaptability
- **Playwright MCP server integration** for browser automation
- **Security-first credential handling**

## Security

- Credentials stored in `.env` with 600 permissions
- No sensitive data in git repository
- Privacy-focused application tracking
- Secure browser automation patterns

## Requirements

- Claude Code CLI
- Playwright MCP server
- LinkedIn account with valid credentials
- Resume file (PDF/DOC format)

---

*Built with Claude Code for intelligent, secure, and efficient job application automation.*