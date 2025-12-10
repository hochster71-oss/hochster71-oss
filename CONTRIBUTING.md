# Contributing to hochster71-oss

Thank you for your interest in contributing to the BMC3 Sandbox RMF Package! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- **Bug Reports**: Found an issue? Open a bug report with detailed information
- **Feature Requests**: Have an idea? Share it via an issue
- **Code Contributions**: Submit pull requests for bug fixes or new features
- **Documentation**: Help improve documentation and examples
- **Testing**: Test the scripts on different platforms and report issues

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   gh repo fork hochster71-oss/hochster71-oss
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/hochster71-oss.git
   cd hochster71-oss
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

### Testing

Before submitting a pull request:

1. **Test on multiple platforms** (Windows, Linux, macOS if possible)
2. **Run all scripts** to ensure they work end-to-end
3. **Verify generated outputs** are valid (CSVs, Mermaid diagrams, XML)

### Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new control family support`
- `fix: Correct CSV escaping in Jira export`
- `docs: Update installation instructions`
- `refactor: Simplify flowchart generation logic`

## 🔍 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Test your changes** thoroughly
3. **Update README.md** if needed
4. **Ensure no generated files** are committed (they're in .gitignore)
5. **Submit PR** with clear description of changes

### PR Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] All scripts run successfully
- [ ] Generated outputs are valid

## Related Issues
Fixes #(issue number)
```

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **System information**
   - OS and version
   - Python version
   - Shell type

2. **Steps to reproduce**
   - Exact commands run
   - Current directory
   - Input files (if any)

3. **Expected behavior**
4. **Actual behavior**
5. **Error messages** (full stack trace)
6. **Screenshots** (if applicable)

## 💡 Feature Requests

For feature requests, describe:

1. **The problem** you're trying to solve
2. **Your proposed solution**
3. **Alternative solutions** you've considered
4. **Use case** and benefits

## 📋 Project Structure

```
hochster71-oss/
├── fetch_cci_mapping.py      # Download DISA CCI mappings
├── build_rmf_flowchart.py    # Generate Mermaid diagrams
├── generate_jira_csv.py      # Create Jira import CSVs
├── confluence_export.xml     # Confluence space template
├── run_all.sh               # Unix automation script
├── run_all.ps1              # Windows automation script
├── requirements.txt         # Python dependencies
├── README.md                # Main documentation
├── CONTRIBUTING.md          # This file
└── .gitignore              # Ignored files
```

## 🔐 Security

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email the maintainer directly
3. Include detailed information about the vulnerability
4. Allow time for a fix before public disclosure

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

- Open an issue for general questions
- Tag issues with `question` label
- Be respectful and patient

## 🙏 Recognition

Contributors will be acknowledged in:
- The project README
- Release notes
- Special thanks section

Thank you for contributing to making DoD RMF compliance easier! 🛡️
