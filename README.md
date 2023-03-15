# Muninn Prototype

Muninn is an assistant that brings together multiple organizational, search, and AI tools to help users perform research and store information in an organized way that can easily be recalled. This prototype version of Muninn is a Python-based application that demonstrates the core functionality of the tool.

## Developer Setup

The project uses [Poetry](https://python-poetry.org/docs/) to manage dependencies

To set up a Python environment for Muninn, please follow these steps:
```pwsh
setup_dev.ps1
```

### Download the english model for spacy to use
```sh
python -m spacy download en_core_web_sm
```

## Running the tests
To run all tests in the current directory and its subdirectories, use the following command:
```sh
poe unit
poe integration
poe model
```


To start using Muninn, simply run the `muninn.py` file with Python:
This will launch the Muninn prototype, which you can use to perform research and store information.

## Contributing

If you would like to contribute to Muninn, please submit a pull request with your proposed changes. We welcome contributions of all types, including bug fixes, new features, and documentation improvements.


