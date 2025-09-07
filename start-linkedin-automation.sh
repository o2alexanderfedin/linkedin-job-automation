#!/bin/bash
# LinkedIn Job Automation Startup Script
# Sets up and starts the complete automation environment

set -euo pipefail

# Configuration
PLAYWRIGHT_MCP_PORT="8931"
PLAYWRIGHT_MCP_URL="http://localhost:${PLAYWRIGHT_MCP_PORT}/mcp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_CONFIG_FILE="${SCRIPT_DIR}/.mcp.json"
CLAUDE_EXECUTABLE="$HOME/.claude/local/claude"
PLAYWRIGHT_MCP_PID_FILE="${SCRIPT_DIR}/.claude/tmp/playwright-mcp.pid"
LOG_DIR="${SCRIPT_DIR}/.claude/logs"
PLAYWRIGHT_LOG="${LOG_DIR}/playwright-mcp.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Cleanup function
cleanup() {
    log "Shutting down LinkedIn automation environment..."
    
    # Stop Playwright MCP server
    if [ -f "$PLAYWRIGHT_MCP_PID_FILE" ]; then
        local pid=$(cat "$PLAYWRIGHT_MCP_PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            log "Stopping Playwright MCP server (PID: $pid)..."
            kill $pid
            # Wait for process to stop
            local count=0
            while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                ((count++))
            done
            if ps -p $pid > /dev/null 2>&1; then
                warn "Playwright MCP server didn't stop gracefully, force killing..."
                kill -9 $pid
            fi
        fi
        rm -f "$PLAYWRIGHT_MCP_PID_FILE"
    fi
    
    # Kill any remaining playwright/MCP processes
    pkill -f "mcp-server-playwright" 2>/dev/null || true
    pkill -f "@playwright/mcp" 2>/dev/null || true
    
    log "Environment shutdown complete."
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Create required directories
setup_directories() {
    log "Setting up directory structure..."
    mkdir -p "${SCRIPT_DIR}/.claude/tmp"
    mkdir -p "${SCRIPT_DIR}/.claude/logs"
    mkdir -p "${SCRIPT_DIR}/.claude/applications/logs"
}

# Check if Node.js is installed
check_nodejs() {
    if ! command -v node >/dev/null 2>&1; then
        error "Node.js is not installed. Please install Node.js from https://nodejs.org/"
        exit 1
    fi
    
    local node_version=$(node --version | cut -d'v' -f2)
    local major_version=$(echo $node_version | cut -d'.' -f1)
    
    if [ "$major_version" -lt "16" ]; then
        error "Node.js version 16 or higher is required. Current version: $node_version"
        exit 1
    fi
    
    info "Node.js version: $node_version ✓"
}

# Check if Claude Code is installed
check_claude_installation() {
    if [ ! -f "$CLAUDE_EXECUTABLE" ]; then
        error "Claude Code is not installed at $CLAUDE_EXECUTABLE"
        echo "Please install Claude Code by following the instructions at:"
        echo "https://docs.anthropic.com/en/docs/claude-code/installation"
        exit 1
    fi
    
    info "Claude Code installation found ✓"
}

# Install/Update Playwright MCP server
install_playwright_mcp() {
    log "Ensuring Playwright MCP server is installed..."
    
    # Check if already installed and get version
    if npx --yes @playwright/mcp@latest --version >/dev/null 2>&1; then
        info "Playwright MCP server is available ✓"
    else
        error "Failed to verify Playwright MCP server installation"
        exit 1
    fi
}

# Configure MCP server
configure_mcp() {
    log "Configuring MCP server..."
    
    cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "playwrite": {
      "type": "http",
      "url": "$PLAYWRIGHT_MCP_URL"
    }
  }
}
EOF
    
    info "MCP configuration written to $MCP_CONFIG_FILE ✓"
}

# Start Playwright MCP server
start_playwright_mcp() {
    log "Starting Playwright MCP server on port $PLAYWRIGHT_MCP_PORT..."
    
    # Check if port is already in use
    if lsof -Pi :$PLAYWRIGHT_MCP_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        warn "Port $PLAYWRIGHT_MCP_PORT is already in use"
        local existing_pid=$(lsof -Pi :$PLAYWRIGHT_MCP_PORT -sTCP:LISTEN -t)
        if ps -p $existing_pid -o comm= | grep -q "mcp-server-playwright\|@playwright/mcp"; then
            info "Playwright MCP server is already running (PID: $existing_pid)"
            echo $existing_pid > "$PLAYWRIGHT_MCP_PID_FILE"
            return 0
        else
            error "Port $PLAYWRIGHT_MCP_PORT is occupied by another process (PID: $existing_pid)"
            exit 1
        fi
    fi
    
    # Start the server in background
    npx --yes @playwright/mcp@latest --port $PLAYWRIGHT_MCP_PORT > "$PLAYWRIGHT_LOG" 2>&1 &
    local mcp_pid=$!
    echo $mcp_pid > "$PLAYWRIGHT_MCP_PID_FILE"
    
    # Wait for server to start
    local count=0
    while ! curl -s "http://localhost:$PLAYWRIGHT_MCP_PORT/mcp" >/dev/null 2>&1 && [ $count -lt 30 ]; do
        sleep 1
        ((count++))
        if ! ps -p $mcp_pid > /dev/null 2>&1; then
            error "Playwright MCP server failed to start"
            cat "$PLAYWRIGHT_LOG" | tail -20
            exit 1
        fi
    done
    
    if [ $count -eq 30 ]; then
        error "Playwright MCP server did not start within 30 seconds"
        cat "$PLAYWRIGHT_LOG" | tail -20
        exit 1
    fi
    
    log "Playwright MCP server started successfully (PID: $mcp_pid) ✓"
}

# Verify MCP server is responding
verify_mcp_server() {
    log "Verifying MCP server connectivity..."
    
    if curl -s "$PLAYWRIGHT_MCP_URL" >/dev/null 2>&1; then
        info "MCP server is responding ✓"
    else
        error "MCP server is not responding at $PLAYWRIGHT_MCP_URL"
        exit 1
    fi
}

# Start Claude Code
start_claude() {
    log "Starting Claude Code with LinkedIn automation environment..."
    
    # Change to project directory
    cd "$SCRIPT_DIR"
    
    # Start Claude with proper configuration
    exec "$CLAUDE_EXECUTABLE" \
        --allowedTools "*" \
        --dangerously-skip-permissions \
        --permission-mode "bypassPermissions" \
        "$@"
}

# Print environment status
print_status() {
    echo
    log "LinkedIn Job Automation Environment Status:"
    echo "  📁 Project Directory: $SCRIPT_DIR"
    echo "  🤖 Playwright MCP Server: http://localhost:$PLAYWRIGHT_MCP_PORT/mcp"
    echo "  📝 MCP Configuration: $MCP_CONFIG_FILE"
    echo "  📋 Logs Directory: $LOG_DIR"
    echo "  🎯 Ready for LinkedIn job automation!"
    echo
    info "Available commands:"
    echo "  /linkedin-jobs - Start automated job applications"
    echo "  /setup-job-credentials - Configure your credentials"
    echo "  /browse-apply-jobs - Browse and apply to jobs manually"
    echo
}

# Main execution
main() {
    log "Starting LinkedIn Job Automation Environment Setup..."
    
    # Setup
    setup_directories
    check_nodejs
    check_claude_installation
    install_playwright_mcp
    configure_mcp
    
    # Start services
    start_playwright_mcp
    verify_mcp_server
    
    # Show status and start Claude
    print_status
    start_claude "$@"
}

# Help function
show_help() {
    cat << EOF
LinkedIn Job Automation Startup Script

USAGE:
    $0 [OPTIONS]

DESCRIPTION:
    Sets up and starts the complete LinkedIn job automation environment including:
    - Playwright MCP server for browser automation
    - Claude Code with proper configuration
    - Required directory structure and logging

OPTIONS:
    -h, --help     Show this help message

ENVIRONMENT:
    The script will:
    1. Verify Node.js and Claude Code installations
    2. Install/update Playwright MCP server
    3. Configure MCP server connection
    4. Start Playwright MCP server in background
    5. Start Claude Code with automation environment
    6. Clean up Playwright MCP server on exit

LOGS:
    Playwright MCP logs: $LOG_DIR/playwright-mcp.log
    
CONFIGURATION:
    MCP server configuration: .mcp.json
    Playwright MCP server port: $PLAYWRIGHT_MCP_PORT

For more information, see the project documentation in CLAUDE.md
EOF
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac