# -----------------server ontvang foto
# laad modules
import base64
from math import ceil
from bluetooth import *

# ---- setup
# constanten
afbeelding_path = "ontvang.jpg" # ontvangen afbeelding opslaan in
aantal_tekens = 50 # beslist hoeveel tekens wordt gebruikt om het aantal lijsten te verzenden

# ---- zet server aan
# ---set server
server_socket=BluetoothSocket( RFCOMM )
server_socket.bind(("", 3 ))
server_socket.listen(1)
client_socket, address = server_socket.accept()

# ----- ontvang data
#ontvang het getal van totaal aantal lijsten
aantal_str = client_socket.recv(aantal_tekens)
aantal = int(aantal_str)

# ontvang chunks van 1024 karakters en zet ze in 1 string (afbeelding_b64)
afbeelding_b64=""
for i in range(0,aantal):
    afbeelding_b64=afbeelding_b64+client_socket.recv(1024)
    print("chunk %d van %d ontvangen" % (i,aantal))

# ---- decrypt data
# zet data om van base64 naar normaal en slaat het op in bestand
fh = open(afbeelding_path, "wb")
fh.write(afbeelding_b64.decode('base64'))
fh.close()

# ---- zet server uit
#close connection
client_socket.close()
server_socket.close()
print("voltooid!!!")
