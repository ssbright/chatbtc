import grpc
import os
import codecs
from lndgrpc import LNDClient, AsyncLNDClient
import qrcode
from dotenv import load_dotenv
from google.protobuf.json_format import MessageToDict
import time 

load_dotenv()

# Set up LND gRPC connection
cert_path = os.path.expanduser('node/tls.cert')
macaroon_path = os.path.expanduser('node/invoice.macaroon')

hash= "lnbc50n1p37avphpp5whngttlk2pv9a3kf5jsk9pumlj20t5fus394038rnzv0xuks4t8sdquf9h8vmmfvdjjqem9dejhyct5v4jqcqzpgxqyz5vqsp5hs500auh4fjhv5qqlyp4wdwsjmxsa7qxfzamawndpm57g4wwhh7s9qyyssq3ze5ejcpz535gh6rs50wsyhee846d5lssz5ymrs60h8k2sf3tkgprr3m240c4m296g8dpjk7t9e8g74twnslm8mkgpmht5lk7t6xc0qqzc0lla"

#Deine the RPC client for specifc channel from config file
LND_RPC_PORT = os.getenv('LND_NODE_PORT')
LND_RPC_IP = os.getenv('LND_NODE_IP')
LND_FOLDER = os.getenv('LND_FOLDER')
LND_MACAROON_FILE = os.getenv('LND_MACAROON_FILE')
LND_TLS_CERT_FILE = os.getenv('LND_TLS_CERT_FILE')
LND_RPC_HOST = os.getenv('LND_RPC_HOST')
lnd_ip_port = f"{LND_RPC_IP}:{LND_RPC_PORT}"



lnd = LNDClient(
    lnd_ip_port,
    macaroon_filepath=LND_MACAROON_FILE,
    cert_filepath=LND_TLS_CERT_FILE,
)



def create_invoice_nc(amt):
    lnd.add_invoice(amt,"Invoice generated");
    invoices = lnd.list_invoices()
    paymentHash = invoices.invoices._values[-1].payment_request
    print(invoices.state)
    qr = qrcode.make(paymentHash)
    qr.save("invoice.png")

