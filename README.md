# FSQ_AI_Testcases_Mac

AI-powered test case recording and automation for Microsoft Edge on macOS. This project provides automated testing capabilities using BDD (Behavior-Driven Development) approach with Gherkin feature files.

## Features

- **BDD Testing**: Uses Gherkin feature files for test scenarios
- **AI-Powered**: Automated test case recording and generation
- **Cross-Platform**: Optimized for macOS Edge browser testing
- **Appium Integration**: Mobile and desktop app automation support

## Project Structure

```
features/           # BDD feature files and step definitions
├── download/       # Download functionality tests
├── favorite/       # Favorites feature tests
├── history/        # Browser history tests
├── ominibox/       # Address bar/omnibox tests
├── tab/            # Tab management tests
└── steps/          # Python step implementations
scripts/            # Utility scripts (Appium setup, etc.)
logs/               # Test execution logs
```

## Getting Started

### Prerequisites

- Python 3.8+
- macOS
- Microsoft Edge browser
- Appium (for automation)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FSQ_AI_Testcases_Mac
```

2. Install dependencies:
```bash
uv sync
```

3. Start Appium server:
```bash
./scripts/start_appium.sh
```

### Running Tests

Execute BDD test scenarios:
```bash
# Run all tests
behave features/

```

## 🎨 Code Formatting

This project uses automated code formatting for consistent code style:
- **Python files**: Formatted with [Ruff](https://docs.astral.sh/ruff/)
- **Feature files**: Formatted with [reformat-gherkin](https://pypi.org/project/reformat-gherkin/)

### Manual Formatting
```bash
uv run format.py
```

### Pre-commit Hooks
```bash
# Setup
uv sync
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files

# Skip pre-commit hooks (直接提交)
git commit --no-verify -m "commit message"
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

For complex changes, please open an issue first to discuss the proposal.
