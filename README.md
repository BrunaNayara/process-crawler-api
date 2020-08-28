# process-crawler-api

Using virtualenv 
```
pip3 install -r requirements.txt
```

To run
```
flask run
```

To make a request
```
curl --header "Content-Type: application/json" --request GET --data '{"numProcesso": "0710802-55.2018.8.02.0001"}'   http://127.0.0.1:5000/processo
```
Example of a request
