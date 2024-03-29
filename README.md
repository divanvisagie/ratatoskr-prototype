# Muninn Prototype

Muninn is an assistant that brings together multiple organizational, search, and AI tools to help users perform research and store information in an organized way that can easily be recalled. This prototype version of Muninn is a Python-based application that demonstrates the core functionality of the tool.

## Developer Setup


The project uses [Poetry](https://python-poetry.org/docs/) to manage dependencies

To set up a Python environment for Muninn, please follow these steps:

Windows
```pwsh
setup_dev.ps1
```

Linux/MacOS
```bash
setup_dev.sh
```

#### Prerequisites
Install pytorch into the pip environment based on your [Compute Platform](https://pytorch.org/get-started/locally/)

##### GPU
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

##### CPU
```
pip3 install torch torchvision torchaudio
```

##### Set transformers cache location
To set the huggingface cache location, you can set the environment variable `TRANSFORMERS_CACHE` to the location you want to use. For example, on Windows, you can use the following command to set the cache location to `D:\Models` in the environment variables section of the system properties, or in your `.bashrc` file on Linux/MacOS:
```sh
TRANSFORMERS_CACHE=D:/Models
```


### Database
```sh
docker-compose up -d
```

### Download the english model for spacy to use
```sh
python -m spacy download en_core_web_sm
```

## Running the tests
To run all tests in the current directory and its subdirectories, use the following command:
```sh
./test.py unit
./test.py integration
./test.py model
```


To start using Muninn, simply run the `muninn.py` file with Python:
This will launch the Muninn prototype, which you can use to perform research and store information.

## Contributing

If you would like to contribute to Muninn, please submit a pull request with your proposed changes. We welcome contributions of all types, including bug fixes, new features, and documentation improvements.


