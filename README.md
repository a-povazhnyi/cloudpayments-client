# **CloudPayments Client Gateway**

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/a-povazhnyi/cloudpayments-client.git
$ cd cloudpayments-client
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r build/requirements.txt
```

Run `main.py`
```sh
(venv)$ python main.py
```

## Info
- class **CloudPaymentsClient** needs `public_id`, `api_secret` to authorize
user's request 
- `charge` method is used for cryptogram Yandex payment. Required parameter is
`request_data`
