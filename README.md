# llm-tools-memory

[![PyPI](https://img.shields.io/pypi/v/llm-tools-memory.svg)](https://pypi.org/project/llm-tools-memory/)
[![Changelog](https://img.shields.io/github/v/release/tombedor/llm-tools-memory?include_prereleases&label=changelog)](https://github.com/tombedor/llm-tools-memory/releases)
[![Tests](https://github.com/tombedor/llm-tools-memory/actions/workflows/test.yml/badge.svg)](https://github.com/tombedor/llm-tools-memory/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/tombedor/llm-tools-memory/blob/main/LICENSE)

Memory tools for LLM

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-tools-memory
```
## Usage

To use this with the [LLM command-line tool](https://llm.datasette.io/en/stable/usage.html):

```bash
llm --tool create_memory "Example prompt goes here" --tools-debug
```

With the [LLM Python API](https://llm.datasette.io/en/stable/python-api.html):

```python
import llm
from llm_tools_memory import create_memory

model = llm.get_model("gpt-4.1-mini")

result = model.chain(
    "Example prompt goes here",
    tools=[create_memory]
).text()
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-tools-memory
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
