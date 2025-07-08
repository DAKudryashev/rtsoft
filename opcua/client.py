import time
from opcua import Client

URL = "opc.tcp://localhost:4840"

if __name__ == "__main__":
    client = Client(URL)
    client.connect()
    voltNode = client.get_node("ns=2;i=2")
    while True:
        voltage = voltNode.get_value()
        print("{0:.1f} В".format(voltage))
        time.sleep(1)
