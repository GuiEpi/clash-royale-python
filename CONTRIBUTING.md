# Contributing

Contributions are welcome, and they are greatly appreciated! Every little helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs on [our issues page][gh-issues]. If you are reporting a bug, please include:

- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" is open to whoever wants to implement it.

### Write Documentation

This module could always use more documentation, whether as part of the official docs, in docstrings, or other.

### Submit Feedback

The best way to send feedback is to file a ticket on [our issues page][gh-issues]. If you are proposing a feature:

- Explain how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome.

## Get Started!

Ready to contribute? Here's how to set up `clash-royale-python` for local development.

1. Fork the repo on GitHub.

2. Clone your fork locally:

   ```shell
   git clone git@github.com:your_name_here/clash-royale-python.git
   ```

3. Install the dependencies with [uv](https://docs.astral.sh/uv/):

   ```shell
   uv sync --dev --group docs
   ```

4. Create a branch for local development:

   ```shell
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass our tests:

   ```shell
   uv run pytest
   ```

6. Type checking is done with [ty](https://docs.astral.sh/ty/), and is run with:

   ```shell
   uv run ty check
   ```

7. Linting is done through [pre-commit](https://pre-commit.com). You can run all hooks as a one-off:

   ```shell
   uv run pre-commit run -a
   ```

   Or better, install the hooks once and have them run automatically each time you commit:

   ```shell
   uv run pre-commit install
   ```

8. Commit your changes, quoting GitHub issue in the commit message, if applicable, and push your branch to GitHub:

   ```shell
   git add .
   git commit -m "feat(something): your detailed description of your changes"
   git push origin name-of-your-bugfix-or-feature
   ```

   Note: the commit message should follow [the conventional commits](https://www.conventionalcommits.org). We run [`commitlint` on CI](https://github.com/marketplace/actions/commit-linter) to validate it, and if you've installed pre-commit hooks at the previous step, the message will be checked at commit time.

9. Submit a pull request on GitHub.

## Obtain an API Key

To work with the Clash Royale API, you'll need an API key. You can obtain one from the [Clash Royale Developer Portal](https://developer.clashroyale.com/).

1. Create an account or log in at [developer.clashroyale.com](https://developer.clashroyale.com/)
2. Go to "My Account" and create a new API key
3. Whitelist your IP address(es) for the key

For testing, you can use the [RoyaleAPI proxy](https://docs.royaleapi.com/#/proxy) which doesn't require IP whitelisting.

Create a `.env` file in the project root with your API key:

```shell
CLASH_ROYALE_API_KEY=your-api-key-here
```

This is used when generating VCR cassettes for tests.

## Pull Request Guidelines

Feel free to open the pull request as soon as possible, but please be explicit if it's still a work in progress, we recommend draft pull requests. Please try to:

1. Include tests for feature or bug fixes.
2. Update the documentation for any significant API changes.
3. Ensure tests are passing on continuous integration.

## Building Documentation

The documentation is built with Sphinx. To build it locally:

```shell
uv sync --group docs
cd docs
uv run make html
```

The built documentation will be in `docs/build/html/`.

For live reloading during development:

```shell
uv run sphinx-autobuild docs/source docs/build/html
```
