# polta-cli
_Textual CLI applications for polta implementations._

# At a Glance

This repository contains various CLI applications that will aid you in your projects that utilize `polta`.

As such, this is an optional companion repository to `polta`.

## Metastore

This app allows you to view and manage your `polta` metastores in one convenient terminal.

### Tables Screen

_View tables at a glance, and even read them with basic SQL filtering options._

### Volumes Screen

_View ingestion, quarantine, and export directories. Open files using default system programs._

# Installation

This project exists in `PyPI` and can be installed this way:

```sh
pip install polta-cli
```

## Initializing the Repository

To use the code from the repository itself, either for testing or contributing, follow these steps:

1. Clone the repository to your local machine.
2. Create a virtual environment, preferably using `venv`, that runs `Python 3.13`. 
3. Ensure you have `poetry` installed (installation instructions [here](https://python-poetry.org/docs/#installation)).
4. Make `poetry` use the virtual environment using `poetry env use .venv/path/to/python`.
5. Download dependencies by executing `poetry install`.
6. Building a wheel file by executing `poetry build`.

# Running an App

Each application exists in the top-level directory of this repository. There are two ways to access them.

This sub-section will use the `MetastoreApp` as an example, but the same processs applies to the other apps.

## Running via Terminal

Run this at the top-level of this repository:

```sh
poetry run metastore path/to/metastore
```

## Running via Python Code

In your own project, import this package via `pip` as detailed in the `Installation` section above.

Then, import and run the app directory:

```python
from sys import argv
from polta_cli.metastore import MetastoreApp


app: MetastoreApp = MetastoreApp('path/to/metastore')
app.run()
```

# License

This project exists under the `MIT License`.

## Acknowledgements

The `polta-cli` project uses third-party dependencies that use the following permissive open-source licenses:

1. `Apache Software License (Apache-2.0)`
2. `MIT License`

Below are the top-level packages with their licenses.

| Package | Version | Purpose | License |
| ------- | ------- | ------- | ------- |
| [polta](https://github.com/JoshTG/polta/tree/main) | >=0.8.2, <0.9.0 | The data storage / transformation package | MIT License |
| [pytest](https://github.com/pytest-dev/pytest) | >=8.3.5, <8.4.0 | Runs test cases for unit testing | MIT License |
| [pytest-cov](https://github.com/pytest-dev/pytest-cov) | >=6.2.1, <6.3.0 | Applies test coverage to pytest runs | MIT License |
| [ruff](https://github.com/astral-sh/ruff) | >=0.12.3, <0.13.0 | Executes linting checks in the repository | MIT License |
| [ruff-action](https://github.com/astral-sh/ruff-action) | latest | Executes a ruff check in the GitHub workflow | Apache Software License (Apache-2.0) |
| [textual](https://github.com/Textualize/textual) | >=5.3.0,<5.4.0 | Builds the CLI applications | MIT License |
| [tzdata](https://github.com/python/tzdata) | >=2025.2, <2026.1 | Contains timezone information for Datetime objects | Apache Software License (Apache-2.0) |

# Contributing

Because this project is open-source, contributions are most welcome by following these steps:

1. Submit the contribution request to the [issues page](https://github.com/JoshTG/polta-cli/issues).
2. Await signoff/feedback from a repository administrator.
3. Clone the repository into your local machine.
4. Create a descriptive feature branch.
5. Make the desired changes.
6. Uptick the `poetry` project version appropriately using standard semantic versioning.
7. Create a merge request into the `main` branch of the official `polta-cli` project and assign it initially to @JoshTG.
8. Once the merge request is approved and merged, an administrator will schedule a release cycle and deploy the changes using a new release tag.

# Contact

You may contact the main contributor, [JoshTG](https://github.com/JoshTG), by sending an email to this address: jgillilanddata@gmail.com.
