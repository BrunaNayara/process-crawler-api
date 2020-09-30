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
curl http://127.0.0.1:5000/processo/{numero-do-processo}
```
Alguns exemplos de processo
- 710802-55.2018.8.02.0001
- 806233-85.2019.8.02.0000
- 0821901-51.2018.8.12.0001

Os dois primeiros exemplos são do TJAL. O primeiro só tem info no primeiro grau e o segundo apenas no segundo.

O terceiro tem informações nos dois graus. (Ainda não está totalmente implementado no 2)

## Running the tests
```
python -m unittest
```
