# Scheduler Deployment Guide

## Prerequisites

### 1. System Requirements

- macOS (for Appium-based test automation)
- Python 3.10+
- Git with SSH key configured for `git@github.com:edge-microsoft/FSQ_AI_Testcases_Mac.git`

### 2. Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

### 3. Configure Claude API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add to `~/.zshrc` or `~/.bashrc` for persistence.

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
- `profiles.<name>.clone.repo_url` — SSH URL of the test case repository
- `profiles.<name>.claude.timeout_seconds` — Max time for Claude analysis (default: 3600)
- `profiles.<name>.power_automate.webhook_url` — Power Automate HTTP trigger URL (optional)

### 3. Verify SSH Access

```bash
ssh -T git@github.com
```

Should show: `Hi <username>! You've successfully authenticated`.

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
        <key>ANTHROPIC_API_KEY</key>
        <string>sk-ant-...</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
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
Check SSH key: `ssh -T git@github.com`. Ensure the deploy key or personal SSH key has access to the repository.

### Claude times out
Increase `claude.timeout_seconds` in `config.yaml`. Default is 3600 (1 hour).
