# Development Guide

This guide covers everything you need to know to contribute to pypresence.

## Setting Up Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/qwertyquerty/pypresence.git
   cd pypresence
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install in editable mode with development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

   This installs pypresence in editable mode along with all development tools:
   - `pytest` - Testing framework
   - `pytest-asyncio` - Async test support
   - `pytest-mock` - Mocking utilities
   - `pytest-cov` - Coverage reporting
   - `black` - Code formatter
   - `flake8` - Linter
   - `mypy` - Type checker
   - `isort` - Import sorter
   - `sphinx` - Documentation generator

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_presence.py
```

Run tests with coverage:
```bash
pytest --cov=pypresence --cov-report=html
```

Exclude manual tests (require Discord running):
```bash
pytest -m "not manual"
```

### Test Markers

- `asyncio` - Async tests
- `integration` - Integration tests
- `manual` - Tests requiring manual setup (e.g., Discord running)

## Code Quality

**Format code with Black:**
```bash
black .
```

**Check code style with flake8:**
```bash
flake8 pypresence tests
```

**Sort imports with isort:**
```bash
isort .
```

**Type check with mypy:**
```bash
mypy pypresence
```

**Run all checks at once:**
```bash
black . && isort . && flake8 pypresence tests && mypy pypresence && pytest
```

## Project Structure

```
pypresence/
├── pypresence/          # Main package
│   ├── __init__.py     # Package initialization, version
│   ├── baseclient.py   # Base RPC client
│   ├── client.py       # Full RPC client (authorize, etc.)
│   ├── presence.py     # Simple presence client
│   ├── payloads.py     # Payload builders
│   ├── exceptions.py   # Custom exceptions
│   ├── types.py        # Type definitions
│   └── utils.py        # Utility functions
├── tests/              # Test suite
│   ├── test_baseclient.py
│   ├── test_presence.py
│   ├── test_payloads.py
│   └── ...
├── examples/           # Example scripts
├── docs/              # Documentation
└── pyproject.toml     # Project configuration
```

### Key Files

- **`pypresence/__init__.py`** - Package entry point, defines `__version__`
- **`pypresence/baseclient.py`** - Core IPC communication with Discord
- **`pypresence/presence.py`** - Simple Rich Presence API
- **`pypresence/client.py`** - Full RPC client with authorization
- **`pyproject.toml`** - All project configuration (build, tools, dependencies)

## Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the existing style
   - Add tests for new functionality
   - Update documentation if needed
   - Ensure type hints are included

3. **Run tests and linters**
   ```bash
   pytest
   black .
   flake8 pypresence tests
   mypy pypresence
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Version Management

The project uses a **single source of truth** for versioning. The version is defined only in `pypresence/__init__.py`:

```python
__version__ = "4.5.2"
```

The `pyproject.toml` automatically reads this version using dynamic versioning:

```toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "pypresence.__version__"}
```

**When releasing a new version**, only update the version in `pypresence/__init__.py`. The version will automatically propagate to:
- Package metadata
- Build artifacts
- PyPI uploads
- All imports

## Building the Package

Install build tools:
```bash
pip install build
```

Build source distribution and wheel:
```bash
python -m build
```

The built packages will be in the `dist/` directory:
- `pypresence-x.x.x.tar.gz` (source distribution)
- `pypresence-x.x.x-py3-none-any.whl` (wheel)

## Continuous Integration

The project uses GitHub Actions for CI/CD:

### Test Workflow (`.github/workflows/test.yml`)
- Runs on every push and pull request
- Tests Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- Tests on Ubuntu, Windows, and macOS
- Ensures cross-platform compatibility

### Lint Workflow (`.github/workflows/lint_python.yml`)
- Runs bandit, black, codespell, flake8, isort, mypy
- Checks code quality and security
- Some checks are non-blocking (|| true)

### Publish Workflow (`.github/workflows/publish-to-pypi.yml`)
- Automatically publishes to PyPI on GitHub releases
- Uses trusted publishing (no API tokens needed)

## Contributing Guidelines

### Before Submitting a PR

✅ All tests pass (`pytest`)  
✅ Code is formatted (`black .`)  
✅ Imports are sorted (`isort .`)  
✅ No linting errors (`flake8 pypresence tests`)  
✅ Type checking passes (`mypy pypresence`)  
✅ New features have tests  
✅ Documentation is updated if needed  

### Code Style

- Follow PEP 8 (enforced by black and flake8)
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions focused and testable
- Prefer clarity over cleverness

### Commit Messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Common types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semi-colons, etc.)
- `refactor:` - Code refactoring (no feature changes or bug fixes)
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks (dependencies, build process, etc.)
- `ci:` - CI/CD changes

**Examples:**
```
feat: add support for Discord activity buttons
fix: resolve connection timeout on Windows
docs: update async client documentation
test: add coverage for presence.update method
chore: update pytest to 8.0.0
ci: add Python 3.13 to test matrix
```

**With scope:**
```
feat(presence): add button support
fix(client): handle connection timeout properly
docs(readme): add development section
```

**Breaking changes:**
```
feat!: remove deprecated sync_handler parameter

BREAKING CHANGE: The sync_handler parameter has been removed.
Use error_handler instead.
```

### Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature
3. **Make your changes** with tests
4. **Run all checks** (tests, linters, type checker)
5. **Push** to your fork
6. **Open a Pull Request** with a clear description
7. **Respond to feedback** from maintainers

## Additional Resources

- [pypresence Documentation](https://qwertyquerty.github.io/pypresence/html/index.html)
- [Discord Rich Presence Documentation](https://discord.com/developers/docs/rich-presence/how-to)
- [Discord RPC Documentation](https://discord.com/developers/docs/topics/rpc)
- [Discord API Support Server](https://discord.gg/discord-api)
- [pyresence Discord Support Server](https://discord.gg/JF3kg77)

## Getting Help

- Open an issue on GitHub for bugs or feature requests
- Join the Discord server for questions
- Check existing issues and PRs before creating new ones

## License

pypresence is licensed under the MIT License. See [LICENSE](LICENSE) for details.
