# pypresence Test Suite

This directory contains the test suite for pypresence.

## Structure

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── test_payloads.py         # Tests for payload generation (no I/O)
├── test_utils.py            # Tests for utility functions
├── test_types.py            # Tests for type enums
├── test_exceptions.py       # Tests for exception classes
├── test_presence.py         # Tests for Presence class (mocked I/O)
├── test_baseclient.py       # Tests for BaseClient (mocked I/O)
└── README.md                # This file
```

## Running Tests

### Install test dependencies

```bash
pip install pytest pytest-asyncio pytest-mock
```

### Run all tests

```bash
pytest
```

### Run specific test files

```bash
pytest tests/test_payloads.py
pytest tests/test_presence.py
```

### Run specific test classes or methods

```bash
pytest tests/test_payloads.py::TestPayloadGeneration
pytest tests/test_payloads.py::TestPayloadGeneration::test_basic_payload_creation
```

### Run with coverage

```bash
pip install pytest-cov
pytest --cov=pypresence --cov-report=html
```

### Run tests with verbose output

```bash
pytest -v
```

### Run tests and show print statements

```bash
pytest -s
```

## Test Categories

### Unit Tests (No I/O)
- `test_payloads.py` - Tests payload generation logic
- `test_utils.py` - Tests utility functions
- `test_types.py` - Tests type enums
- `test_exceptions.py` - Tests exception classes

These tests run entirely in-memory with no external dependencies.

### Integration Tests (Mocked I/O)
- `test_presence.py` - Tests Presence class with mocked sockets
- `test_baseclient.py` - Tests BaseClient with mocked connections

These tests mock the IPC communication layer to test the full flow without requiring Discord.

## Key Testing Strategies

### 1. **Mocking Socket Communication**
We mock `sock_reader` and `sock_writer` to simulate Discord IPC responses:

```python
presence.sock_writer = Mock()
presence.sock_reader = AsyncMock()
```

### 2. **Testing Payload Format**
We verify that payloads are correctly formatted by parsing the sent data:

```python
call_args = presence.sock_writer.write.call_args[0][0]
op, length = struct.unpack('<II', call_args[:8])
payload_json = call_args[8:8+length].decode('utf-8')
payload = json.loads(payload_json)
```

### 3. **Testing Error Handling**
We simulate various error conditions:

```python
client.sock_reader.read = AsyncMock(side_effect=BrokenPipeError())
with pytest.raises(PipeClosed):
    await client.read_output()
```

### 4. **Testing Async Code**
We use pytest-asyncio for async tests:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected
```

## What's NOT Tested

These tests do **NOT** require:
- Discord to be running
- A valid Discord application/client ID
- Network connectivity
- Visual verification of what appears in Discord

The tests focus on:
- Correct payload generation
- Proper protocol implementation
- Error handling
- Parameter validation and conversion

## Future Additions

Potential future test additions:

1. **Mock IPC Server** - Create a fake Discord IPC server for full integration testing
2. **Smoke Tests** - Optional tests that verify real Discord connectivity (marked with `@pytest.mark.manual`)
3. **Property-based Testing** - Use hypothesis for testing edge cases
4. **Performance Tests** - Benchmark payload generation and serialization

## Writing New Tests

When adding new tests:

1. Use appropriate fixtures from `conftest.py`
2. Mock external dependencies (sockets, file I/O)
3. Test both success and error cases
4. Use descriptive test names that explain what's being tested
5. Add docstrings to test classes and methods
6. Group related tests in classes

Example:

```python
class TestNewFeature:
    """Test the new feature"""
    
    def test_feature_with_valid_input(self, client_id):
        """Test that feature works with valid input"""
        # Test implementation
        pass
    
    def test_feature_with_invalid_input(self, client_id):
        """Test that feature raises appropriate error with invalid input"""
        # Test implementation
        pass
```
