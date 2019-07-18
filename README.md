# Python-API-request-script
This script takes a client id and secret from a config.py file, and generates a token if the input is valid. It then sends a get request to the Beaver Bus API and prints the data from the request to the user.

To run the script, first install the dependencies with `pip install -r requirements.txt`. Then navigate to the directory `script.py` is located in, and run it with `python3 script.py`. The script requires an additional config.py file to define `client_id` and `client_secret` (see `config-example.py` for formatting). 

Version: Python 3.7.3
