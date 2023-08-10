import sys
sys.path.insert(0, "..")
import logging

from IPython import embed
import asyncio
from asyncua import Client

'''
comand1 generates a key: "openssl genrsa -out key.pem 2048"
comand2 generates a x509v3 certificate: "openssl req -x509 -days 365 -new -out cert.pem -key key.pem -config ssl.conf"
openssl x509 -outform der -in cert.pem -out my_cert.der
'''
async def get_t():
    client = Client("opc.tcp://localhost:53530/OPCUA/SimulationServer/")

    await client.load_client_certificate('my_cert.der')
    await client.load_private_key('key.pem')

    try:

        await client.connect()
        root = client.nodes.root
        objects = client.nodes.objects
        print("childs og objects are: ",await objects.get_children())
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_t())