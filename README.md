# recruitment-challenge-2019
Working repo for developing the challenge to test out potential employees

## How to use this tool

After setting up the dev environment, run the following command:

```batch
python process_data.py INPUT_CSV_FILE POSTCODE --output_file=OUTPUT_CSV_FILE --output_endpoint=OUTPUT_API_URL
```

## Development guide

### Environment set-up

Requires [virtualenv](https://virtualenv.pypa.io/en/latest/).

On windows:

```batch
python -m virtualenv env
env\Scripts\activate
pip install -r requirements.txt
```

On linux:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Running tests

[Tox](https://tox.readthedocs.io/en/latest/) is used for unit testing and continuous integration, install it via `python -m pip install tox` and run the unit tests using:

```batch
tox
```

Note: you may also need to install the [tox-venv](https://pypi.org/project/tox-venv/) package depending on your environment `python -m pip install tox-venv`


## Deployment

TODO
