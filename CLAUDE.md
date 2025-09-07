# LinkedIn Job Automation - Claude Code Architecture

## Project Overview

This project implements comprehensive LinkedIn job application automation using Claude Code's agent-based architecture. The system consists of specialized agents that work together in a coordinated workflow to analyze resumes, search for jobs, and submit applications automatically.

## Architectural Principles

### 1. Agent-Based Architecture
- **Specialized Agents**: Each agent has a single, focused responsibility
- **Clear Boundaries**: Agents communicate through well-defined interfaces
- **Autonomous Operation**: Each agent can operate independently within its domain
- **Composable Workflow**: Agents combine to form complex automation workflows

### 2. Data Flow Architecture
- **Sequential Processing**: Data flows through agents in a defined sequence
- **Context Preservation**: Complete context is passed between workflow stages
- **Immutable Handoffs**: Each agent receives complete context and returns structured results
- **Audit Trail**: All operations are logged for transparency and debugging

### 3. Browser Automation Standards
- **Playwright MCP Exclusive**: All browser interactions use Playwright MCP server
- **Human-Like Patterns**: Natural delays, scrolling, and interaction timing
- **State Management**: Browser state is carefully maintained across agent transitions
- **Error Recovery**: Robust handling of UI changes and network issues

## Common Rules and Standards

### Task Execution Rules

**SEQUENTIAL EXECUTION REQUIRED** when:
- Data dependencies exist (Task B needs Task A's output)
- State mutations occur (authentication, file operations, browser navigation)
- Browser state changes (page loads before element interactions)
- File operations with dependencies (creation before permission setting)

**PARALLEL EXECUTION ALLOWED** only when:
- Independent validation checks (format validation, permission checks)
- Read-only operations with no shared state
- Multiple format compatibility checks
- Concurrent verification operations

**NEVER run dependent Task tool calls in parallel** - Each dependent step requires output from the previous step.

### Context Passing Requirements

**CRITICAL CONTEXT FLOW**:
All Task tool calls must receive complete context to ensure proper execution:

1. **Input Context**: What the component needs to receive
2. **Processing Context**: Intermediate state and decision-making data
3. **Output Context**: Structured results for downstream components
4. **Error Context**: Comprehensive error information for debugging

**Context Categories**:
- **Candidate Profile**: Skills, experience, preferences, contact info
- **Session Context**: Authentication state, browser state, progress tracking
- **Configuration Context**: Application preferences, target counts, filtering criteria
- **Operational Context**: File paths, timestamps, system requirements

### Tool Usage Patterns

**Required Tool Categories**:
- **Browser Automation**: `mcp__playwrite__browser_*` for all LinkedIn interactions
- **Task Orchestration**: `Task` for complex multi-step operations  
- **Progress Tracking**: `TodoWrite` for workflow planning and progress
- **File Operations**: `Read`, `Write`, `Edit` for data persistence
- **System Operations**: `Bash` for credential management and system tasks

**Tool Selection Rules**:
- Use Playwright MCP for ALL browser interactions (no alternatives)
- Use Task tool for multi-step operations requiring specialized logic
- Use TodoWrite for planning and tracking complex workflows
- Use native file tools for data operations and configuration management

### Agent Design Standards

#### 1. Goal Definition Section
Every agent must define:
- **Primary Goal**: Single, focused objective
- **Success Criteria**: Measurable completion conditions
- **Scope Constraints**: Clear boundaries of responsibility
- **Integration Points**: How the agent fits in the workflow

#### 2. Multi-Step Operations Section
Every agent must specify:
- **TodoWrite Usage**: Planning and progress tracking requirements
- **Task Delegation**: When and how to use Task tool
- **Sequential Dependencies**: Order of operations for complex workflows
- **Error Handling**: How to handle and recover from failures

#### 3. Task Execution Rules Section
Every agent must define:
- **Sequential Requirements**: Dependencies that require ordered execution
- **Parallel Allowances**: Independent operations that can run concurrently
- **Dependency Reasoning**: Why specific order is required

#### 4. Context Requirements Section
Every agent must specify:
- **Input Context**: Required data from calling components
- **Output Context**: Data provided to downstream components
- **Subtask Context**: Data passed to Task tool calls
- **Inter-Agent Context**: Specific forwarding between agents

### Command Design Standards

#### 1. Workflow Documentation
Every command must include:
- **Process Flow Diagram**: Mermaid flowchart showing agent interactions
- **Key Features**: Automation capabilities and constraints
- **Usage Examples**: Multiple scenarios demonstrating flexibility

#### 2. Execution Control
Every command must define:
- **Task Execution Rules**: Sequential vs parallel execution patterns
- **Context Passing Requirements**: Data flow between workflow stages
- **Error Recovery**: How to handle workflow failures

### File and Data Management

#### 1. Application Logging
- **Daily Log Files**: Separate files per day in `.claude/applications/logs/`
- **Sequential Numbering**: Continuous numbering within each day
- **Structured Format**: Consistent markdown listicle format
- **Complete Information**: Job details, timing, relevance assessment

#### 1.1. Temporary File Management
- **Temporary Directory**: All temporary files stored in `.claude/tmp/` directory
- **Automatic Cleanup**: Temporary files should be cleaned up after use
- **Isolation**: Keeps temporary files separate from application data and logs
- **Security**: Temporary files excluded from version control via .gitignore

#### 2. Credential Management
- **Environment Variables**: Secure storage in `.env` files
- **Source Priority**: Task args → .env → interactive prompt
- **Security Standards**: Restricted file permissions (600)
- **Backup Strategy**: Automated backup before credential updates

#### 3. Job Qualification Assessment
- **Default Behavior**: Skip positions where candidate is significantly overqualified to maintain professional appropriateness
- **User Override**: When user explicitly requests applying to overqualified positions (e.g., "include overqualified roles", "apply to entry-level positions"), system will apply and document reasoning
- **Documentation**: All overqualified applications are logged with "Medium" relevance score and reasoning explaining user's explicit request
- **Context Passing**: Overqualified policy preferences must be passed through entire workflow chain

#### 4. Resume Processing
- **Format Support**: PDF, DOC, MD, TXT file handling
- **Parameter Extraction**: Job titles, skills, location, seniority
- **Priority System**: Explicit params → resume data → defaults
- **Validation**: Format checking and content verification

## Workflow Architecture

### Primary Automation Flow
```
Resume Analysis → LinkedIn Login → Job Search → Job Processing → Application Tracking
```

### Inter-Agent Communication
1. **resume-analyzer** → Provides candidate profile and search parameters
2. **linkedin-login** → Establishes authenticated session
3. **linkedin-job-search** → Configures search and loads results
4. **job-processor** → Evaluates and applies to individual jobs
5. **application-tracker** → Monitors progress against targets

### Supporting Workflows
- **Credential Setup**: Secure credential configuration and validation
- **Application Logging**: Comprehensive documentation of all applications
- **Progress Tracking**: Real-time monitoring of automation progress

## Quality Standards

### 1. Error Handling
- **Graceful Degradation**: System continues when possible
- **Comprehensive Logging**: All errors captured with context
- **Recovery Strategies**: Automatic retry with exponential backoff
- **User Notification**: Clear error messages and resolution guidance

### 2. Security Standards
- **Credential Protection**: Never expose credentials in logs
- **Secure Storage**: Environment variables with restricted permissions
- **Session Management**: Proper authentication state handling
- **Data Privacy**: Minimal data retention and secure processing

### 3. Performance Standards
- **Human-Like Timing**: Natural delays to avoid detection
- **Resource Efficiency**: Minimal browser resource usage
- **Parallel Processing**: Where safe, concurrent validation operations
- **State Optimization**: Efficient browser state management

### 4. Testing and Validation
- **Input Validation**: All external data validated before use
- **State Verification**: Browser and file state confirmed at each step
- **Progress Tracking**: Real-time monitoring of workflow progress
- **Result Verification**: Application success confirmed before logging

## Development Guidelines

### 1. Adding New Agents
1. Follow the four-section standard: Goals, Operations, Execution Rules, Context
2. Define clear input/output context requirements
3. Specify Task execution patterns (sequential vs parallel)
4. Include comprehensive error handling and recovery

### 2. Modifying Existing Workflows
1. Update context passing requirements when changing data flow
2. Maintain sequential execution where dependencies exist
3. Update documentation to reflect workflow changes
4. Test end-to-end automation after modifications

### 3. Tool Integration
1. Use Playwright MCP exclusively for browser automation
2. Implement proper context passing for all Task tool calls
3. Use TodoWrite for complex workflow planning and tracking
4. Follow established file operation patterns for data persistence

### 4. Debugging and Monitoring
1. Enable comprehensive logging at each workflow stage
2. Use TodoWrite for tracking progress through complex operations
3. Implement proper error context capture and reporting
4. Monitor application success rates and system performance

## Compliance and Ethics

### 1. LinkedIn Terms of Service
- **Rate Limiting**: Human-like interaction timing
- **Respectful Automation**: No aggressive scraping or bulk operations
- **Account Safety**: Proper authentication and session management
- **Content Respect**: No manipulation of LinkedIn content or data

### 2. Professional Standards
- **Accurate Applications**: Only apply to genuinely suitable positions
- **Overqualified Position Policy**: By default, skip positions where candidate is significantly overqualified; when explicitly requested by user, apply to overqualified positions and document reasoning
- **Quality Control**: Resume and application information accuracy
- **Transparency**: Clear logging of all automation activities
- **User Control**: Easy monitoring and control of automation behavior

This architecture document serves as the foundation for all development and modification activities within the LinkedIn Job Automation system. All agents, commands, and workflows must conform to these standards to ensure reliability, security, and maintainability.