#!/bin/bash

# Non-interactive Appium Startup Script for automation
# Automatically kills existing Appium and starts fresh

PORT=4723
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/appium_$(date +%Y%m%d_%H%M%S).log"

echo "=== Starting Appium Server (Auto Mode) ==="

# Check if Appium is installed
if ! command -v appium &> /dev/null; then
    echo "Error: Appium not installed"
    exit 1
fi

echo "Appium version: $(appium --version)"

# Kill existing Appium process if running
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Killing existing Appium process on port $PORT..."
    pkill -f appium
    sleep 3
    
    # Force kill if still running
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "Force killing..."
        lsof -Pi :$PORT -sTCP:LISTEN -t | xargs kill -9 2>/dev/null
        sleep 2
    fi
fi

# Create log directory
mkdir -p "$LOG_DIR"

echo "Starting Appium on port $PORT..."
echo "Log file: $LOG_FILE"

# Start Appium in background
nohup appium server \
    --port $PORT \
    --log-level info \
    --log-timestamp \
    --local-timezone \
    --log "$LOG_FILE" \
    --relaxed-security \
    --allow-insecure chromedriver_autodownload \
    > /dev/null 2>&1 &

APPIUM_PID=$!
echo "Appium PID: $APPIUM_PID"

echo "Waiting for Appium to start..."
for i in {1..15}; do
    if curl -s http://localhost:$PORT/status > /dev/null 2>&1; then
        echo "Appium server is ready!"
        echo "URL: http://localhost:$PORT"
        exit 0
    fi
    sleep 1
done

echo "Error: Appium failed to start within 15 seconds"
exit 1
