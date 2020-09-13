# process-crawler-api

## Setup
```
pip3 install -r requirements.txt
```

## Running
```
flask run
```

## Making a request

This is an example of a request.
```
curl --header "Content-Type: application/json" --request GET --data '{"numProcesso": "0710802-55.2018.8.02.0001"}'   http://127.0.0.1:5000/processo
```

## Running the tests
```
python -m unittest
```
