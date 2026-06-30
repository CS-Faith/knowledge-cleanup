# Contributing to knowledge-cleanup

Thank you for your interest in contributing to knowledge-cleanup! We welcome contributions from everyone.

## How to Contribute

### Reporting Issues

1. **Check existing issues** - Please search our [Issues](https://github.com/CS-Faith/knowledge-cleanup/issues) to see if the issue has already been reported.
2. **Create a new issue** - If the issue doesn't exist, create a new one with:
   - Clear title describing the problem
   - Detailed description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Your environment (Python version, OS, etc.)

### Suggesting Features

1. **Check our roadmap** - Look at existing issues and discussions
2. **Open a discussion** - Start a discussion in [GitHub Discussions](https://github.com/CS-Faith/knowledge-cleanup/discussions) to propose new features
3. **Create an issue** - For well-defined feature requests

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add appropriate comments
   - Update documentation if needed
4. **Test your changes**
   - Run existing tests
   - Add new tests for new functionality
5. **Commit your changes**
   ```bash
   git commit -m 'Add some feature'
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Describe what you changed and why

## Development Setup

```bash
# Clone the repository
git clone https://github.com/CS-Faith/knowledge-cleanup.git
cd knowledge-cleanup

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies (if any)
pip install -r requirements-dev.txt
```

## Code Style Guidelines

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 120 characters
- **Naming**: Use descriptive names for variables and functions
- **Comments**: Add comments to explain complex logic
- **Imports**: Group imports (standard library, third-party, local)
- **Docstrings**: Add docstrings to functions and classes

## Testing

Please ensure your changes don't break existing functionality:

```bash
# Run the main script with test data
python run_cleanup.py /path/to/test/source /path/to/test/target
```

## Pull Request Guidelines

1. **Small, focused changes** - Keep PRs small and focused on one feature/fix
2. **Clear commit messages** - Each commit should have a clear, descriptive message
3. **Update documentation** - Update README, docs, etc. if your change affects usage
4. **Add tests** - Add tests for new functionality
5. **Keep it clean** - Remove any debug code, print statements, etc.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

By contributing to knowledge-cleanup, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to knowledge-cleanup! Your contributions help make this project better for everyone.