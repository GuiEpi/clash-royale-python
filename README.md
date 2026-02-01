<div align="center">
    <h1>Clash Royale Python 👑</h1>
</div>

<p align="center">
    <a href="https://github.com/guiepi/clash-royale-python/actions/workflows/ci.yml?query=branch%3Amain">
        <img alt="CI Status" src="https://img.shields.io/github/actions/workflow/status/guiepi/clash-royale-python/ci.yml?branch=main&logo=github&style=flat-square">
    </a>
    <a href="https://guiepi.github.io/clash-royale-python/">
        <img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue?style=flat-square&logo=github" alt="Documentation">
    </a>
    <a href="https://codecov.io/gh/guiepi/clash-royale-python">
        <img src="https://img.shields.io/codecov/c/github/guiepi/clash-royale-python.svg?logo=codecov&style=flat-square" alt="Test coverage percentage">
    </a>
    </p>
    <p align="center">
    <a href="https://github.com/astral-sh/uv">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
    </a>
    <a href="https://github.com/astral-sh/ty">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json" alt="ty">
    </a>
    <a href="https://github.com/pre-commit/pre-commit">
        <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
    </a>
</p>
<p align="center">
    <a href="https://pypi.org/project/clash-royale-python/">
        <img src="https://img.shields.io/pypi/v/clash-royale-python.svg?logo=python&amp;logoColor=fff&amp;style=flat-square" alt="PyPi Status">
    </a>
        <img src="https://img.shields.io/pypi/pyversions/clash-royale-python.svg?style=flat-square" alt="pyversions">
        <img src="https://img.shields.io/pypi/l/clash-royale-python.svg?style=flat-square" alt="license">
</p>

<br />

<div align="center">
    <strong>A friendly, synchronous, fully-typed Python wrapper around the <a href="https://developer.clashroyale.com">Clash Royale API</a>.</strong>
</div>

<br />

<div align="center">
    <a href="https://github.com/guiepi/clash-royale-python">Source code</a>
    <span> · </span>
    <a href="https://guiepi.github.io/clash-royale-python/">Documentation</a>
</div>

<br />

<div align="center">
    <sub>Cooked by <a href="https://github.com/GuiEpi/">Guillaume Coussot</a> 👨‍🍳</sub>
</div>

<br />

## Installation

The package is published on [PyPI](https://pypi.org/project/clash-royale-python/) and can be installed by running:

```shell
pip install clash-royale-python
```

## Basic Use

Easily query the Clash Royale API from your Python code. The data returned by the API is mapped to fully-typed Python models:

```python
import clash_royale

client = clash_royale.Client(api_key="your-api-key")

# Get a player by tag
player = client.players.get("#ABC123")
print(player.name)

# Get a clan and its members
clan = client.clans.get("#XYZ789")
for member in client.clans.get_members("#XYZ789"):
    print(member.name)

# Search for clans
results = client.clans.search(name="Royal")
for clan in results:
    print(clan.name)
```

Ready for more? Check out the full [documentation](https://guiepi.github.io/clash-royale-python/).
