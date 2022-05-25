import socket
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("IP", help="Adresse IP sur laquelle le serveur écoute")
parser.add_argument("PORT", help="Numéro du port sur lequel le serveur écoute", type=int)
parser.add_argument("PROTOCOLE", help="Protocole TCP ou UDP")
args = parser.parse_args()


# Crée une socket datagramme ou TCP
if args.PROTOCOLE == "UDP":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print( "Le client chat émet en mode ", args.PROTOCOLE, " à destination de l'adresse IP" ,args.IP, " et vers le port n°: ", args.PORT)
print( "Taper quit pour quitter l'application")
print( "" )

msg = ""

while msg != "quit" :
    msg = input("> ")

    if args.PROTOCOLE == "TCP":
        if s.connect((args.IP, args.PORT)):
            for i in range(1000000000000000000000000000000000000):
                s.send( str.encode( msg ) )
    else:
        for i in range(1000000000000000000000000000000):
            s.sendto( str.encode( msg ), (args.IP, args.PORT))

s.close()
    
