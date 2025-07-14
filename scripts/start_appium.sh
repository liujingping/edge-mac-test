#!/bin/bash

# macOS Appium 环境启动脚本
# 包含完整的环境检查和服务器启动

echo "=== macOS Appium 自动化环境启动脚本 ==="
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Appium 是否安装
if ! command -v appium &> /dev/null; then
    echo -e "${RED}❌ Appium 未安装，请先运行: npm install -g appium${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Appium 版本: $(appium --version)${NC}"

# 检查 Mac2 驱动
echo -e "\n${BLUE}📋 检查已安装的驱动:${NC}"
MAC2_OUTPUT=$(appium driver list 2>&1)
if echo "$MAC2_OUTPUT" | grep -q "mac2.*\[installed"; then
    MAC2_INFO=$(echo "$MAC2_OUTPUT" | grep "mac2.*\[installed" | head -1 | sed 's/^- //')
    echo -e "${GREEN}✅ Mac2 驱动已安装${NC}"
    echo -e "${BLUE}📍 $MAC2_INFO${NC}"
else
    echo -e "${RED}❌ Mac2 驱动未安装${NC}"
    echo -e "${YELLOW}正在安装 Mac2 驱动...${NC}"
    appium driver install mac2
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Mac2 驱动安装成功${NC}"
    else
        echo -e "${RED}❌ Mac2 驱动安装失败${NC}"
        exit 1
    fi
fi

# 检查端口占用
PORT=4723
echo -e "\n${BLUE}📋 检查端口占用:${NC}"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  端口 $PORT 已被占用${NC}"
    
    # 询问是否终止现有进程
    read -p "是否终止现有的Appium进程？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}正在终止现有进程...${NC}"
        pkill -f appium
        sleep 3
        
        # 再次检查
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
            echo -e "${RED}❌ 无法终止现有进程，请手动处理${NC}"
            exit 1
        else
            echo -e "${GREEN}✅ 现有进程已终止${NC}"
        fi
    else
        echo -e "${YELLOW}使用不同端口启动...${NC}"
        PORT=4724
        echo -e "${BLUE}新端口: $PORT${NC}"
    fi
else
    echo -e "${GREEN}✅ 端口 $PORT 可用${NC}"
fi

# 创建日志目录
LOG_DIR="./logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo -e "${GREEN}✅ 创建日志目录: $LOG_DIR${NC}"
fi

# 生成日志文件名
LOG_FILE="$LOG_DIR/appium_$(date +%Y%m%d_%H%M%S).log"

echo -e "\n${BLUE}🚀 启动 Appium 服务器...${NC}"
echo -e "${BLUE}端口: $PORT${NC}"
echo -e "${BLUE}日志文件: $LOG_FILE${NC}"
echo -e "${BLUE}停止服务器: Ctrl+C${NC}"
echo

# 启动参数配置
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

# 检查WebDriverAgentMac是否已构建
echo -e "\n${BLUE}📋 检查 WebDriverAgentMac 构建状态:${NC}"
WDA_PATH=$(find ~/.appium -name "WebDriverAgentMac" -type d 2>/dev/null | head -1)
if [[ -n "$WDA_PATH" ]]; then
    echo -e "${BLUE}📍 WebDriverAgentMac 路径: $WDA_PATH${NC}"
    
    # 检查多个可能的构建位置
    WDA_BUILT=false
    BUILD_LOCATIONS=()
    
    # 检查 DerivedData 中的构建结果
    DERIVED_DATA_PATHS=$(find ~/Library/Developer/Xcode/DerivedData -name "*WebDriverAgentMac*" -type d 2>/dev/null)
    for DERIVED_DATA_PATH in $DERIVED_DATA_PATHS; do
        if [[ -d "$DERIVED_DATA_PATH/Build/Products/Debug" ]]; then
            RUNNER_APPS=$(find "$DERIVED_DATA_PATH/Build/Products/Debug" -name "*Runner*.app" -type d 2>/dev/null)
            if [[ -n "$RUNNER_APPS" ]]; then
                WDA_BUILT=true
                BUILD_LOCATIONS+=("DerivedData: $DERIVED_DATA_PATH/Build/Products/Debug")
                break
            fi
        fi
    done
    
    # 检查项目本地构建目录
    if [[ -d "$WDA_PATH/build" ]]; then
        BUILD_PRODUCTS=$(find "$WDA_PATH/build" -name "*.app" -type d 2>/dev/null)
        if [[ -n "$BUILD_PRODUCTS" ]]; then
            WDA_BUILT=true
            BUILD_LOCATIONS+=("本地构建: $WDA_PATH/build")
        fi
    fi
    
    if [[ "$WDA_BUILT" == "true" ]]; then
        echo -e "${GREEN}✅ WebDriverAgentMac 已构建${NC}"
        for location in "${BUILD_LOCATIONS[@]}"; do
            echo -e "${GREEN}   - $location${NC}"
        done
    else
        echo -e "${YELLOW}⚠️  WebDriverAgentMac 未构建，建议先构建${NC}"
        echo -e "${BLUE}构建命令: cd '$WDA_PATH' && xcodebuild -project WebDriverAgentMac.xcodeproj -scheme WebDriverAgentRunner -destination 'platform=macOS' build${NC}"
        
        read -p "是否现在构建 WebDriverAgentMac？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}正在构建 WebDriverAgentMac...${NC}"
            cd "$WDA_PATH"
            xcodebuild -project WebDriverAgentMac.xcodeproj -scheme WebDriverAgentRunner -destination 'platform=macOS' build
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ WebDriverAgentMac 构建成功${NC}"
            else
                echo -e "${RED}❌ WebDriverAgentMac 构建失败${NC}"
                echo -e "${YELLOW}提示: 可能需要先运行 'sudo xcodebuild -runFirstLaunch'${NC}"
                echo -e "${YELLOW}或者尝试手动在 Xcode 中打开项目进行构建${NC}"
            fi
            cd - > /dev/null
        fi
    fi
else
    echo -e "${YELLOW}⚠️  未找到 WebDriverAgentMac，Mac2 驱动可能未正确安装${NC}"
    echo -e "${BLUE}请确认 Mac2 驱动已安装: appium driver install mac2${NC}"
fi

echo -e "\n${GREEN}🎯 启动命令: appium ${APPIUM_ARGS[*]}${NC}"
echo -e "${BLUE}按 Ctrl+C 停止服务器${NC}"
echo "=" * 60

# 捕获退出信号 - 在启动服务器前设置，确保用户按Ctrl+C时能优雅退出
trap 'echo -e "\n${YELLOW}正在停止 Appium 服务器...${NC}"; exit 0' INT TERM

echo -e "\n${GREEN}🚀 启动 Appium 服务器...${NC}"
echo -e "${BLUE}   访问地址: http://localhost:4723${NC}"
echo -e "${BLUE}   按 Ctrl+C 停止服务器${NC}"
echo -e "${BLUE}   保持此终端窗口打开，在新窗口中运行测试${NC}"
echo

# 启动 Appium 服务器
appium "${APPIUM_ARGS[@]}"