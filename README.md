# Muninn Prototype

Muninn is an assistant that brings together multiple organizational, search, and AI tools to help users perform research and store information in an organized way that can easily be recalled. This prototype version of Muninn is a Python-based application that demonstrates the core functionality of the tool.

## Developer Setup

To set up a Python environment for Muninn, please follow these steps:

1. Create a new virtual environment for the project:
    ```
    $ python -m venv env
    ```
2. Activate the virtual environment:
    - On Unix or Linux-based systems:
    ```
    $ source env/bin/activate
    ```
    - On Windows:
    ```
    env\Scripts\activate
    ```
3. Install the required packages for the project:
    ```
    $ pip install -r requirements.txt
    ```
    **Note:** If you add any new dependencies, be sure to update the requirements.txt file and freeze pip by running the following command:
    ```
    $ pip freeze > requirements.txt
    ```


## Running the tests
To run all tests in the current directory and its subdirectories, use the following command:
```
python -m unittest discover -s .
```

## Usage

### Run the database migrations

```
alembic upgrade head
```

To start using Muninn, simply run the `muninn.py` file with Python:
This will launch the Muninn prototype, which you can use to perform research and store information.

## Contributing

If you would like to contribute to Muninn, please submit a pull request with your proposed changes. We welcome contributions of all types, including bug fixes, new features, and documentation improvements.


