#!/usr/bin/python3

import requests
from hashlib import md5

# Producción - https://vpos.infonet.com.py
# Staging - https://vpos.infonet.com.py:8888

url = 'http://localhost:8008'
env_staging = "https://vpos.infonet.com.py:8888"
env_prod = "https://vpos.infonet.com.py"
private_key = "FVwH3T1DQAz.k(DlnWBL+mtkmRxQF9EK,.YkaJXd"
shop_process_id = "7"
amount = "1000.00"
currency = "PYG"

token = md5(private_key.encode('utf-8') + shop_process_id.encode('utf-8') + amount.encode('utf-8') + currency.encode('utf-8'))

data = {
    "public_key": "PZ3M9x4FvsiHDl5T4thxltJit9HbHQse",
    "operation": {
        "token": token.hexdigest(),
        "shop_process_id": shop_process_id,
        "currency": currency,
        "amount": amount,
        "additional_data": "",
        "description": "Test desde python con token generado",
        "return_url": "https://tecnopro.com.py/webhooks/bancard/approved",
        "cancel_url": "https://tecnopro.com.py/webhooks/bancard/cancelled"
    }
}

answ = requests.post(url="%s/vpos/api/0.3/single_buy" % env_staging, json=data)

if answ.ok:
    json = answ.json()
    process_id = json.get('process_id')
    url = '%s/checkout/new?process_id=%s' % (env_staging, process_id)
else:
    json = answ.json()
    print(json.get('status'))
    for msg in json.get('messages'):
        print(msg.get('level'))
        print(msg.get('key'))
        print(msg.get('dsc'))

print(url)
