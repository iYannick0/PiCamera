# -----------------client zend foto
# laad modules
import base64
from math import ceil
from bluetooth import *

# ---- setup
# constanten
afbeelding_path = "test.jpg"
mac_adress = "B8:27:EB:43:1D:AF"
aantal_tekens = 50 # beslist hoeveel tekens wordt gebruikt om het aantal lijsten te verzenden

# ---lees bestand en encrypt en zet het in afbeelding_b64 
imageFile = open(afbeelding_path, "rb")
afbeelding_b64 = base64.b64encode(imageFile.read())
imageFile.close()

# ---hak afbeelding_b64 in stuken van 1024 tekens en zet in (lijst)
str_len = len(afbeelding_b64)
chunk = 1024.0 # groote deel (moet een coma getal zijn!!!!)
aantal = int(ceil(str_len/chunk))
lijst = [""]*aantal
n=0
q=0
for i in range(0,str_len):
    lijst[n] = lijst[n] + afbeelding_b64[i]
    q=q+1
    if q >= chunk:
        n=n+1
        q=0

# ---zend de lijsten van 1024 tekens
# opent connectie
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect((mac_adress, 3))

# zend hoeveel lijsten er worden verzonden
client_socket.send(' '*(aantal_tekens-len(str(aantal)))+str(aantal))

# zend lijsten
for i in range(0,aantal):
    client_socket.send(lijst[i])
    print("zend chunk %d van %d" % (i,aantal))

# --- eindig programa
# sluit connectie
client_socket.close()
print("voltooid!!!")
