from ast import Pass
import requests
import json
import os
from dotenv import load_dotenv
import psycopg2
import qrcode
import qrcode.image.svg

def get_access_token():
    conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
    cur = conn.cursor()
    cur.execute('select * from user_pos')
    conn.commit()

    user_table = cur.fetchall()


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
      "amount_sats": "{}".format(10),
      "memo": "rapaygo POS invoice",
    }

    headers = {
      'Authorization': accessToken
    }
    response = requests.request("POST", url2, headers=headers, data=json.dumps(payload))

    #print(response.text)
    tokenDict = json.loads(response.text)
    #print("tokenDict", tokenDict)
    price=tokenDict["amount"]
    qr = qrcode.make(tokenDict["payment_request"])
    qrimage = qr.save("invoice.png")
    invoice="Here is your patment request for {} sats: ```{}```".format(tokenDict["amount"],tokenDict["payment_request"])
    #print(invoice)
    return invoice

create_invoice()