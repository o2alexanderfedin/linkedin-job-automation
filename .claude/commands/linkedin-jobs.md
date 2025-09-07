---
allowed-tools: mcp__playwrite__browser_*, Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), TodoWrite(*), Task(*)
argument-hint: [free-text instructions with keywords, location, time, and target count]
description: Automated LinkedIn job search and application with comprehensive tracking
model: claude-3-5-sonnet-20241022
---

# LinkedIn Job Application Automation

Perform comprehensive LinkedIn job search and application automation with the following parameters:

**Instructions:** 
Parse the following free-text instructions to extract search parameters: $ARGUMENTS

**Default Parameters (if not specified in instructions):**
- Keywords: Extracted from candidate's resume (job titles, skills, seniority level)
- Location: Extracted from candidate's resume (current location, willing to relocate)
- Time Filter: "Past week"
- Target Count: 100 applications

**Resume Analysis:**
The system will automatically analyze the candidate's resume to determine:
- **Job Titles**: Current/target roles (e.g., "Principal Software Engineer", "Staff Engineer")
- **Skills**: Technical expertise for keyword matching (e.g., "AI/ML", "Cloud", "Python")
- **Seniority**: Experience level for appropriate role targeting
- **Location Preferences**: Current location and relocation willingness
- **Industry Focus**: Previous companies/sectors for targeted search

**Example Usage:**
- `/linkedin-jobs` (analyzes resume and uses intelligent defaults)
- `/linkedin-jobs Apply to 20 Staff Software Engineer jobs in California from the past 3 days`
- `/linkedin-jobs Find Principal Engineer positions in Seattle, apply to 50`
- `/linkedin-jobs AI/ML Engineer roles in New York area, target 30 applications this week`
- `/linkedin-jobs Senior Engineer remote positions, apply to 10 jobs posted yesterday`

**Smart Defaults Example:**
For a resume showing "Principal Software Engineer at Waymo" with "AI/ML, Python, C++" skills in "San Jose, CA", the system would default to searching for "Principal Software Engineer AI/ML" positions in "San Jose, CA" and nearby areas.

**Automation Process Flow:**

```mermaid
flowchart TD
    A["Analyze Resume & Extract Parameters <br/> Use resume-analyzer agent"] --> B[Open Browser]
    B --> C[Navigate to LinkedIn]
    C --> D["Login to LinkedIn <br/> Use linkedin-login agent"]
    D --> E["Search for Jobs <br/> Use linkedin-job-search agent"]
    E --> F{Jobs found?}
    F -->|No| G[End - no jobs found]
    F -->|Yes| H["Browse and Apply to Jobs <br/> Use Task tool with browse-apply-jobs.md command"]
    H --> I{"Applied to target count? <br/> Use application-tracker agent"}
    I -->|No| E
    I -->|Yes| J[End - Target reached]
```


**Key Features:**
- Uses Playwright MCP server exclusively for all browser interactions
- Human-like interaction patterns (delays, natural scrolling)
- Comprehensive job matching based on candidate profile
- Automatic resume upload and form completion
- Detailed application tracking and documentation
- Error handling and retry mechanisms
- Skip positions already applied to

**Documentation Format:**
Each application will be documented with:
- Position URL and title
- Company and location details
- Job description and key technologies
- Salary information when available
- Application timestamp and status
- Match reasoning based on qualifications

**Credential Handling:** Managed by linkedin-login agent with flexible source priority

Execute the full LinkedIn job application automation workflow with the specified search parameters.