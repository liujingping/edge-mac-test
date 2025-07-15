#!/bin/bash

# macOS Appium Environment Startup Script
# Includes complete environment check and server startup

echo "=== macOS Appium Automation Environment Startup Script ==="
echo

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Appium is installed
if ! command -v appium &> /dev/null; then
    echo -e "${RED}❌ Appium not installed, please run: npm install -g appium${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Appium version: $(appium --version)${NC}"

# Check Mac2 driver
echo -e "\n${BLUE}📋 Checking installed drivers:${NC}"
MAC2_OUTPUT=$(appium driver list 2>&1)
if echo "$MAC2_OUTPUT" | grep -q "mac2.*\[installed"; then
    MAC2_INFO=$(echo "$MAC2_OUTPUT" | grep "mac2.*\[installed" | head -1 | sed 's/^- //')
    echo -e "${GREEN}✅ Mac2 driver installed${NC}"
    echo -e "${BLUE}📍 $MAC2_INFO${NC}"
else
    echo -e "${RED}❌ Mac2 driver not installed${NC}"
    echo -e "${YELLOW}Installing Mac2 driver...${NC}"
    appium driver install mac2
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Mac2 driver installation successful${NC}"
    else
        echo -e "${RED}❌ Mac2 driver installation failed${NC}"
        exit 1
    fi
fi

# Check port usage
PORT=4723
echo -e "\n${BLUE}📋 Checking port usage:${NC}"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Port $PORT is already in use${NC}"
    
    # Ask whether to terminate existing process
    read -p "Do you want to terminate the existing Appium process? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Terminating existing process...${NC}"
        pkill -f appium
        sleep 3
        
        # Check again
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
            echo -e "${RED}❌ Unable to terminate existing process, please handle manually${NC}"
            exit 1
        else
            echo -e "${GREEN}✅ Existing process terminated${NC}"
        fi
    else
        echo -e "${YELLOW}Starting with different port...${NC}"
        PORT=4724
        echo -e "${BLUE}New port: $PORT${NC}"
    fi
else
    echo -e "${GREEN}✅ Port $PORT is available${NC}"
fi

# Create log directory
LOG_DIR="./logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo -e "${GREEN}✅ Created log directory: $LOG_DIR${NC}"
fi

# Generate log filename
LOG_FILE="$LOG_DIR/appium_$(date +%Y%m%d_%H%M%S).log"

echo -e "\n${BLUE}🚀 Starting Appium server...${NC}"
echo -e "${BLUE}Port: $PORT${NC}"
echo -e "${BLUE}Log file: $LOG_FILE${NC}"
echo -e "${BLUE}Stop server: Ctrl+C${NC}"
echo

# Startup parameter configuration
APPIUM_ARGS=(
    "server"
    "--port" "$PORT"
    "--log-level" "info"
    "--log-timestamp"
    "--local-timezone"
    "--log" "$LOG_FILE"
    "--relaxed-security"
    "--allow-insecure" "chromedriver_autodownload"
)

# Check if WebDriverAgentMac is built
echo -e "\n${BLUE}📋 Checking WebDriverAgentMac build status:${NC}"
WDA_PATH=$(find ~/.appium -name "WebDriverAgentMac" -type d 2>/dev/null | head -1)
if [[ -n "$WDA_PATH" ]]; then
    echo -e "${BLUE}📍 WebDriverAgentMac path: $WDA_PATH${NC}"
    
    # Check multiple possible build locations
    WDA_BUILT=false
    BUILD_LOCATIONS=()
    
    # Check build results in DerivedData
    DERIVED_DATA_PATHS=$(find ~/Library/Developer/Xcode/DerivedData -name "*WebDriverAgentMac*" -type d 2>/dev/null)
    for DERIVED_DATA_PATH in $DERIVED_DATA_PATHS; do
        if [[ -d "$DERIVED_DATA_PATH/Build/Products/Debug" ]]; then
            RUNNER_APPS=$(find "$DERIVED_DATA_PATH/Build/Products/Debug" -name "*Runner*.app" -type d 2>/dev/null)
            if [[ -n "$RUNNER_APPS" ]]; then
                WDA_BUILT=true
                BUILD_LOCATIONS+=("DerivedData: $DERIVED_DATA_PATH/Build/Products/Debug")
                break
            fi
        fi        done
    
    # Check project local build directory
    if [[ -d "$WDA_PATH/build" ]]; then
        BUILD_PRODUCTS=$(find "$WDA_PATH/build" -name "*.app" -type d 2>/dev/null)
        if [[ -n "$BUILD_PRODUCTS" ]]; then
            WDA_BUILT=true
            BUILD_LOCATIONS+=("Local build: $WDA_PATH/build")
        fi
    fi
    
    if [[ "$WDA_BUILT" == "true" ]]; then
        echo -e "${GREEN}✅ WebDriverAgentMac built${NC}"
        for location in "${BUILD_LOCATIONS[@]}"; do
            echo -e "${GREEN}   - $location${NC}"
        done
    else
        echo -e "${YELLOW}⚠️  WebDriverAgentMac not built, recommend building first${NC}"
        echo -e "${BLUE}Build command: cd '$WDA_PATH' && xcodebuild -project WebDriverAgentMac.xcodeproj -scheme WebDriverAgentRunner -destination 'platform=macOS' build${NC}"
        
        read -p "Do you want to build WebDriverAgentMac now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Building WebDriverAgentMac...${NC}"
            cd "$WDA_PATH"
            xcodebuild -project WebDriverAgentMac.xcodeproj -scheme WebDriverAgentRunner -destination 'platform=macOS' build
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ WebDriverAgentMac build successful${NC}"
            else
                echo -e "${RED}❌ WebDriverAgentMac build failed${NC}"
                echo -e "${YELLOW}Tip: You may need to run 'sudo xcodebuild -runFirstLaunch' first${NC}"
                echo -e "${YELLOW}Or try manually opening the project in Xcode for building${NC}"
            fi
            cd - > /dev/null
        fi
    fi
else
    echo -e "${YELLOW}⚠️  WebDriverAgentMac not found, Mac2 driver may not be installed correctly${NC}"
    echo -e "${BLUE}Please confirm Mac2 driver is installed: appium driver install mac2${NC}"
fi

echo -e "\n${GREEN}🎯 Startup command: appium ${APPIUM_ARGS[*]}${NC}"
echo -e "${BLUE}Press Ctrl+C to stop server${NC}"
echo "=" * 60

# Capture exit signals - Set before starting server to ensure graceful exit when user presses Ctrl+C
trap 'echo -e "\n${YELLOW}Stopping Appium server...${NC}"; exit 0' INT TERM

echo -e "\n${GREEN}🚀 Starting Appium server...${NC}"
echo -e "${BLUE}   Access URL: http://localhost:4723${NC}"
echo -e "${BLUE}   Press Ctrl+C to stop server${NC}"
echo -e "${BLUE}   Keep this terminal window open, run tests in a new window${NC}"
echo

# Start Appium server
appium "${APPIUM_ARGS[@]}"