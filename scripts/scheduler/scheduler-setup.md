# Scheduler Deployment Guide

## Prerequisites

### 1. System Requirements

- macOS (for Appium-based test automation)
- Python 3.10+
- Git with HTTPS access to `https://github.com/edge-microsoft/FSQ_AI_Testcases_Mac.git`
- Git Credential Manager (GCM) for unattended HTTPS clone

### 2. Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

### 3. Configure Claude Code Access

**Option A: API Key (Direct)**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add to `~/.zshrc` or `~/.bashrc` for persistence.

**Option B: Proxy (e.g., Agent Maestro)**

Configure the proxy URL and auth token in `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:23333/api/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "your-proxy-auth-token"
  }
}
```

When using a proxy, no `ANTHROPIC_API_KEY` is needed. Make sure the proxy service is running before starting the scheduler.

### 4. Install Azure CLI

```bash
brew install azure-cli
az extension add --name azure-devops
```

### 5. Login to Azure

```bash
az login
az devops configure --defaults organization=https://dev.azure.com/microsoft project=Edge
```

Verify:
```bash
az account show
```

> **Note:** For unattended execution, use a service principal:
> ```bash
> az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>
> ```

### 6. Install Python Dependencies

```bash
pip install pyyaml
```

Or if using `uv`:
```bash
uv pip install pyyaml
```

### 7. Configure Git Credential Manager

The scheduler clones the repository via HTTPS on every run. To avoid interactive authentication prompts, configure Git Credential Manager (GCM) to cache credentials in macOS Keychain.

**Install GCM** (if not already bundled with Git):
```bash
brew install git-credential-manager
```

**Verify GCM is configured:**
```bash
git config --global credential.helper
# Should output: /usr/local/share/gcm-core/git-credential-manager (or similar)
```

**Trigger initial authentication** (one-time, interactive):
```bash
git clone https://github.com/edge-microsoft/FSQ_AI_Testcases_Mac.git /tmp/test-clone --depth 1
rm -rf /tmp/test-clone
```

After authenticating once, GCM stores the token in macOS Keychain. Subsequent unattended clones will use the cached credential automatically.

## Setup

### 1. Copy Scheduler Files

Copy the scheduler directory to your desired location:

```bash
cp -r scripts/scheduler /path/to/scheduler
cd /path/to/scheduler
```

### 2. Edit Configuration

Edit `config.yaml`:

```yaml
pipelines:
  - edge-FSQ-mac-canary
  - edge-FSQ-mac-beta
  - edge-FSQ-mac-stable

poll_interval_minutes: 10

# ...
```

Key settings:
- `profiles.<name>.pipelines` — Pipeline names to monitor
- `profiles.<name>.clone.repo_url` — HTTPS URL of the test case repository
- `profiles.<name>.claude.timeout_seconds` — Max time for Claude analysis (default: 3600)
- `profiles.<name>.power_automate.webhook_url` — Power Automate HTTP trigger URL (optional)

### 3. Verify Git Access

```bash
git ls-remote https://github.com/edge-microsoft/FSQ_AI_Testcases_Mac.git HEAD
```

Should return a commit hash without prompting for credentials.

### 4. Test Run (Single Poll)

```bash
python scheduler.py --once
```

This runs one poll cycle and exits. Check the output for any errors.

## Running

### Option A: Direct Execution

```bash
python scheduler.py
```

Runs continuously, polling every N minutes as configured.

### Option B: launchd (macOS, Recommended)

Create `~/Library/LaunchAgents/com.fsq.scheduler.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fsq.scheduler</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/scheduler/scheduler.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/scheduler</string>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/scheduler/scheduler.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/scheduler/scheduler.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <!-- Option A: Direct API key -->
        <!-- <key>ANTHROPIC_API_KEY</key>
        <string>sk-ant-...</string> -->

        <!-- Option B: Proxy (e.g., Agent Maestro) -->
        <key>ANTHROPIC_BASE_URL</key>
        <string>http://localhost:23333/api/anthropic</string>
        <key>ANTHROPIC_AUTH_TOKEN</key>
        <string>your-proxy-auth-token</string>

        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>HOME</key>
        <string>/Users/your-username</string>
    </dict>
</dict>
</plist>
```

Load and start:
```bash
launchctl load ~/Library/LaunchAgents/com.fsq.scheduler.plist
```

Check status:
```bash
launchctl list | grep fsq
```

Stop:
```bash
launchctl unload ~/Library/LaunchAgents/com.fsq.scheduler.plist
```

## Files

| File | Description |
|------|-------------|
| `config.yaml` | Configuration (pipelines, clone URL, timeouts, etc.) |
| `scheduler.py` | Main scheduler script |
| `build_history.json` | Processed build records (auto-generated, retained 30 days) |
| `.scheduler.lock` | Lock file to prevent concurrent runs (auto-managed) |

## Troubleshooting

### "Failed to get access token"
Azure CLI session expired. Run `az login` again.

### "Lock held since ..."
A previous run is still in progress or crashed. If crashed, delete `.scheduler.lock` manually.

### Clone fails
Check Git credential: `git ls-remote https://github.com/edge-microsoft/FSQ_AI_Testcases_Mac.git HEAD`. If prompted for credentials, re-authenticate once to refresh the GCM cache.

### Claude times out
Increase `claude.timeout_seconds` in `config.yaml`. Default is 3600 (1 hour).
