from ast import Pass
import requests
import json
import os
from dotenv import load_dotenv
import qrcode
import qrcode.image.svg

price=2000

def get_access_token():


    url1 = "https://api.rapaygo.com/v1//auth/key"

    load_dotenv()


    key = os.getenv("KEY")
    password = os.getenv("SECRET")
    payload = {
        "key": key,
        "secret": password
        }

    headers = {
        'Authorization': ''
        }
    response1 = requests.request("POST", url1, data=json.dumps(payload))
    #print(response1)
    tokenDict = json.loads(response1.text)
    accessToken = tokenDict["access_token"]
    #print(accessToken)
    return accessToken
 

def create_invoice():
    url2 = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"
    accessToken = get_access_token()
    payload = {
      "amount_sats": "{}".format(price),
      "memo": "rapaygo POS invoice",
    }

    headers = {
      'Authorization': accessToken
    }
    response = requests.request("POST", url2, headers=headers, data=json.dumps(payload))

    #print(response.text)
    tokenDict = json.loads(response.text)
    #print("tokenDict", tokenDict)
    qr = qrcode.make(tokenDict["payment_request"])
    qr.save("invoice.png")
    #print(invoice)
    return tokenDict

def payment_confirmed_checker(pay_hash, amt):
  # Payment verifidier

  url3 = "https://api.rapaygo.com/v1/invoice_payment/by_payment_hash/{}".format(pay_hash)

  payload = {
    "amount_sats": amt,
    "memo": "rapaygo POS invoice",
  }

  headers = {
    'Authorization': '',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url3, headers=headers, data=payload)
  responseDict = response.json()
  #print(responseDict)
  '''
  {"amount":200,
  "checking_id":"3ca2f50e55c98b25734fd8306bf8dbd0c11da70369948d45a6cccb84cf72a92e",
  "created_at":"2022-06-15 23:23:21.154171",
  "created_at_ts":1655335401.154171,
  "extra":"",
  "fee":0,
  "id":2610,
  "ln_fee":0,
  "lnurl_payment_id":null,
  "memo":"7c686 POS payment. rapaygo POS invoice",
  "msat_amount":200000,
  "msat_fee":0,
  "msat_ln_fee":0,
  "msat_tx_fee":2000,
  "payment_hash":"3ca2f50e55c98b25734fd8306bf8dbd0c11da70369948d45a6cccb84cf72a92e",
  "payment_request":"lnbc2u1p32560fpp58j302rj4ex9j2u60mqcxh7xm6rq3mfcrdx2g63dxen9cfnmj4yhqhp56mgev926f9h2f88f9l78at6js6klpz8juh52zm9ehrr3pyr9selqcqzpgxqyz5vqsp5everph8kx3wsgzw5d4u3zruhkwlyj0adm7sux829zyf0cu6n270s9qyyssqrmtpmr86j3vr9luczu3g2d7zzt625y26wlp3uz23pqvw26gvcnkkw7pklempcyt7k4lvgp90fay0vfq0v3daqdt7ccq5dne038zf0tsqgqqmwr",
  "pending":false,
  "pending_int":0,
  "preimage":"",
  "status":"COMPLETED",
  "tx_fee":2,
  "updated_at":"2022-06-15 23:23:58.636452",
  "wallet_id":141,
  "webhook":"",
  "webhook_external_id":null,
  "webhook_status":"pending",
  "withdraw_voucher_id":null}
  '''

  payment_stat = responseDict["status"]

  return payment_stat